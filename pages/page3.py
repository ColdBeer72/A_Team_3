import streamlit as st
from inc.basic import *
from inc.config import *
from inc.state_machine import *
from inc.video_stream import VideoProcessor
from streamlit_webrtc import webrtc_streamer, ClientSettings, WebRtcMode

@st.experimental_dialog("Tips de Ayuda")
def tips(postu):
    st.write(f"A destacar en la postura {postu}")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

st.header("Practica Posturas", anchor = False, divider="red")

# st.subheader("¡Escoge tu ejercicio!", anchor = False, divider="gray")

secuencias_red = list(TRANSICIONES.keys())
secuencias = secuencias_red + ["Postura concreta"]

cajaselect = st.container(height = 160, border = True)
scol1, scol2, scol3, scol4 = cajaselect.columns(spec = [25, 25, 25, 25],
                                gap = 'small', vertical_alignment = 'top')

scol1_seleccion = scol1.popover("Selecciona tu ejercicio")
scol1_secuencia = scol1_seleccion.selectbox("Escoja su Secuencia", secuencias, index=len(secuencias)-1)
scol1_cajavisos = scol1.empty()
scol3_muestravid = scol3.toggle(label = "TIPS / VIDEO MUESTRA", value = False, )
scol3_postura = scol3.empty()
scol4_semaforo = scol4.image(SEM_RED, caption = "MAL",
                             use_column_width="auto")

secuencia_min = "_".join(scol1_secuencia.split(" ")).lower()
cajavideos = st.empty()
vercaja = False
postura = False

if secuencia_min == "postura_concreta":
    secuencia_concreta = scol1_seleccion.selectbox("¿De qué secuencia quieres practicar una postura?", secuencias_red)
    posturas = sublista(TRANSICIONES, secuencia_concreta)
    postura:str = scol1_seleccion.select_slider("Escoja su postura a practicar:", posturas)
    secuencia_min = "_".join(secuencia_concreta.split(" ")).lower()
    postura_min = "_".join(postura.split(" ")).lower()
    vercaja = True
    video_path = f"{VIDEO_DIR}/{secuencia_min}/{postura_min}.mp4"
    scol2.markdown(f"Modalidad: **:orange[POSTURA CONCRETA]**")
else:
    scol1_seleccion.warning("La selección de SECUENCIA todavía no está disponible.")
    # Se añadirá a postoriori
    vercaja = False
    scol2.markdown(f"Modalidad: **:orange[SECUENCIA COMPLETA]**")
    scol2.markdown(f"Secuencia seleccionada: **:blue[{secuencia_concreta}]**")

if postura:
    scol3_postura = scol3.markdown(f"Postura seleccionada: **:red[{postura}]**")
else:
    scol3_postura = scol3.empty()

if vercaja:
    cajavideos = st.container(height = 600, border = True)
    lcol = 15
    rcol = 85
    col1, col2 = cajavideos.columns(spec = [lcol, rcol], gap = 'small', vertical_alignment = 'top')
    if scol3_muestravid:
        col1.write("VideoDemo")
        col1.video(data = video_path, loop = True, autoplay = True, muted = True)
    else:
        col1.write("Aquí vendrán los TIPS") 

    with col2:
        col2.write("Aquí irá el Vídeo de WebCam")
        model_input = Modelos.YOLO
        user_pose = UserPose()
        client_settings = ClientSettings(
                                        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
                                        media_stream_constraints={"video": True, "audio": False}
                                        )
        webrtc_stream = webrtc_streamer(
                            key = "streamer",
                            mode = WebRtcMode.SENDRECV,
                            video_processor_factory = lambda: VideoProcessor(model_input, user_pose),
                            client_settings = client_settings
                            )
        if webrtc_stream.video_processor:
            keypoints = st.session_state.get("keypoints", {})
            user_pose.update_keypoints(keypoints)