import streamlit as st
from componentes.modo_formulario import modo_formulario
from componentes.modo_texto_libre import modo_texto_libre

st.set_page_config(page_title="Agente de Historias", layout="centered")
st.title("📝 Agente Creativo de Historias")

modo = st.radio("Selecciona el modo de entrada:", ["📝 Formulario guiado", "🗒️ Texto libre"], horizontal=True)

# --- MODO TEXTO LIBRE ---
if modo == "🗒️ Texto libre":
    modo_texto_libre()

# --- MODO FORMULARIO GUIADO ---
else:
    modo_formulario()