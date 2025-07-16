import streamlit as st
from creador_de_historias.prompts import construir_prompt
from creador_de_historias.generation import generar_historia, refinar_historia
from componentes.formularios_genero import funciones_campos_genero
from creador_de_historias.validator import evaluar_apto_para_edad

dict_conf_inicial = {
        "personaje": "Anaís",
        "rol": "héroe",
        "personalidad": "inteligente, gruñona, es una niña",
        "relacion": "sus hermanos Gumball y Darwin",
        "escenario": "Elmore",
        "atmósfera": "épica",
        "conflicto": "El evento más aleatorio le acaba de suceder a tus hermanos y ahora debes arreglar su desastre",
        "edad": "adolescente",
        "tono": "humorístico",
        "longitud": "mediana",
        "detalles_adicionales": ""
    }

# Configuraciones por defecto
CONFIGURACIONES_DEFECTO = {
    "defecto": dict_conf_inicial,
    "favorita": dict_conf_inicial
}


def inicializar_configuraciones():
    """Inicializa las configuraciones en session_state si no existen."""
    if "configuraciones" not in st.session_state:
        st.session_state["configuraciones"] = CONFIGURACIONES_DEFECTO.copy()


def cargar_configuracion_favorita():
    """Carga la configuración favorita en session_state para usar en el formulario."""
    st.session_state["usar_favorita"] = True
    st.toast("⭐ Configuración favorita cargada", icon="✅")


def obtener_valores_formulario(genero: str, usar_favorita: bool = False) -> dict:
    """
    Obtiene los valores a usar en el formulario basándose en la configuración seleccionada.
    
    Args:
        genero (str): Género seleccionado
        usar_favorita (bool): Si usar la configuración favorita
        
    Returns:
        dict: Valores para el formulario
    """
    config_tipo = "favorita" if usar_favorita else "defecto"
    valores = st.session_state["configuraciones"][config_tipo].copy()
    valores["genero"] = genero
    return valores


def guardar_configuracion_favorita(data: dict):
    """
    Guarda la configuración actual como favorita.
    
    Args:
        data (dict): Datos del formulario a guardar
    """
    # Solo guardamos los campos comunes (antes de los campos específicos de género)
    campos_comunes = [
        "personaje", "rol", "personalidad", "relacion", "escenario", 
        "atmósfera", "conflicto", "tono", "longitud", "detalles_adicionales"
    ]
    
    nueva_favorita = {}
    for campo in campos_comunes:
        if campo in data:
            nueva_favorita[campo] = data[campo]
    
    st.session_state["configuraciones"]["favorita"] = nueva_favorita
    st.success("⭐ Configuración guardada como favorita")


def modo_formulario():
    """
    Controla el flujo del modo de entrada por formulario.

    Renderiza los formularios, recoge datos del usuario, genera la historia 
    y permite refinarla con sugerencias.
    """
    # Inicializar configuraciones
    inicializar_configuraciones()
    
    st.markdown("Completa los parámetros para generar tu historia:")
    
    # Fila con selector de género y botón de configuración favorita
    col_genero, col_favorita = st.columns([3, 1])
    
    with col_genero:
        genero = st.selectbox(
            "📚 Género",
            ["Fantasía", "Misterio", "Romance", "Terror", "Ciencia ficción", "Comedia", "Aventura"]
        )
    
    with col_favorita:
        st.markdown("<br>", unsafe_allow_html=True)  # Espaciado para alineación
        if st.button("⭐ Favoritos"):
            cargar_configuracion_favorita()

    # Verificar si se debe usar la configuración favorita
    usar_favorita = st.session_state.get("usar_favorita", False)
    
    data = construir_formulario_principal(genero, usar_favorita)

    if data:
        st.session_state["historia_datos"] = data
        with st.spinner("🪄 Generando historia..."):
            try:
                prompt = construir_prompt(data)
                historia = generar_historia(prompt, data["longitud"])
                apta, comentario = evaluar_apto_para_edad(historia, data["edad"])
                if not apta:
                    st.warning(f"La historia podría no ser apropiada para {data['rango_edad']}: {comentario}")

                st.session_state["historia_generada"] = historia
                st.subheader("📖 Historia Generada")
                st.write(historia)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    mostrar_bloque_refinamiento()


def construir_formulario_principal(genero: str, usar_favorita: bool = False) -> dict | None:
    """
    Construye y muestra el formulario principal para capturar los datos de la historia.

    Parámetros:
        genero (str): Género narrativo seleccionado por el usuario.
        usar_favorita (bool): Si usar los valores de la configuración favorita.

    Retorna:
        dict | None: Diccionario con los datos del usuario si se envía el formulario, de lo contrario None.
    """
    # Obtener valores base según configuración
    valores_base = obtener_valores_formulario(genero, usar_favorita)
    
    with st.form("formulario_historia"):
        data = {"genero": genero}
        col1, col2 = st.columns(2)

        with col1:
            data["personaje"] = st.text_input(
                "👤 Nombre del personaje", 
                value=valores_base.get("personaje", "Luna")
            )
            data["rol"] = st.selectbox(
                "🎭 Rol", 
                ["héroe", "villano", "aliado", "otro"],
                index=["héroe", "villano", "aliado", "otro"].index(valores_base.get("rol", "héroe"))
            )
            data["personalidad"] = st.text_area(
                "🧠 Rasgos de personalidad", 
                value=valores_base.get("personalidad", "curiosa, valiente, impulsiva")
            )
            data["relacion"] = st.text_input(
                "🔗 Relaciones importantes", 
                value=valores_base.get("relacion", "su gato parlante")
            )

        with col2:
            data["escenario"] = st.text_input(
                "🌍 Ubicación / Época", 
                value=valores_base.get("escenario", "castillo encantado en el bosque")
            )
            data["atmósfera"] = st.selectbox(
                "🎨 Atmósfera", 
                ["oscura", "alegre", "misteriosa", "épica"],
                index=["oscura", "alegre", "misteriosa", "épica"].index(valores_base.get("atmósfera", "misteriosa"))
            )
            data["conflicto"] = st.text_area(
                "⚔️ Tipo de conflicto", 
                value=valores_base.get("conflicto", "escapar de un hechizo peligroso")
            )
            data["edad"] = st.selectbox(
                "👶 Edad del público", 
                ["infantil", "adolescente", "adulto"],
                index=["infantil", "adolescente", "adulto"].index(valores_base.get("edad", "infantil"))
            )
            

        data["tono"] = st.selectbox(
            "🎵 Tono", 
            ["humorístico", "dramático", "oscuro", "caprichoso"],
            index=["humorístico", "dramático", "oscuro", "caprichoso"].index(valores_base.get("tono", "humorístico"))
        )
        data["longitud"] = st.selectbox(
            "📏 Longitud", 
            ["corta", "mediana", "larga"],
            index=["corta", "mediana", "larga"].index(valores_base.get("longitud", "corta"))
        )

        st.markdown(f"Completa estas preguntas para que tu historia de {genero.lower()} sea mejor")

        # Campos adicionales por género
        campos_func = funciones_campos_genero.get(genero)
        if campos_func:
            data.update(campos_func())

        with st.expander("🧩 Agregar detalles adicionales"):
            data["detalles_adicionales"] = st.text_area(
                "✏️ Detalles adicionales",
                value=valores_base.get("detalles_adicionales", ""),
                placeholder="Ej: Quiero que tenga un dragón que hable en rimas..."
            )

        # Botones del formulario
        col_generar, col_guardar = st.columns([2, 1])
        
        with col_generar:
            submit = st.form_submit_button("✨ Generar historia")
        
        with col_guardar:
            guardar_favorita = st.form_submit_button("⭐ Guardar como favorita")
        
        # Procesar acciones
        if guardar_favorita:
            guardar_configuracion_favorita(data)
            
        # Limpiar flag de usar favorita después de usar
        if st.session_state.get("usar_favorita", False):
            st.session_state["usar_favorita"] = False
            
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