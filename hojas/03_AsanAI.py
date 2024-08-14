import streamlit as st
#from inc.basic import sublista, update_semaforo
from inc.basic import *
from inc.config import *
from inc.state_machine import *
from inc.video_stream import VideoProcessor, keypoint_queue
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

# Header de la página
st.subheader("Practica Posturas", anchor = False, divider="red")

# Caja superior con selector de Ejercicio
# Creación de la caja contenedor
cajaselect = st.container(height = 110, border = True)
# Variables de sección
postura = ""
secuencia_concreta = ""
scol2_text = ""
progress_text = "Postura detectada, un momento..."
posturas = []
step = 0
frame_count = 0
frame_success = 0
secuencias_red = list(TRANSICIONESTIPS.keys())
secuencias = secuencias_red + ["Postura concreta"]
# Creación de columnas
scol1, scol2, scol3, scol4 = cajaselect.columns(
        spec=[20, 45, 30, 5],
        gap='small',
        vertical_alignment='top'
    )
# Popover para seleccionar ejercicio en COL1
scol1_seleccion = scol1.popover("Selecciona tu ejercicio")
scol1_secuencia = scol1_seleccion.selectbox(
        "Escoja su Secuencia",
        secuencias,
        index=len(secuencias)-1
    )
secuencia_min = "_".join(scol1_secuencia.split(" ")).lower()

scol1_cajavisos = scol1.empty()
scol2_modsec = scol2.empty()
scol3_scroll = scol3.empty()
cajavideos = st.empty()
vercaja = False

if secuencia_min == "postura_concreta":
    secuencia_concreta = scol1_seleccion.selectbox("¿De qué secuencia quieres practicar una postura?", secuencias_red)
    posturas = sublista(TRANSICIONESTIPS, secuencia_concreta)
    postura:str = scol1_seleccion.select_slider("Escoja su postura a practicar:", posturas)
    secuencia_min = "_".join(secuencia_concreta.split(" ")).lower()
    postura_min = "_".join(postura.split(" ")).lower()
    vercaja = True
    video_path = f"{VIDEO_DIR}/{secuencia_min}/{postura_min}.mp4"
    scol2_text = f'''
                    Modalidad: **:orange[POSTURA CONCRETA]**<br>
                    Secuencia seleccionada: **:blue[{secuencia_concreta}]**<br>
                    Postura seleccionada: **:red[{postura}]**
                    '''
else:
    sequence = scol1_secuencia
    posturas_sequence = TRANSICIONES_SECUENCIA[sequence]
    posturas = list(posturas_sequence.values())
    pose_actual = posturas[step]
    vercaja = True
    video_path = f"{VIDEO_DIR}/{secuencia_min}/{pose_actual}.mp4"
    scol2_text = f'''
                    Modalidad: **:orange[SECUENCIA]**<br>
                    Secuencia seleccionada: **:blue[{sequence}]**<br>
                    Postura actual: **:red[{pose_actual}]**
                    '''

scol2_modsec.markdown(scol2_text, unsafe_allow_html=True)

scol3_bar = scol3.progress(0, text=progress_text)
# scol3_bar = scol3.button("Activa")
scol3.button("Activa")

scol4_semaforo = scol4.empty()
estado_usuario = False
update_semaforo(estado_usuario, scol4_semaforo)

# Caja
if vercaja:
    cajavideos = st.container(height = 650, border = True)
    lcol = 20
    w1 = 25
    rcol = 45
    w2 = 10
    col1, _, col2, _ = cajavideos.columns(spec=[lcol, w1, rcol, w2],
                                    gap='small',
                                    vertical_alignment='top'
                                    )
    col1_kps = col1.toggle(
        "Ver KeyPoints",
        value=True
        )
    col1_muestravid = col1.toggle(
        label="TIPS / VIDEO MUESTRA",
        value=False
    )
    videotip = col1.container(height=None, border= False)

    if col1_muestravid:
        videotip.video(data=video_path,
                   loop=True,
                   autoplay=True,
                   muted=True
                   )
    else:
        if secuencia_min == "postura_concreta":
            for tip in TRANSICIONESTIPS[secuencia_concreta][postura]:
                videotip.markdown(f"- {tip}<br>", unsafe_allow_html=True)
        else:
            for tip in TRANSICIONESTIPS[sequence][pose_actual]:
                videotip.markdown(f"- {tip}<br>", unsafe_allow_html=True)
    with col2:
        user_pose = UserPose(postura, secuencia_concreta)
        video_processor = video_processor_factory()
        video_processor.set_draw(col1_kps)
        user_pose.set_sequence(secuencia_concreta)
        user_pose.set_pose(postura)
        rtc_configuration = RTCConfiguration({
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        })
        media_stream_constraints = {
            "video": {
                "width": {"ideal": CAM_WIDTH},
                "height": {"ideal": CAM_HEIGHT},
                "frameRate": {"exact": 15} #"min":20, "max": 40}
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
        # Mientras este el PLAY >>> Hacemos cositas aqui
        while webrtc_ctx.state.playing:
            keypoints = keypoint_queue.get()
            if frame_count % 10 == 0:
                frame_count += 1
                user_pose.update_keypoints(keypoints)
                user_pose.set_pose(postura)
                estado_usuario = user_pose.postura()
                if estado_usuario:
                    counterto100(scol3_bar, progress_text, frame_success)
                    frame_success += FRAMES_SUCCESS_RATIO
                    if frame_success >= 100:
                        update_semaforo(estado_usuario, scol4_semaforo)
                        frame_success = 0
                        step += 1
                        if step < len(posturas):
                            pose_actual = posturas[step]
                            scol2_text = f'''
                                            Modalidad: **:orange[SECUENCIA]**<br>
                                            Secuencia seleccionada: **:blue[{sequence}]**<br>
                                            Postura actual: **:red[{pose_actual}]**
                                            '''
                            scol2_modsec.markdown(scol2_text, unsafe_allow_html=True)
                            video_path = f"{VIDEO_DIR}/{secuencia_min}/{pose_actual}.mp4"
                            # Actualizar video mostrado
                            if col1_muestravid:
                                videotip.video(data=video_path,
                                               loop=True,
                                               autoplay=True,
                                               muted=True
                                               )
                        else:
                            st.success("¡Secuencia completada!")
                            break
                else:
                    frame_success = 0
                    counterto100(scol3_bar, progress_text, frame_success)
                if frame_count == 1000:
                    frame_count = 0
            else:
                frame_count += 1
        else:
            keypoint_queue.empty()