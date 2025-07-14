import streamlit as st
from creador_de_historias.prompts import construir_prompt
from creador_de_historias.generation import generar_historia

def modo_formulario():
    st.markdown("Completa los parámetros para generar tu historia:")

    with st.form("formulario_historia"):
        col1, col2 = st.columns(2)

        with col1:
            personaje = st.text_input("👤 Nombre del personaje", "Luna")
            rol = st.selectbox("🎭 Rol", ["héroe", "villano", "aliado", "otro"])
            personalidad = st.text_area("🧠 Rasgos de personalidad", "curiosa, valiente, impulsiva")
            relacion = st.text_input("🔗 Relaciones importantes", "su gato parlante")

        with col2:
            escenario = st.text_input("🌍 Ubicación / Época", "castillo encantado en el bosque")
            atmosfera = st.selectbox("🎨 Atmósfera", ["oscura", "alegre", "misteriosa", "épica"])
            genero = st.selectbox("📚 Género", ["fantasía", "misterio", "comedia", "aventura", "terror", "romance"])
            conflicto = st.text_area("⚔️ Tipo de conflicto", "escapar de un hechizo peligroso")

        tono = st.selectbox("🎵 Tono", ["humorístico", "dramático", "oscuro", "caprichoso"])
        longitud = st.selectbox("📏 Longitud", ["corta", "mediana", "larga"])

        with st.expander("🧩 Agregar detalles adicionales"):
            detalles_adicionales = st.text_area(
                "✏️ Detalles adicionales", 
                placeholder="Ej: Quiero que tenga un dragón que hable en rimas..."
            )

        submit = st.form_submit_button("✨ Generar historia")

    if submit:
        data = {
            "personaje": personaje,
            "rol": rol,
            "personalidad": personalidad,
            "relacion": relacion,
            "escenario": escenario,
            "atmósfera": atmosfera,
            "genero": genero,
            "conflicto": conflicto,
            "tono": tono,
            "longitud": longitud,
            "detalles_adicionales": detalles_adicionales
        }

        with st.spinner("🪄 Generando historia..."):
            try:
                prompt = construir_prompt(data)
                historia = generar_historia(prompt)
                st.subheader("📖 Historia Generada")
                st.write(historia)
            except Exception as e:
                st.error(f"❌ Error: {e}")
