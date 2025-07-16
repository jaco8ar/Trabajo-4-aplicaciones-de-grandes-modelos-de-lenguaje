import re

def contar_palabras(texto: str) -> int:
    """
    Cuenta las palabras en un texto después de limpiarlo:
    - Elimina signos de puntuación como comas, puntos, guiones, etc.
    - Elimina múltiples espacios y espacios al inicio/final.
    - Preserva letras con tildes y caracteres especiales como 'ñ'.

    Parámetros:
        texto (str): Texto del cual se quieren contar las palabras.

    Retorna:
        int: Número total de palabras limpias.
    """
    texto_limpio = re.sub(r"[.,!?;:\-\"\'()\[\]{}]", "", texto)
    texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()
    palabras = texto_limpio.split()
    return len(palabras)


def construir_contexto(datos_entrada: dict) -> str:
    """
    Construye un contexto en formato de lista con los datos del formulario,
    para ser usado como parte del prompt que genera o refina la historia.

    Parámetros:
        datos_entrada (dict): Diccionario con los datos del formulario.

    Retorna:
        str: Texto contextual con formato limpio.
    """
    contexto = "Esta es la información base de la historia:\n"
    for clave, valor in datos_entrada.items():
        clave_limpia = clave.replace('_', ' ').capitalize()
        if isinstance(valor, str) and valor.strip() == "":
            valor = "No especificado"
        contexto += f"- {clave_limpia}: {valor}\n"
    return contexto.strip()
