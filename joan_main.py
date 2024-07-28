import streamlit as st
from inc.basic import *
from inc.joan_YOLO_process import process_frame, draw_kp
from inc.state_machine import UserPose
from inc.joan_video_stream import video_stream

def main():
    # Configuración de la página
    st.set_page_config(page_title="DSB10RT Grupo A", layout="wide", initial_sidebar_state="collapsed")

    # Título principal
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Proyecto Final")
    with col2:
        logo_path = "streamlit_sources/hab_logo.png"
        st.image(logo_path, width=100)

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

        postura = st.selectbox("Escoja su postura:", ["Tadasana", "Perro Bocabajo"])

        DEFAULT_WIDTH = 30
        VIDEO_DATA = "data/Raw/01_Tadasana/Figura1_Tadasana_Postura de equilibro.mp4"
        width = st.sidebar.slider(
            label= "Tamaño del Video:",
            min_value=15,
            max_value=50,
            value=DEFAULT_WIDTH,
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
        
        status_text = st.empty()
        FRAME_WINDOW = st.image([])

        if st.session_state['run']:
            st.write("Iniciando captura de video...")
            for frame in video_stream():
                if not st.session_state:
                    st.write("Captura detenida.")
                    break

                keypoints, processed_frame = process_frame(frame)

                # Evaluar la postura utilizando la State Machine
                postura_usuario = UserPose()
                postura_usuario.set_pose(postura)
                postura_usuario.update_keypoints(keypoints)
                if postura == 'Tadasana':
                    postura_usuario.tadasana()
                    
                if postura_usuario.tadasana_state:
                    status_text.success("¡NAMASTE!")
                else: 
                    status_text.warning("Revisa tu alineación")

                FRAME_WINDOW.image(processed_frame)

if __name__ == "__main__":
    main()