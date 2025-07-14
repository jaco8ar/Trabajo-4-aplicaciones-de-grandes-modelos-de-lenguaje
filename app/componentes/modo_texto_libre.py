import streamlit as st
from creador_de_historias.validator import validar_entrada_libre
from creador_de_historias.generation import generar_historia

def modo_texto_libre():
    descripcion_libre = st.text_area("Describe la historia que quieres leer", height=300)

    if st.button("✨ Validar descripción"):
        valido, faltantes, elementos = validar_entrada_libre(descripcion_libre)
        st.session_state["texto_valido"] = valido
        st.session_state["faltantes"] = faltantes
        st.session_state["descripcion_libre"] = descripcion_libre

    if "texto_valido" in st.session_state:
        if not st.session_state["texto_valido"]:
            st.warning("Parece que tu texto no es una solicitud clara de historia. Intenta describir mejor lo que quieres.")
        elif st.session_state["faltantes"]:
            st.warning(
                f"Faltan elementos clave: {', '.join(st.session_state['faltantes'])}. "
                "Puedes agregarlos o generar la historia de todas formas."
            )
            if st.button("👉 Generar de todas formas"):
                mostrar_historia()
        else:
            mostrar_historia()

def mostrar_historia():
    with st.spinner("🪄 Generando historia..."):
        try:
            historia = generar_historia(st.session_state["descripcion_libre"])
            st.subheader("📖 Historia Generada")
            st.write(historia)
        except Exception as e:
            st.error(f"❌ Error: {e}")
