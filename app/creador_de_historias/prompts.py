# prompts.py

def prompt_extra_fantasia(data):
    return f"""
    Añade elementos mágicos y criaturas fantásticas. La historia debe desarrollarse en un mundo imaginario donde {data.get('personaje')} interactúa con {data.get('relacion', 'seres místicos')}.
    """

def prompt_extra_misterio(data):
    return f"""
    Desarrolla una trama centrada en un enigma. El personaje principal debe seguir pistas como {data.get('pistas', 'objetos extraños')} para resolver el misterio de {data.get('crimen', 'una desaparición')}.
    """

def prompt_extra_romance(data):
    return f"""
    El eje central debe ser una relación amorosa. Destaca los sentimientos de {data.get('personaje')} hacia {data.get('relacion', 'una persona importante')}, en medio de {data.get('conflicto', 'obstáculos emocionales')}.
    """

def prompt_extra_terror(data):
    return f"""
    Usa una atmósfera inquietante. La amenaza principal, como {data.get('amenaza', 'una figura espectral')}, debe generar tensión psicológica en {data.get('personaje')}.
    """

def prompt_extra_ciencia_ficcion(data):
    return f"""
    Explora ideas futuristas como {data.get('tecnologia', 'inteligencia artificial')} en un entorno como {data.get('ambientacion', 'una colonia espacial')}. Aborda dilemas como {data.get('conflicto_cientifico', 'ética en la clonación')}.
    """

def prompt_extra_comedia(data):
    return f"""
    Usa un estilo humorístico con situaciones absurdas como {data.get('situaciones', 'una boda durante un terremoto')}. El tono debe ser {data.get('estilo_humor', 'paródico')}.
    """

def prompt_extra_aventura(data):
    return f"""
    Enfócate en una misión clara: {data.get('mision', 'explorar ruinas antiguas')}, con aliados como {data.get('aliados', 'un sabio y un ladrón simpático')} y antagonistas como {data.get('enemigos', 'bandidos del desierto')}.
    """

# Diccionario de funciones por género
funciones_genero = {
    "Fantasía": prompt_extra_fantasia,
    "Misterio": prompt_extra_misterio,
    "Romance": prompt_extra_romance,
    "Terror": prompt_extra_terror,
    "Ciencia ficción": prompt_extra_ciencia_ficcion,
    "Comedia": prompt_extra_comedia,
    "Aventura": prompt_extra_aventura
}

# Función principal
def construir_prompt(data):
    genero = data["genero"]
    extra_func = funciones_genero.get(genero)
    prompt_genero = extra_func(data) if extra_func else ""

    prompt_base = f"""
    Escribe una historia de {data['genero']} con tono {data['tono']}.

    Estructura:
    1. Introducción: Presenta al personaje principal, {data['personaje']}, un(a) {data['rol']} con personalidad {data['personalidad']}, en {data['escenario']} con atmósfera {data['atmósfera']}.
    2. Desarrollo: El conflicto central está relacionado con {data['conflicto']}. Describe los desafíos.
    3. Resolución: Explica cómo se resuelve la situación de forma coherente.

    {prompt_genero}

    Longitud deseada: {data['longitud']} palabras.
    Asegúrate de mantener coherencia en la personalidad del personaje y estilo narrativo.
    No incluyas los títulos de Introducción, Desarrollo o Resolución en la historia.
    """.strip()

    return prompt_base
