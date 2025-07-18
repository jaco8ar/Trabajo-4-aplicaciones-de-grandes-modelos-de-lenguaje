from openai import OpenAI
from dotenv import load_dotenv
from creador_de_historias.utils import contar_palabras, construir_contexto
import streamlit as st
import requests
import os

load_dotenv()

CLIENT = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

MAX_TOKENS = 2000
MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

LENGTH_MAP = {
    "corta": 400,
    "mediana": 600,
    "larga": 800
}

def llamar_modelo_chat(messages, temperature=0.8, max_tokens=MAX_TOKENS, top_p=1.0):
    """
    Envía una solicitud al modelo de lenguaje con los mensajes dados y devuelve la respuesta.

    Args:
        messages (list): Lista de diccionarios con los mensajes de la conversación (roles: 'user', 'system', 'assistant').
        temperature (float): Nivel de creatividad aleatoria. Valores altos generan salidas más creativas.
        max_tokens (int): Límite máximo de tokens en la respuesta.
        top_p (float): Nucleus sampling (para controlar la diversidad).

    Returns:
        str: Contenido generado por el modelo o un mensaje amigable si ocurre un error.
    """
    try:
        completion = CLIENT.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p
        )
        return completion.choices[0].message.content.strip()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "🚨 El modelo está temporalmente saturado. Por favor, intenta nuevamente en unos minutos."
        else:
            return f"❌ Error HTTP: {e.response.status_code}"

    except requests.exceptions.ConnectionError:
        return "⚠️ No se pudo conectar con el servidor. Verifica tu conexión a internet o inténtalo más tarde."

    except Exception as e:
        return f"❌ Ocurrió un error inesperado: {e}"


def generar_historia(prompt: str, longitud: str = "mediana") -> str:
    """
    Genera una historia basada en un prompt y ajusta su longitud según lo especificado.

    Args:
        prompt (str): Instrucción o descripción para generar la historia.
        longitud (str): Puede ser 'corta', 'mediana' o 'larga'. Define la longitud esperada en palabras.

    Returns:
        str: Historia generada, ajustada a la longitud deseada.
    """
    max_palabras = LENGTH_MAP.get(longitud, LENGTH_MAP["mediana"])
    min_palabras = max_palabras - (200 if longitud != "corta" else 100)

    historia = generar_historia_una_vez(prompt)
    palabras = contar_palabras(historia)

    intentos = 0
    while (palabras < min_palabras or palabras > max_palabras) and intentos < 3:
        razon = "muy corta" if palabras < min_palabras else "muy larga"
        historia = corregir_longitud_historia(historia, prompt, max_palabras, razon)
        palabras = contar_palabras(historia)
        intentos += 1

    return historia


def generar_historia_una_vez(prompt: str) -> str:
    """
    Llama al modelo una sola vez para generar una historia a partir de un prompt.

    Args:
        prompt (str): Instrucción o descripción para crear la historia.

    Returns:
        str: Historia generada por el modelo.
    """
    messages = [
        {"role": "system", "content": "Eres un narrador experto en crear historias estructuradas y creativas para los usuarios."},
        {"role": "user", "content": prompt}
    ]
    return llamar_modelo_chat(messages)


def corregir_longitud_historia(historia: str, prompt: str, max_palabras: int, razon: str) -> str:
    """
    Ajusta la longitud de una historia existente para que se aproxime a un número de palabras objetivo.

    Args:
        historia (str): Historia original generada.
        prompt (str): Prompt original que generó la historia.
        max_palabras (int): Número deseado de palabras.
        razon (str): 'muy corta' o 'muy larga', define si hay que expandir o resumir.

    Returns:
        str: Historia ajustada en longitud.
    """
    if razon == "muy corta":
        instruccion = (
            "La historia anterior es demasiado breve. Reescríbela con una trama más rica, más escenas y profundidad, "
            "agregale más detalles al final, a todo el mundo le gusta un buen final "
            f"sin cambiar su esencia. Apunta a unas {max_palabras} palabras."
        )
    else:
        instruccion = (
            f"La historia anterior es muy extensa. Reescríbela de forma más concisa, resume escenas secundarias y elimina repeticiones, "
            f"para que encaje en unas {max_palabras} palabras."
        )
    instruccion += " Solo debes decir el título de la historia y la historia. Nada de comentarios extra ni entre paréntesis."

    messages = [
        {"role": "system", "content": "Eres un narrador experto en ajustar la longitud de historias sin perder coherencia ni estilo."},
        {"role": "user", "content": instruccion},
        {"role": "assistant", "content": historia}
    ]
    return llamar_modelo_chat(messages)


def refinar_historia(historia_actual: str, sugerencia: str, datos_entrada: dict, modo: str = "formulario") -> str:
    """
    Refina una historia existente con base en una sugerencia del usuario y los datos originales.

    Args:
        historia_actual (str): Historia ya generada que se desea mejorar o modificar.
        sugerencia (str): Comentario o cambio que el usuario desea aplicar.
        datos_entrada (dict): Diccionario con los datos iniciales del usuario (formulario o texto libre).
        modo (str): 'formulario' o 'texto_libre'. Define cómo construir el contexto.

    Returns:
        str: Historia refinada de acuerdo con la sugerencia.
    """
    if modo == "formulario":
        contexto = construir_contexto(datos_entrada)
    else:
        contexto = f"""El usuario inicialmente describió la historia de esta manera:
        \"\"\"{datos_entrada.get('descripcion_libre', '')}\"\"\" 
        Ten esto presente al hacer modificaciones, ya que esta fue la base de la historia."""

    messages = [
        {"role": "system", "content": "Eres un narrador experto en editar y mejorar historias manteniendo coherencia, estilo y estructura."},
        {"role": "user", "content": contexto},
        {"role": "assistant", "content": historia_actual},
        {"role": "user", "content": f"Por favor, modifica la historia anterior siguiendo esta sugerencia:\n{sugerencia}"}
    ]
    return llamar_modelo_chat(messages)
