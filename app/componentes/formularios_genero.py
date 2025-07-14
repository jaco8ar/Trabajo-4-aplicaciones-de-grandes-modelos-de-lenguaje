import streamlit as st

def campos_fantasia():
    raza = st.text_input("🧝 Raza o criatura principal", "elfos del bosque")
    magia = st.text_input("✨ Tipo de magia presente", "hechizos de transformación")
    reino = st.text_input("🏰 Reino o territorio mágico", "Elarion")
    return {"raza": raza, "magia": magia, "reino": reino}

def campos_misterio():
    crimen = st.text_input("🕵️‍♂️ Tipo de crimen o misterio", "una desaparición inexplicable")
    pistas = st.text_area("🔍 Pistas disponibles", "una carta rasgada, un reloj roto")
    investigador = st.text_input("👤 Quién investiga", "una joven periodista curiosa")
    return {"crimen": crimen, "pistas": pistas, "investigador": investigador}

def campos_romance():
    interes_amoroso = st.text_input("💞 Interés amoroso del personaje", "un(a) músico callejero(a)")
    obstaculo = st.text_input("🚧 Obstáculo en la relación", "la desaprobación familiar")
    lugar_encuentro = st.text_input("🌹 Lugar importante para la pareja", "una librería antigua")
    return {"interes_amoroso": interes_amoroso, "obstaculo": obstaculo, "lugar_encuentro": lugar_encuentro}

def campos_terror():
    amenaza = st.text_input("👹 Entidad o amenaza principal", "una criatura del bosque que imita voces")
    lugar_clave = st.text_input("🏚️ Lugar siniestro", "una cabaña abandonada")
    psicologico = st.text_input("🧠 Elemento psicológico", "paranoia, alucinaciones")
    return {"amenaza": amenaza, "lugar_clave": lugar_clave, "psicologico": psicologico}

def campos_ciencia_ficcion():
    tecnologia = st.text_input("🤖 Tecnología destacada", "inteligencia artificial autónoma")
    ambientacion = st.text_input("🌌 Ambientación futurista o espacial", "una colonia en Marte")
    conflicto_cientifico = st.text_input("🧪 Conflicto científico o ético", "la clonación de humanos")
    return {"tecnologia": tecnologia, "ambientacion": ambientacion, "conflicto_cientifico": conflicto_cientifico}

def campos_comedia():
    situaciones = st.text_area("🤣 Situaciones ridículas o absurdas", "una boda en medio de un terremoto")
    estilo_humor = st.selectbox("😜 Estilo de humor", ["absurdo", "sarcasmo", "situacional", "parodia"])
    return {"situaciones": situaciones, "estilo_humor": estilo_humor}

def campos_aventura():
    mision = st.text_input("🗺️ Misión principal", "explorar una isla secreta")
    aliados = st.text_input("🤝 Aliados clave", "un piloto renegado y un robot parlante")
    enemigos = st.text_input("🧟‍♂️ Antagonistas", "piratas del aire")
    return {"mision": mision, "aliados": aliados, "enemigos": enemigos}

# Diccionario exportable para importar por género
funciones_campos_genero = {
    "Fantasía": campos_fantasia,
    "Misterio": campos_misterio,
    "Romance": campos_romance,
    "Terror": campos_terror,
    "Ciencia ficción": campos_ciencia_ficcion,
    "Comedia": campos_comedia,
    "Aventura": campos_aventura
}
