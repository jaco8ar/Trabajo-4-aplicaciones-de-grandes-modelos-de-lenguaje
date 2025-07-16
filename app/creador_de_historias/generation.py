import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import requests
import re

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MAX_TOKENS = 200

# Asigna tokens según la longitud deseada (tokens, palabras)
LENGTH_MAP = {
    "corta":    400,    
    "mediana":  600, 
    "larga":    800   
}



def generar_historia(prompt: str, longitud: str = "mediana") -> str:
    """
    Genera una historia y la valida por número de palabras. Si no cumple el rango,
    intenta corregirla hasta 2 veces.
    """
    max_palabras = LENGTH_MAP.get(longitud, LENGTH_MAP["mediana"])
    min_palabras = max_palabras - (200 if longitud != "corta" else 100)

    historia = generar_historia_una_vez(prompt)
    palabras = contar_palabras(historia)

    intentos = 0
    while (palabras < min_palabras or palabras > max_palabras) and intentos < 3:
        razon = "muy corta" if palabras < min_palabras else "muy larga"
        # st.warning(f"La historia es {razon}, intentando ajustarla...")
        historia = corregir_longitud_historia(historia, prompt, max_palabras, razon)
        palabras = contar_palabras(historia)
        intentos += 1

    return historia


def corregir_longitud_historia(historia: str, prompt: str, max_palabras: int, razon: str) -> str:
    """
    Corrige la longitud de una historia: la resume o la expande.
    
    Parámetros:
        historia (str): Historia original.
        prompt (str): Prompt inicial.
        max_palabras (int): Límite superior.
        razon (str): "muy corta" o "muy larga"
    """
    if razon == "muy corta":
        instruccion = (
            "La historia anterior es demasiado breve. Reescríbela con una trama más rica, más escenas y profundidad, "
            "Agregale más detalles al final, a todo el mundo le gusta un buen final"
            f"sin cambiar su esencia. Apunta a unas {max_palabras} palabras."
        )
    else:  # muy larga
        instruccion = (
            f"La historia anterior es muy extensa. Reescríbela de forma más concisa, resume escenas secundarias y elimina repeticiones, "
            f"para que encaje en unas {max_palabras} palabras."
        )
    instruccion += "Solo debes decir el titulo de la historia y la historia nada de comentarios extra o entre parentesis."
    
    retry_completion = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": "Eres un narrador experto en ajustar la longitud de historias sin perder coherencia ni estilo"
                                        " y con una excelente memoria para detalles como nombres y los temas de las historias." },
                                       
            {"role": "user", "content": instruccion},
            {"role": "assistant", "content": historia}
        ],
        temperature=0.8,
        max_tokens=MAX_TOKENS,
        top_p=1.0
    )

    return retry_completion.choices[0].message.content.strip()

def generar_historia_una_vez(prompt: str) -> str:
    """Llama una vez al modelo con el prompt original."""
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": "Eres un narrador experto en crear historias estructuradas y creativas para los usuarios."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=MAX_TOKENS,
        top_p=1.0
    )

    return completion.choices[0].message.content.strip()


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
            max_tokens=MAX_TOKENS,
            top_p=1.0
        )

        return completion.choices[0].message.content.strip()

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Error de conexión al refinar historia. Intenta nuevamente más tarde.")
    except Exception as e:
        raise RuntimeError(f"Error al refinar historia: {e}")




def contar_palabras(texto: str) -> int:
    """
    Cuenta las palabras en un texto después de limpiarlo:
    - Elimina puntuación (.,!?-)
    - Elimina múltiples espacios
    - Mantiene letras con tildes y ñ
    
    Parámetros:
        texto (str): Texto a analizar.

    Retorna:
        int: Número de palabras limpias en el texto.
    """
    
    texto_limpio = re.sub(r"[.,!?;:\-\"\'()\[\]{}]", "", texto)
    
    texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()
    
    palabras = texto_limpio.split()
    return len(palabras)

    
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
