import streamlit as st
#from inc.basic import sublista, update_semaforo
from inc.basic import *
from inc.config import *
from inc.state_machine import *
from inc.video_stream import VideoProcessor, keypoint_queue
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

postura = ""
secuencia_concreta = ""
falso_frame_count = 0

def video_processor_factory():
    model_input = Modelos.YOLO
    return VideoProcessor(model_input)

st.subheader("Practica Posturas", anchor = False, divider="red")

# st.subheader("¡Escoge tu ejercicio!", anchor = False, divider="gray")

secuencias_red = list(TRANSICIONESTIPS.keys())
secuencias = secuencias_red + ["Postura concreta"]

cajaselect = st.container(height = 100, border = True)
scol1, scol2, scol3, scol4 = cajaselect.columns(
        spec=[20, 45, 30, 5],
        gap='small',
        vertical_alignment='top'
    )
scol1_seleccion = scol1.popover("Selecciona tu ejercicio")
scol1_secuencia = scol1_seleccion.selectbox(
        "Escoja su Secuencia",
        secuencias,
        index=len(secuencias)-1
    )
scol1_cajavisos = scol1.empty()
scol2_modsec = scol2.empty()
scol2_text = ""

progress_text = "Postura detectada, un momento..."
scol3_scroll = scol3.empty()

secuencia_min = "_".join(scol1_secuencia.split(" ")).lower()
cajavideos = st.empty()
vercaja = False
estado_usuario = False

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
    secuencia_concreta = scol1_seleccion.selectbox("¿De qué secuencia quieres practicar una postura?", secuencias_red)
    scol1_seleccion.warning("La selección de SECUENCIA todavía no está disponible.")
    # Se añadirá a postoriori
    scol2_text = ""
    vercaja = False

scol2_modsec.markdown(scol2_text, unsafe_allow_html=True)

scol3_bar = scol3.progress(0, text=progress_text)
counterto100(scol3_bar, progress_text)
# scol3_bar = scol3.button("Activa")
scol3.button("Activa")

scol4_semaforo = scol4.empty()
update_semaforo(estado_usuario, scol4_semaforo)

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
    col1_muestravid = col1.toggle(
        label="TIPS / VIDEO MUESTRA",
        value=False
    )
    col1_kps = col1.checkbox(
        "¿Quieres ver los Keypoints en el video?",
        value=True
        )
    videotip = col1.container(height=None, border= False)

    if col1_muestravid:
        videotip.video(data=video_path,
                   loop=True,
                   autoplay=True,
                   muted=True
                   )
    else:
        # col1.write("Aquí vendrán los TIPS")
        for tip in TRANSICIONESTIPS[secuencia_concreta][postura]:
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
            if falso_frame_count % 10 == 0:
                falso_frame_count += 1
                user_pose.update_keypoints(keypoints)
                user_pose.set_pose(postura)
                estado_usuario = user_pose.postura()
                update_semaforo(estado_usuario, scol4_semaforo)
                if falso_frame_count == 1000:
                    falso_frame_count = 0
            else:
                falso_frame_count += 1
        else:
            keypoint_queue.empty()