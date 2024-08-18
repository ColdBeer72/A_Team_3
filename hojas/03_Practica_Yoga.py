import streamlit as st
from inc.basic import *
from inc.config import *
from inc.functions_page3 import *
from inc.state_machine import *
from streamlit_webrtc import webrtc_streamer, WebRtcMode

st.markdown(
    HIDE_IMG_FS,
    unsafe_allow_html=True
)

if 'grabando' not in st.session_state:
    st.session_state.grabando = False

if 'frame_count' not in st.session_state:
    st.session_state.frame_count = 0

if 'frames_success' not in st.session_state:
    st.session_state.frames_success = 0

if 'step' not in st.session_state:
    st.session_state.step = 0

if 'secuencia' not in st.session_state:
    st.session_state.secuencia = False

user_pose = UserPose()

# Header de la página
st.subheader(
    "Practica Posturas",
    anchor=False,
    divider="rainbow"
)

# DISTRIBUCION DEL ESPACIO
# Caja Superior > Seleccion de Ex
caja_superior = st.container(
    height=110,
    border=True
)
# Caja Inferior > Ex en Webcam
caja_inferior = st.container(
    height=600,
    border=True
)

# Columnas Superiores
up_col1, up_col2, up_col3, up_col4 = caja_superior.columns(
        spec=[25, 30, 30, 15],
        gap='small',
        vertical_alignment='top'
)
# Columnas inferiores
_, down_col1, _, down_col2, _ = caja_inferior.columns(
        spec=[5, 15, 15, 45, 20],
        gap='small',
        vertical_alignment='top'
)

# SECCION SUPERIOR
# Up_Col1 > Selector Ejercicio
with up_col1:
    sequence, postura, video_path, upper_col2_text = up_col1_menu(up_col1)
    user_pose.set_pose(postura)
    user_pose.set_sequence(sequence)
# Up_Col2 > Visualizar INFO
with up_col2:
    up_col2_info_markdown = st.empty()
    up_col2_update_info_markdown(
        up_col2_info_markdown,
        upper_col2_text
    )
# Up_Col3 > Carga de Check Postura
with up_col3:
    up_col3_progress_bar = st.empty()
# Up_Col4 > Semaforo
with up_col4:
    up_col4_status = st.empty()

# SECCION INFERIOR
# Down_Col1 > TIPS / VIDS + toggles
with down_col1:
    model_select = down_col1_choose_model(down_col1)
    video_processor = video_processor_factory(model_select)
    down_col1_update_kps_vision(
        down_col1,
        video_processor
    )
    tips_or_video_box = down_col1.container(
        height=None,
        border= False
    )
    down_col1_update_tips_or_vids(
        down_col1,
        video_path,
        sequence,
        postura,
        tips_or_video_box
    )
# Down_Col2 > Webcam
with down_col2:
    webrtc_ctx = webrtc_streamer(
        key="streamer",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=video_processor.recv,
        rtc_configuration=rtc_configuration,
        media_stream_constraints=media_stream_constraints,
        async_processing=True
    )
    while webrtc_ctx.state.playing:
        if not st.session_state.grabando:
            st.session_state.grabando = True
        keypoints = keypoint_queue.get()
        if st.session_state.frame_count % 10 != 0:
            DEBUG and print("FRAME_COUNT != 0")
            frame_counter_increment()
        elif st.session_state.frame_count % 10 == 0:
            DEBUG and print(f"{st.session_state.frame_count}")
            frame_counter_increment()
            try:
                estado_usuario = check_postura(
                    user_pose,
                    keypoints
                )
            except:
                estado_usuario = False
            if estado_usuario:
                st.session_state.frames_success += FRAMES_SUCCESS_RATIO
                up_col3_update_progress_bar(up_col3_progress_bar)
                if st.session_state.frames_success == 100:
                    pose_success(
                        user_pose,
                        up_col4_status
                    )
            else:
                up_col3_update_progress_bar(up_col3_progress_bar)
                up_col4_update_status(
                    up_col4_status,
                    False
                )
                reset_frame_success()
        else:
            frame_counter_increment()
    else:
        keypoint_queue.empty()
        st.session_state.grabando = False