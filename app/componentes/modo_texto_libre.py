import streamlit as st
from creador_de_historias.validator import validar_entrada_libre, evaluar_apto_para_edad
from creador_de_historias.generation import generar_historia, refinar_historia
from componentes.modo_formulario import guardar_historia_en_PDF

import requests


def modo_texto_libre():
    """
    Renderiza el modo de entrada por texto libre en la app.

    Permite al usuario describir libremente la historia que desea. 
    La entrada se valida automáticamente para extraer elementos clave 
    y sugerir mejoras antes de generar o refinar la historia.
    """
    descripcion = st.text_area("Describe la historia que quieres leer", height=300)

    if st.button("✨ Validar descripción"):
        with st.spinner("Validando..."):
            valido, faltantes, elementos = validar_entrada_libre(descripcion)

        st.session_state.update({
            "texto_valido": valido,
            "elementos": elementos,
            "faltantes": faltantes,
            "descripcion_libre": descripcion
        })

    manejar_resultado_validacion()
    mostrar_bloque_refinamiento()
    guardar_historia_en_PDF(modo = "libre")


def manejar_resultado_validacion():
    """
    Maneja el resultado de la validación del texto libre.

    Si el texto es inválido, muestra advertencias. Si es válido, permite generar la historia.
    También permite al usuario generar la historia aún si faltan elementos clave.
    """
    if "texto_valido" not in st.session_state:
        return

    if not st.session_state["texto_valido"]:
        st.warning("Parece que tu texto no es una solicitud clara de historia. Intenta describir mejor lo que quieres.")
    elif st.session_state["faltantes"]:
        st.warning(
            f"Faltan elementos clave: {', '.join(st.session_state['faltantes'])}. "
            "Puedes agregarlos o generar la historia de todas formas. Si no los agregas estos serán llenados automáticamente."
        )
        if st.button("👉 Generar de todas formas"):
            generar_y_mostrar_historia()
    else:
        generar_y_mostrar_historia()


def generar_y_mostrar_historia():
    """
    Genera una historia a partir del texto libre validado y la muestra al usuario.

    Guarda la historia original y la versión generada en el estado de sesión.
    Maneja errores de conexión y fallos generales de generación.
    """
    with st.spinner("🪄 Generando historia..."):
        try:
            prompt = st.session_state["descripcion_libre"] 
            prompt += "Solo debes decir el titulo de la historia y la historia nada de comentarios extra o entre parentesis."
            historia = generar_historia(prompt)

            if "historia_original" not in st.session_state:
                st.session_state["historia_original"] = historia

            st.session_state["historia_generada"] = historia
            st.subheader("📖 Historia Generada")
            st.write(historia)

        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión: no se pudo contactar con el servidor. Verifica tu conexión.")
        except Exception as e:
            st.error(f"❌ Error: {e}")


def mostrar_bloque_refinamiento():
    """
    Muestra el formulario para refinar la historia ya generada en modo texto libre.

    Permite al usuario sugerir cambios que serán aplicados por el LLM,
    manteniendo el contexto original del texto libre.
    """
    if st.session_state.get("historia_generada"):
        st.subheader("✏️ ¿Quieres hacer ajustes?")
        with st.form("formulario_refinar"):
            sugerencia = st.text_area("Describe los cambios que deseas hacer a la historia", height=150)
            refinar = st.form_submit_button("🔁 Refinar historia")

            if refinar and sugerencia.strip():
                with st.spinner("🔄 Refinando historia..."):
                    historia_refinada = refinar_historia(
                        st.session_state["historia_generada"],
                        sugerencia,
                        {"descripcion_libre": st.session_state.get("descripcion_libre", "")},
                        modo="texto_libre"
                    )
                    st.session_state["historia_generada"] = historia_refinada
                    st.subheader("📖 Historia Refinada")
                    st.write(historia_refinada)
                    apta, comentario = evaluar_apto_para_edad(st.session_state["historia_generada"], "infantil")
                    if not apta:
                        st.warning(f"La historia podría no ser apropiada para niños: {comentario}")
