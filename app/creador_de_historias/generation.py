import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Asigna tokens según la longitud deseada (tokens, palabras)
LENGTH_MAP = {
    "corta":    (550,400),    
    "mediana":  (800, 600), 
    "larga":    (1100, 800)   
}

def generar_historia(prompt: str, longitud: str = "mediana") -> str:
    """
    Genera una historia con un LLM basada en un prompt. 
    Si se supera el limite de longitud de la respuesta se le indica al LLM que genere una versión más corta de la historia
    
    Parámetros:
        prompt (str): prompt escrito directamente por el usuario o construido mediante formulario.
        longitud (str): Longitud de la historia deseada por el usuario

    Retorna:
        str: Historia .
    """
    try:
        max_tokens, max_palabras = LENGTH_MAP.get(longitud, LENGTH_MAP["mediana"])

        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {"role": "system", "content": "Eres un narrador experto en crear historias estructuradas y creativas para los usuarios."},
                {"role": "user", "content": f"{prompt}\nLa historia no debe tener más de {max_palabras + 100}, no digas cuantas palabras o caracteres tiene la historia"}
            ],
            temperature=0.8,
            max_tokens=max_tokens,
            top_p=1.0
        )

        respuesta = completion.choices[0].message.content.strip()
        finish_reason = completion.choices[0].finish_reason

        # Si se cortó por límite, intenta una nueva versión más resumida
        if finish_reason == "length":
            st.warning("La respuesta se cortó por ser demasiado larga") ## quitar
            retry_prompt = (
                f"La historia generada con el siguiente prompt fue muy larga para el espacio permitido. "
                f"{prompt}"
                f"Por favor, reescríbela manteniendo su esencia, pero con una trama más acelerada "
                f"que encaje en aproximadamente {max_palabras} palabras"

            )

            retry_completion = client.chat.completions.create(
                model="deepseek/deepseek-chat",
                messages=[
                    {"role": "system", "content": "Eres un narrador experto en crear versiones más concisas de historias largas sin perder coherencia ni creatividad."},
                    {"role": "user", "content": retry_prompt},
                    {"role": "assistant", "content": respuesta}
                ],
                temperature=0.8,
                max_tokens=max_tokens,
                top_p=1.0
            )

            return retry_completion.choices[0].message.content.strip()

        return respuesta

    except Exception as e:
        raise RuntimeError(f"❌ Error al generar historia con OpenRouter: {e}")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Error de conexión al refinar historia. Intenta nuevamente más tarde.")

def refinar_historia(historia_actual: str, sugerencia: str, datos_entrada: dict, modo: str = "formulario") -> str:
    """
    Refina una historia generada previamente con base en una sugerencia del usuario.

    Parámetros:
        historia_actual (str): Historia original generada.
        sugerencia (str): Recomendación o ajuste deseado.
        datos_entrada (dict): Datos que dieron origen a la historia.
        modo (str): "formulario" o "texto_libre", define cómo construir el contexto.

    Retorna:
        str: Historia modificada.
    """
    if modo == "formulario":
        contexto = construir_contexto(datos_entrada)
    else:  # modo texto libre
        contexto = f"""El usuario inicialmente describió la historia de esta manera:
            \"\"\"{datos_entrada.get('descripcion_libre', '')}\"\"\"
            Ten esto presente al hacer modificaciones, ya que esta fue la base de la historia."""

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un narrador experto en editar y mejorar historias manteniendo coherencia, estilo y estructura."},
                {"role": "user", "content": f"{contexto}"},
                {"role": "assistant", "content": historia_actual},
                {"role": "user", "content": f"Por favor, modifica la historia anterior siguiendo esta sugerencia:\n{sugerencia}"}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=1.0
        )

        return completion.choices[0].message.content.strip()

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Error de conexión al refinar historia. Intenta nuevamente más tarde.")
    except Exception as e:
        raise RuntimeError(f"Error al refinar historia: {e}")

    
def construir_contexto(datos_entrada: dict) -> str:
    """
    Utiliza los datos obtenidos del formulario para ser añadidos como parte del prompt para construir la historia.

    Parámetros:
        datos_entrada (dict): datos del formulario.

    Retorna:
        str: contexto para el modelo.
    """

    contexto = "Esta es la información base de la historia:\n"
    for clave, valor in datos_entrada.items():
        clave_limpia = clave.replace('_', ' ').capitalize()
        if isinstance(valor, str) and valor.strip() == "":
            valor = "No especificado"
        contexto += f"- {clave_limpia}: {valor}\n"
    return contexto.strip()
