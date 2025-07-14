# generation.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generar_historia(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un narrador experto en crear historias estructuradas y creativas para los usuarios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=800,
            top_p=1.0
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"❌ Error al generar historia con OpenRouter: {e}")
