import streamlit as st
from creador_de_historias.prompts import construir_prompt
from creador_de_historias.generation import generar_historia, refinar_historia
from componentes.formularios_genero import funciones_campos_genero


def modo_formulario():
    """
    Controla el flujo del modo de entrada por formulario.

    Renderiza los formularios, recoge datos del usuario, genera la historia 
    y permite refinarla con sugerencias.
    """
    st.markdown("Completa los parámetros para generar tu historia:")
    genero = st.selectbox(
        "📚 Género",
        ["Fantasía", "Misterio", "Romance", "Terror", "Ciencia ficción", "Comedia", "Aventura"]
    )

    data = construir_formulario_principal(genero)

    if data:
        st.session_state["historia_datos"] = data
        with st.spinner("🪄 Generando historia..."):
            try:
                prompt = construir_prompt(data)
                historia = generar_historia(prompt, data["longitud"])
                st.session_state["historia_generada"] = historia
                st.subheader("📖 Historia Generada")
                st.write(historia)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    mostrar_bloque_refinamiento()


def construir_formulario_principal(genero: str) -> dict | None:
    """
    Construye y muestra el formulario principal para capturar los datos de la historia.

    Parámetros:
        genero (str): Género narrativo seleccionado por el usuario.

    Retorna:
        dict | None: Diccionario con los datos del usuario si se envía el formulario, de lo contrario None.
    """
    with st.form("formulario_historia"):
        data = {"genero": genero}
        col1, col2 = st.columns(2)

        with col1:
            data["personaje"] = st.text_input("👤 Nombre del personaje", "Luna")
            data["rol"] = st.selectbox("🎭 Rol", ["héroe", "villano", "aliado", "otro"])
            data["personalidad"] = st.text_area("🧠 Rasgos de personalidad", "curiosa, valiente, impulsiva")
            data["relacion"] = st.text_input("🔗 Relaciones importantes", "su gato parlante")

        with col2:
            data["escenario"] = st.text_input("🌍 Ubicación / Época", "castillo encantado en el bosque")
            data["atmósfera"] = st.selectbox("🎨 Atmósfera", ["oscura", "alegre", "misteriosa", "épica"])
            data["conflicto"] = st.text_area("⚔️ Tipo de conflicto", "escapar de un hechizo peligroso")

        data["tono"] = st.selectbox("🎵 Tono", ["humorístico", "dramático", "oscuro", "caprichoso"])
        data["longitud"] = st.selectbox("📏 Longitud", ["corta", "mediana", "larga"])

        st.markdown(f"Completa estas preguntas para que tu historia de {genero.lower()} sea mejor")

        # Campos adicionales por género
        campos_func = funciones_campos_genero.get(genero)
        if campos_func:
            data.update(campos_func())

        with st.expander("🧩 Agregar detalles adicionales"):
            data["detalles_adicionales"] = st.text_area(
                "✏️ Detalles adicionales",
                placeholder="Ej: Quiero que tenga un dragón que hable en rimas..."
            )

        submit = st.form_submit_button("✨ Generar historia")
        return data if submit else None


def mostrar_bloque_refinamiento():
    """
    Muestra el formulario de refinamiento de la historia si ya fue generada.

    Permite al usuario introducir una sugerencia de cambio, la cual se envía al modelo
    junto con la historia original y los datos de entrada.
    """
    if "historia_generada" not in st.session_state:
        return

    st.subheader("✏️ ¿Quieres hacer ajustes?")
    with st.form("formulario_refinar"):
        sugerencia = st.text_area("Describe los cambios que deseas hacer a la historia", height=150)
        refinar = st.form_submit_button("🔁 Refinar historia")

        if refinar and sugerencia.strip():
            with st.spinner("🔄 Refinando historia..."):
                datos = st.session_state["historia_datos"]
                datos.setdefault("sugerencias", []).append(sugerencia)
                historia_refinada = refinar_historia(
                    st.session_state["historia_generada"],
                    sugerencia,
                    datos
                )
                st.session_state["historia_generada"] = historia_refinada
                st.subheader("📖 Historia Refinada")
                st.write(historia_refinada)
