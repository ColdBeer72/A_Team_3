import streamlit as st
from inc.basic import *
from inc.config import *
from inc.state_machine import *
from inc.video_stream import VideoProcessor
from streamlit_webrtc import webrtc_streamer

@st.experimental_dialog("Tips de Ayuda")
def tips(postu):
    st.write(f"A destacar en la postura {postu}")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

st.header("Practica Posturas", anchor = False, divider="red")

st.subheader("¡Escoge tu ejercicio!", anchor = False, divider="gray")

secuencia_min = list(TRANSICIONES.keys())
secuencias = secuencia_min + ["Postura concreta"]

seleccion = st.popover("Selecciona tu ejercicio")
secuencia = seleccion.selectbox("Escoja su Secuencia", secuencias, index=len(secuencias)-1)
secuencia_concreta = "_".join(secuencia.split(" ")).lower()
cajavideos = st.empty()
vercaja = False

if secuencia_concreta == "postura_concreta":
    secuencia_concreta = seleccion.selectbox("¿De qué secuencia quieres practicar una postura?", secuencia_min)
    posturas = sublista(TRANSICIONES, secuencia_concreta)
    postura:str = seleccion.select_slider("Escoja su postura a practicar:", posturas)
    secuencia_min = "_".join(secuencia_concreta.split(" ")).lower()
    postura_min = "_".join(postura.split(" ")).lower()
    vercaja = True
    video_path = f"{VIDEO_DIR}/{secuencia_min}/{postura_min}.mp4"
else:
    seleccion.warning("La selección de SECUENCIA todavía no está disponible.")
    # Se añadirá a postoriori
    vercaja = False

muestravid = cajavideos.toggle(label = "Mostrar Vídeo de Muestra", value = False, )

st.divider()

if vercaja:
    cajavideos = st.container(height = 550, border = True)
    if muestravid:
        lcol = 40
        rcol = 60
        col1, col2 = cajavideos.columns(spec = [lcol, rcol], gap = 'small', vertical_alignment = 'top')
        with col1:
            col1.write("VideoDemo")
            col1.video(data = video_path, loop = True, autoplay = True, muted = True)
        with col2:
            col2.write("Aquí irá el Vídeo de WebCam")
    else:
        lcol = 1
        rcol = 99
        col1, col2 = cajavideos.columns(spec = [lcol, rcol], gap = 'small', vertical_alignment = 'top')
        with col2:
            col2.write("Aquí también irá el vídeo de WebCam más grande")

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