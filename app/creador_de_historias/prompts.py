def construir_prompt(data):
    return f"""
Escribe una historia de {data['genero']} con tono {data['tono']}.
Estructura:

1. Introducción: Presenta al personaje principal, {data['personaje']}, un(a) {data['rol']} con personalidad {data['personalidad']}, en {data['escenario']} con atmósfera {data['atmósfera']}.
2. Desarrollo: El conflicto central está relacionado con {data['conflicto']}. Describe los desafíos.
3. Resolución: Explica cómo se resuelve la situación de forma coherente.

Longitud deseada: {data['longitud']} palabras.
Asegúrate de mantener coherencia en la personalidad del personaje y estilo narrativo.

La historia generada no debe tener los titulos de Introducción, Desarrollo y Resolución
"""
