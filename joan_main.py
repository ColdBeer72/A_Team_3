import streamlit as st

# Versión Grupal
from inc.basic import *
from inc.config import *
from inc.joan_video_stream import *
from inc.manu_manage_cameras import *

def main():
    # Configuración de la página
    st.set_page_config(page_title=PAGE_TITLE, layout="wide", initial_sidebar_state="collapsed")

    # Título principal
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(PROYECT_TITLE)
    with col2:
        st.image(LOGO_PATH, width=100)

    # Barra lateral con submenús
    st.sidebar.title("Corrige tu Postura de Yoga")
    menu = st.sidebar.radio(
        "¿Qué quieres visitar?:",
        ("Presentación del Proyecto", "Presentación del Estudio", "Desarrollo del Estudio")
    )

    # 1. Presentación del Proyecto
    if menu == "Presentación del Proyecto":
        st.header("Presentación del Proyecto")
        st.subheader("Proyecto de:")
        autores()

    # 2. Presentación del Estudio
    elif menu == "Presentación del Estudio":
        st.header("Presentación del Estudio")
        md_presentation = "streamlit_sources/presentation.md"
        txt_presentation = read_markdown_file(md_presentation)
        st.markdown(txt_presentation)

    # 3. Desarrollo del Estudio
    elif menu == "Desarrollo del Estudio":
        st.title("Practica Posturas")
        lista_camaras = select_camera()
        user_camara = int(st.selectbox(
            "Escoja la cámara con la que capturar:",
            lista_camaras,
            index=0,
            placeholder="Escoja una cámara"
        ))
        
        secuencias = list(TRANSICIONES.keys()) + ["Postura concreta"]
        secuencia = st.selectbox("Escoja su Secuencia", secuencias)

        if secuencia == "Postura concreta":
            subsecuencia = st.selectbox("Escoja secuencia para seleccionar postura concreta:", list(TRANSICIONES.keys()))
            posturas = sublista(TRANSICIONES, subsecuencia)
            postura = st.selectbox("Escoja su postura a practicar:", posturas)
            func_video(secuencia, postura, user_camara)
        else:
            st.warning("La selección de SECUENCIA todavía no está disponible.")
            # Se añadirá a postoriori

if __name__ == "__main__":
    main()