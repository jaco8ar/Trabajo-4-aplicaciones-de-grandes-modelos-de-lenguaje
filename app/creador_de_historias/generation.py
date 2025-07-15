# generation.py

import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Asigna tokens según la longitud deseada
TOKEN_MAP = {
    "corta": 550,     # 400 palabras aprox
    "mediana": 800,   # 600 palabras aprox
    "larga": 1100     # 800 palabras aprox
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
        max_tokens = TOKEN_MAP.get(longitud, 650)

        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un narrador experto en crear historias estructuradas y creativas para los usuarios."},
                {"role": "user", "content": prompt}
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
                f"que encaje en aproximadamente {max_tokens} tokens."

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


def refinar_historia(historia_actual: str, sugerencia: str, datos_entrada: dict) -> str:
    """
    Refina una historia existente con base en una sugerencia del usuario.
    
    Parámetros:
        historia_actual (str): La historia original generada.
        sugerencia (str): Cambios o recomendaciones que el usuario desea aplicar.

    Retorna:
        str: Historia modificada.
    """
    contexto = construir_contexto(datos_entrada)

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un narrador experto en editar y mejorar historias manteniendo coherencia, estilo y estructura."},
                {"role": "user", "content": contexto},
                {"role": "assistant", "content": historia_actual},
                {"role": "user", "content": f"Por favor, modifica la historia anterior siguiendo esta sugerencia:\n{sugerencia}"}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=1.0
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"❌ Error al refinar historia: {e}")
    
def construir_contexto(datos_entrada: dict) -> str:
    contexto = "Esta es la información base de la historia:\n"
    for clave, valor in datos_entrada.items():
        clave_limpia = clave.replace('_', ' ').capitalize()
        if isinstance(valor, str) and valor.strip() == "":
            valor = "No especificado"
        contexto += f"- {clave_limpia}: {valor}\n"
    return contexto.strip()
