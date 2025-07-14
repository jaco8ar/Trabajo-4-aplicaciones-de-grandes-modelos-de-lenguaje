# generation.py

import os
from openai import OpenAI
from dotenv import load_dotenv

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
            retry_prompt = (
                f"La historia anterior fue demasiado larga para el espacio permitido. "
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
