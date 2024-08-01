import streamlit as st

# Versión Grupal
from inc.basic import *
from inc.config import *
from inc.joan_YOLO_process import process_frame
from inc.state_machine import UserPose
from inc.joan_video_stream import captura_video
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
            posturas = sublista(TRANSICIONES, "Saludo al sol")
            postura = st.slider("Escoja su postura a practicar:", posturas)
        
        width = st.sidebar.slider(
            label= "Tamaño del Video:",
            min_value=MIN_COLUMN_WIDTH,
            max_value=MAX_COLUMN_WIDTH,
            value=DEFAULT_COLUMN_WIDTH,
            format="%d%%")
        width = max(width, 0.01)
        side = max((100 - width) / 2, 0.01)
        # Creacion de 2 columnas side para centrar el Container del Vid
        _, container, _ = st.columns([side, width, side])
        container.subheader(f"Video ejemplo de la postura {postura}:")
        container.video(data=VIDEO_DATA)

        st.subheader(f"Captura de la postura {postura}:")
        
        # TEST CAPTURA VIDEO
        if 'run' not in st.session_state:
            st.session_state['run'] = False

        # Control de botones
        if not st.session_state['run']:
            if st.button("Iniciar captura de video"):
                st.session_state['run'] = True
        else:
            if st.button("Detener captura de video"):
                st.session_state['run'] = False

        texto_postura_correcta = st.empty()
        FRAME_WINDOW = st.image([])

        if st.session_state['run']:
            st.write("Iniciando captura de video...")
            postura_usuario = UserPose() # Añadir por aqui funcion que pide KPS y los inserta como PARAM.
            for frame in captura_video(camara=user_camara):
                if not st.session_state:
                    st.write("Captura detenida.")
                    break
                keypoints, processed_frame = process_frame(frame)
                # Evaluar la postura utilizando la State Machine
                if secuencia != 'Postura concreta':
                    postura_usuario.set_pose(postura)
                postura_usuario.update_keypoints(keypoints)
                if postura_usuario.postura(postura):
                    texto_postura_correcta.success("¡Bien hecho!")
                else: 
                    texto_postura_correcta.warning("Revisa tu alineación")

                FRAME_WINDOW.image(processed_frame)

if __name__ == "__main__":
    main()