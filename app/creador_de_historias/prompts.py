from creador_de_historias.generation import LENGTH_MAP

def prompt_extra_fantasia(data):
    return f"""
    Desarrolla una historia de fantasía ambientada en el reino mágico de {data.get('reino')}, gobernado por un sistema de {data.get('politica')}. 
    Los protagonistas son {data.get('raza')}, que dominan {data.get('magia')}. 
    La trama debe incluir una misión épica, obstáculos sobrenaturales y criaturas fantásticas. 
    Usa un tono de aventura y maravilla para capturar la esencia del género.
    """

def prompt_extra_misterio(data):
    return f"""
    Construye un relato de misterio centrado en {data.get('crimen')}, investigado por {data.get('investigador')}. 
    Introduce pistas como {data.get('pistas')} que lleven progresivamente a la verdad oculta. 
    El desarrollo debe generar suspenso y concluir con un giro dramático: {data.get('plot')}. 
    Mantén el tono enigmático y juega con las sospechas del lector.
    """

def prompt_extra_romance(data):
    return f"""
    El núcleo de la historia debe ser el vínculo romántico entre el personaje principal y {data.get('interes_amoroso')}. 
    La relación debe enfrentarse a obstáculos como {data.get('obstaculo')}, con momentos significativos en {data.get('lugar_encuentro')}. 
    {data.get('sidekick')} debe acompañar o intervenir para apoyar al protagonista. 
    El tono debe ser emocional, íntimo y centrado en el desarrollo del amor.
    """


def prompt_extra_terror(data):
    return f"""
    Desarrolla una historia de terror con un enfoque en el subgénero {data.get('tipo_terror')}. 
    La amenaza principal es {data.get('amenaza')}, que se manifiesta en {data.get('lugar_clave')}. 
    Explora elementos psicológicos como {data.get('psicologico')} y juega con la fobia del protagonista: {data.get('fobia')}. 
    Mantén la tensión creciente y el final inquietante.
    """


def prompt_extra_ciencia_ficcion(data):
    return f"""
    Desarrolla una historia de ciencia ficción ambientada en {data.get('ambientacion')}, donde la tecnología clave es {data.get('tecnologia')}. 
    El conflicto gira en torno a {data.get('conflicto_cientifico')} y la historia debe mostrar una visión del futuro tipo {data.get('vision')}. 
    Integra dilemas éticos y avances tecnológicos con un tono reflexivo y especulativo.
    """


def prompt_extra_comedia(data):
    return f"""
    La historia debe ser una comedia basada en situaciones absurdas como {data.get('situaciones')}. 
    Utiliza el estilo de humor {data.get('estilo_humor')} dentro del subgénero {data.get('tipo_comedia')}. 
    Haz referencia a elementos conocidos como {data.get('referencia')} para añadir ironía o parodia. 
    El ritmo debe ser ágil y generar risa mediante malentendidos, exageración o sorpresas cómicas.
    """


def prompt_extra_aventura(data):
    return f"""
    Cuenta una historia de aventura con una misión principal: {data.get('mision')}. 
    El protagonista se une con aliados como {data.get('aliados')} y enfrenta antagonistas como {data.get('enemigos')}. 
    La historia debe encajar en el subgénero de aventura: {data.get('sub')}, con ritmo rápido, obstáculos físicos y crecimiento del personaje. 
    Usa escenarios exóticos y desafíos constantes.
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
    
    Debe haber cohesión entre el genero, {data['escenario']}y {data['atmósfera']}
    Estructura:
    1. Introducción: Presenta al personaje principal, {data['personaje']}, un(a) {data['rol']} con personalidad {data['personalidad']}, en {data['escenario']} con atmósfera {data['atmósfera']}.
    2. Desarrollo: El conflicto central está relacionado con {data['conflicto']}. Describe los desafíos.
    3. Resolución: Explica cómo se resuelve la situación de forma coherente.

    Debes construir la historia basandote en las siguientes indicaciones para el genero:

    {prompt_genero}

    Longitud deseada: {LENGTH_MAP[data['longitud']]} palabras.
    Asegúrate de mantener coherencia en la personalidad del personaje y estilo narrativo.
    No incluyas los títulos de Introducción, Desarrollo o Resolución en la historia.
    Los detalles adicionales {data['detalles_adicionales']} son importantes para la historia pero deben ser coherentes y no deben contradecir la estructura ya existente de la misma.
    """.strip()

    edad_prompt = ""
    if data["edad"] == "infantil":
        edad_prompt = "Asegúrate de que la historia sea completamente apta para niños (sin violencia explícita, lenguaje inapropiado o temas sensibles)."
    elif data["edad"] == "adolescente":
        edad_prompt = "Asegúrate de que la historia sea apta para adolescentes, evitando contenido sexual, violencia extrema o lenguaje ofensivo."
    elif data["edad"] == "adulto":
        edad_prompt = "No necesitas aplicar restricciones especiales de contenido."


    return prompt_base + edad_prompt
