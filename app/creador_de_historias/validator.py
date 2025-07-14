## Modulo encargado de validar y estructurar las entradas del usuario
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def validar_entrada_libre(texto: str):
    prompt = f"""
        Analiza el siguiente texto del usuario y determina si es una solicitud de historia. 
        Si lo es, extrae los siguientes elementos narrativos si están presentes:
        - Nombre del personaje principal
        - Rol del personaje (héroe, villano, etc.)
        - Género de la historia (fantasía, comedia, etc.)
        - Escenario o ambientación
        - Conflicto central

        Si no es una solicitud de historia no agregues descripciones adicionales unicamente 
        devuelve los datos en formato JSON como este ejemplo:

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

        Texto del usuario:
        \"\"\"{texto}\"\"\"
    """

    try:
        
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=600
        )

        content = response.choices[0].message.content
        
        content = content.replace("```", "").replace("json", "")

        

        data = json.loads(content)

        if not data.get("es_historia", False):
            return False, [], {}

        elementos = data.get("elementos", {})
        requeridos = ["personaje", "rol", "genero", "escenario", "conflicto"]
        faltantes = [key for key in requeridos if not elementos.get(key)]

        return True, faltantes, elementos

    except Exception as e:
        raise RuntimeError(f"❌ Error al validar entrada: {e}")
