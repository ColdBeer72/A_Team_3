import streamlit as st
from inc.basic import sublista, update_semaforo
from inc.config import *
from inc.state_machine import *
from inc.video_stream import *
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import time

postura = ""
secuencia_concreta = ""

def video_processor_factory(user_pose: type):
    if not postura or not secuencia_concreta:
        st.error("No se ha definido la postura o la secuencia concreta. Asegúrate de que ambos valores estén seleccionados.")
        return None
    model_input = Modelos.YOLO
    user_pose.set_sequence(secuencia_concreta)
    user_pose.set_pose(postura)
    return VideoProcessor(model_input, user_pose)

st.subheader("Practica Posturas", anchor = False, divider="red")

# st.subheader("¡Escoge tu ejercicio!", anchor = False, divider="gray")

secuencias_red = list(TRANSICIONES.keys())
secuencias = secuencias_red + ["Postura concreta"]

cajaselect = st.container(height = 160, border = True)
scol1, scol2, scol3, scol4 = cajaselect.columns(spec=[15, 25, 25, 15],
                                gap='small',
                                vertical_alignment='top'
                                )
scol1_seleccion = scol1.popover("Selecciona tu ejercicio")
scol1_secuencia = scol1_seleccion.selectbox("Escoja su Secuencia",
                                            secuencias,
                                            index=len(secuencias)-1
                                            )
scol1_cajavisos = scol1.empty()
scol3_muestravid = scol3.toggle(label="TIPS / VIDEO MUESTRA",
                                value=False
                                )
scol3_postura = scol3.empty()

secuencia_min = "_".join(scol1_secuencia.split(" ")).lower()
cajavideos = st.empty()
vercaja = False
estado_usuario = False

if secuencia_min == "postura_concreta":
    secuencia_concreta = scol1_seleccion.selectbox("¿De qué secuencia quieres practicar una postura?", secuencias_red)
    posturas = sublista(TRANSICIONES, secuencia_concreta)
    postura:str = scol1_seleccion.select_slider("Escoja su postura a practicar:", posturas)
    secuencia_min = "_".join(secuencia_concreta.split(" ")).lower()
    postura_min = "_".join(postura.split(" ")).lower()
    vercaja = True
    video_path = f"{VIDEO_DIR}/{secuencia_min}/{postura_min}.mp4"
    scol2.markdown(f"Modalidad: **:orange[POSTURA CONCRETA]**")
    scol2.markdown(f"Secuencia seleccionada: **:blue[{secuencia_concreta}]**")
else:
    secuencia_concreta = scol1_seleccion.selectbox("¿De qué secuencia quieres practicar una postura?", secuencias_red)
    scol1_seleccion.warning("La selección de SECUENCIA todavía no está disponible.")
    # Se añadirá a postoriori
    vercaja = False
    scol2.markdown(f"Modalidad: **:orange[SECUENCIA COMPLETA]**")
    scol2.markdown(f"Secuencia seleccionada: **:blue[{secuencia_concreta}]**")
scol3_postura = scol3.markdown(f"Postura seleccionada: **:red[{postura}]**") if postura else scol3.empty()

scol4_semaforo = scol4.empty()
update_semaforo(estado_usuario, scol4_semaforo)

if vercaja:
    cajavideos = st.container(height = 500, border = True)
    lcol = 25
    rcol = 60
    col1, col2 = cajavideos.columns(spec=[lcol, rcol],
                                    gap='small',
                                    vertical_alignment='top'
                                    )
    if scol3_muestravid:
        col1.write("VideoDemo")
        col1.video(data=video_path,
                   loop=True,
                   autoplay=True,
                   muted=True
                   )
    else:
        col1.write("Aquí vendrán los TIPS") 
    with col2:
        user_pose = UserPose(postura, secuencia_concreta)
        video_processor = video_processor_factory(user_pose)
        rtc_configuration = RTCConfiguration({
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        })
        media_stream_constraints = {
            "video": {
                "width": {"ideal": CAM_WIDTH},
                "height": {"ideal": CAM_HEIGHT},
                "frameRate": {"ideal": 20, "max": 40}
            },
            "audio": False
        }
        webrtc_ctx = webrtc_streamer(
            key="streamer",
            mode=WebRtcMode.SENDRECV,
            video_frame_callback=video_processor.recv,
            rtc_configuration=rtc_configuration,
            media_stream_constraints=media_stream_constraints,
            async_processing=True
        )
        falso_frame_count = 0
        # Mientras este el PLAY >>> Hacemos cositas aqui
        st.warning(webrtc_ctx.state.playing)
        st.error(falso_frame_count)
        st.warning(user_pose.actual_state)
        while webrtc_ctx.state.playing:
            keypoints = keypoint_queue.get()
            st.write(f"Últimos keypoints: {video_processor.get_body_dict()}")
            falso_frame_count =+ 1
            st.write(falso_frame_count)
        #     if falso_frame_count == 100:
        #         if falso_frame_count % 10 == 0:
        #             user_pose.update_keypoints(keypoints)
        #             st.write(user_pose.kps)
        #             user_pose.set_pose(postura)
        #             st.write(user_pose.actual_state)
        #             estado_usuario = user_pose.postura()
        #             st.write(estado_usuario)
        #             update_semaforo(estado_usuario, scol4_semaforo)
        #         falso_frame_count = 0
        # else:
        #     video_processor.keypoint_queue.empty()