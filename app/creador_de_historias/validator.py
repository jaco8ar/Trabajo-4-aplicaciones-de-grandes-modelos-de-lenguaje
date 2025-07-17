## Modulo encargado de validar y estructurar las entradas del usuario
import os
from openai import OpenAI
from dotenv import load_dotenv
from creador_de_historias.generation import CLIENT
import json

load_dotenv()
MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

def validar_entrada_libre(texto: str, intentos_max: int = 2):
    """
    Valida si un texto dado es una solicitud de historia y extrae los elementos narrativos clave.

    En caso de que el modelo devuelva una salida no válida o mal estructurada, se intenta nuevamente
    hasta un número máximo de reintentos.

    Parámetros:
        texto (str): Entrada libre proporcionada por el usuario.
        intentos_max (int): Número máximo de intentos para obtener una respuesta válida del modelo.

    Retorna:
        tuple:
            - bool: True si es una solicitud de historia, False en caso contrario.
            - list[str]: Lista de campos faltantes entre los elementos requeridos.
            - dict: Diccionario con los elementos extraídos por el modelo (puede contener campos vacíos).

    Excepciones:
        RuntimeError: Si todos los intentos fallan en producir una salida válida.
    """
    prompt = f"""
        Analiza el siguiente texto del usuario y determina si es una solicitud de historia. 
        Si lo es, extrae los siguientes elementos narrativos si están presentes:
        - Nombre del personaje principal
        - Rol del personaje (héroe, villano, etc.)
        - Género de la historia (fantasía, comedia, etc.)
        - Escenario o ambientación
        - Conflicto central

        Devuelve los datos en formato JSON como este ejemplo:

        {{
        "es_historia": true,
        "elementos": {{
            "personaje": "Luna",
            "rol": "héroe",
            "genero": "fantasía",
            "escenario": "castillo encantado en el bosque",
            "conflicto": "escapar de un hechizo"
        }}
        }}

        Si no te dan los datos textualmente no los infieras y deja el campo vacío. 
        Tampoco crees información que no te dan.
        Texto del usuario:
        \"\"\"{texto}\"\"\"
    """

    for intento in range(1, intentos_max + 1):
        try:
            response = CLIENT.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=600
            )

            content = response.choices[0].message.content
            content = content.replace("```", "").replace("json", "").strip()

            # Intentar decodificar JSON
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                if intento == intentos_max:
                    raise RuntimeError("❌ El modelo devolvió un formato inválido tras varios intentos.")
                continue  # intentar de nuevo

            # Verificar estructura esperada
            if not isinstance(data, dict) or "es_historia" not in data:
                if intento == intentos_max:
                    raise RuntimeError(f"❌ La respuesta del modelo no contiene el campo 'es_historia'. Última respuesta: {data}")
                continue

            if not data.get("es_historia", False):
                return False, [], {}

            elementos = data.get("elementos", {})
            requeridos = ["personaje", "rol", "genero", "escenario", "conflicto"]
            faltantes = [key for key in requeridos if not elementos.get(key)]

            return True, faltantes, elementos

        except Exception as e:
            if intento == intentos_max:
                raise RuntimeError(f"❌ Error persistente al validar entrada: {e}")
            continue  # intenta de nuevo

def evaluar_apto_para_edad(historia: str, rango_edad: str) -> tuple[bool, str]:
    """
    Evalúa si una historia es apta para un determinado rango de edad usando un modelo LLM.

    Parámetros:
        historia (str): Historia generada previamente.
        rango_edad (str): Uno de: "infantil", "adolescente", "adulto".

    Retorna:
        tuple:
            - bool: True si la historia es apta, False si no.
            - str: Justificación o comentario del modelo.
    """

    if rango_edad == "adulto":
        return True, "Sin comentario del modelo"
    instrucciones = {
        "infantil": "Evalúa si la historia es apta para niños. Debe estar libre de violencia explícita, lenguaje inapropiado, terror intenso, temas sensibles o ningun tipo de contenido sexual.",
        "adolescente": "Evalúa si la historia es apta para adolescentes. Puede tener cierto conflicto, pero sin lenguaje ofensivo, contenido sexual explícito ni violencia extrema."
    }

    prompt = f"""
    {instrucciones[rango_edad]}

    Analiza esta historia:
    \"\"\"{historia}\"\"\"

    Responde con el siguiente formato JSON:

    {{
        "apto": true,
        "comentario": "Breve justificación del juicio"
    }}
    """

    try:
        response = CLIENT.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=400
        )

        content = response.choices[0].message.content
        content = content.replace("```", "").replace("json", "").strip()
        data = json.loads(content)

        return data.get("apto", False), data.get("comentario", "Sin comentario del modelo")

    except Exception as e:
        raise RuntimeError(f"Error al evaluar la historia para rango de edad: {e}")
