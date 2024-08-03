import streamlit as st
from inc.basic import *
from inc.config import *
from inc.state_machine import *
from inc.video_stream import VideoProcessor
from streamlit_webrtc import webrtc_streamer

st.header("Practica Posturas", anchor = False, divider="red")

st.subheader("Sigue las indicaciones", anchor = False, divider="gray")

secuencias = list(TRANSICIONES.keys()) + ["Postura concreta"]
secuencia = st.selectbox("Escoja su Secuencia", secuencias, index=len(secuencias)-1)
secuencia = "_".join(secuencia.split(" ")).lower()

if secuencia == "postura_concreta":
    secuencia_concreta = st.selectbox("¿De qué secuencia quieres practicar una postura?", secuencias)
    posturas = sublista(TRANSICIONES, secuencia_concreta)
    postura:str = st.select_slider("Escoja su postura a practicar:", posturas)
    postura = "_".join(postura.split(" ")).lower()
else:
    st.warning("La selección de SECUENCIA todavía no está disponible.")
    # Se añadirá a postoriori

video_path = f"{VIDEO_DIR}/{secuencia}/{postura}.mp4"
#############################################################################################
# ACTUALIZACION IN PROGRESS
#############################################################################################

# width = st.sidebar.slider(
#     label= "Tamaño del Video:",
#     min_value=MIN_COLUMN_WIDTH,
#     max_value=MAX_COLUMN_WIDTH,
#     value=DEFAULT_COLUMN_WIDTH,
#     format="%d%%")
# width = max(width, 0.01)
# side = max((100 - width) / 2, 0.01)

# # Creacion de 2 columnas side para centrar el Container del Vid
# _, container, _ = st.columns([side, width, side])
# container.subheader(f"Video ejemplo de la postura {postura}:")
# container.video(data = video_path)

# st.subheader(f"Captura de la postura {postura}:")

# user_pose = UserPose()

# keypoints en > session_state("keypoints")
# keypoints = st.session_state("keypoints") # keypoints es el DICCIONARIO >>> 'nariz': [x, y]

# user_pose.update_keypoints(keypoints)

# model_input = Modelos.YOLO
# webrtc_streamer(key="streamer", video_processor_factory=lambda: VideoProcessor(model_input), sendback_audio=False)