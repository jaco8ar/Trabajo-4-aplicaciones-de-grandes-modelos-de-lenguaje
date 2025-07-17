from openai import OpenAI
from dotenv import load_dotenv
from creador_de_historias.utils import contar_palabras, construir_contexto
import streamlit as st
import requests


load_dotenv()

CLIENT = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

MAX_TOKENS = 2000

MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

# Asigna tamaño según la longitud deseada palabras
LENGTH_MAP = {
    "corta":    400,    
    "mediana":  600, 
    "larga":    800   
}


def generar_historia(prompt: str, longitud: str = "mediana") -> str:
    """
    Genera una historia y la valida por número de palabras. 
    Si la historia no cumple con el rango esperado, intenta ajustarla hasta 2 veces (máx. 3 intentos en total).

    Parámetros:
        prompt (str): Descripción inicial de la historia.
        longitud (str): Categoría de longitud: 'corta', 'mediana' o 'larga'.

    Retorna:
        str: Historia generada con una longitud adecuada.
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


def corregir_longitud_historia(historia: str, prompt: str, max_palabras: int, razon: str) -> str:
    """
    Corrige la longitud de una historia en caso de ser muy corta o muy larga.

    Parámetros:
        historia (str): Historia original generada.
        prompt (str): Prompt original que generó la historia.
        max_palabras (int): Cantidad máxima deseada de palabras.
        razon (str): 'muy corta' o 'muy larga' para determinar el tipo de corrección.

    Retorna:
        str: Historia ajustada.
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
    
    retry_completion = CLIENT.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Eres un narrador experto en ajustar la longitud de historias sin perder coherencia ni estilo"
                                          " y con una excelente memoria para detalles como nombres y los temas de las historias."},
            {"role": "user", "content": instruccion},
            {"role": "assistant", "content": historia}
        ],
        temperature=0.8,
        max_tokens=MAX_TOKENS,
        top_p=1.0
    )

    return retry_completion.choices[0].message.content.strip()


def generar_historia_una_vez(prompt: str) -> str:
    """
    Genera una historia a partir del prompt proporcionado usando el modelo.

    Parámetros:
        prompt (str): Descripción inicial de la historia.

    Retorna:
        str: Historia generada por el modelo.
    """
    completion = CLIENT.chat.completions.create(
        model=MODEL_NAME,
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
    Refina una historia previamente generada, aplicando una sugerencia del usuario.

    Parámetros:
        historia_actual (str): Texto de la historia actual.
        sugerencia (str): Cambio que el usuario desea aplicar.
        datos_entrada (dict): Información original que generó la historia.
        modo (str): "formulario" o "texto_libre" para definir cómo construir el contexto.

    Retorna:
        str: Historia refinada.
    """
    if modo == "formulario":
        contexto = construir_contexto(datos_entrada)
    else:  # modo texto libre
        contexto = f"""El usuario inicialmente describió la historia de esta manera:
            \"\"\"{datos_entrada.get('descripcion_libre', '')}\"\"\" 
            Ten esto presente al hacer modificaciones, ya que esta fue la base de la historia."""

    try:
        completion = CLIENT.chat.completions.create(
            model=MODEL_NAME,
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


