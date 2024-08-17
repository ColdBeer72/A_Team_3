from inc.basic import *
from inc.config import *
import streamlit as st
from inc.video_stream import keypoint_queue
import time

# UPDATE INFO Caja Superior
def update_upper_col2_info(sequence, postura, selection):
    sequence_minus = to_minus(sequence)
    postura_minus = to_minus(postura)
    video_path = VIDEO_PATH + f"/{sequence_minus}/{postura_minus}.mp4"
    upper_col2_text = f'''
        Modalidad: **<span style="color:orange;">{selection}</span>**<br>
        Secuencia: **<span style="color:purple;">{sequence}</span>**<br>
        Postura: **<span style="color:magenta;">{postura}</span>**
        '''
    return(video_path, upper_col2_text)

def set_pose_for_sequence(sequence):
    lista_posturas = list(TRANSICIONES_SECUENCIA[sequence].values())
    if st.session_state.step < len(lista_posturas):
        postura = lista_posturas[st.session_state.step]
        video_path, upper_col2_text = update_upper_col2_info(
            sequence,
            postura,
            'SECUENCIA'
        )
    return postura, video_path, upper_col2_text

###############################################################################################
#                                   POPOVER MENUS                                             #
###############################################################################################
def up_col1_specific_pose_selection(box):
    sequence = box.selectbox(
        "¿De qué secuencia quieres practicar una postura?",
        lista_sequences,
    )
    list_posturas = sublista(
        TRANSICIONESTIPS,
        sequence
    )
    postura = box.select_slider(
        "Escoja postura a practicar:",
        list_posturas
    )
    video_path, upper_col2_text = update_upper_col2_info(
        sequence,
        postura,
        'PORTURA CONCRETA'
    )
    return(sequence, postura, video_path, upper_col2_text)

def up_col1_specific_sequence_selection(box):
    if st.session_state.secuencia:
        sequence = box.selectbox(
            "¿Qué secuencia quieres practicar?",
            lista_sequences,
            )
        postura, video_path, upper_col2_text = set_pose_for_sequence(sequence)
        return(sequence, postura, video_path, upper_col2_text)

def up_col1_menu(location):
    select_exercice = location.popover(("Selecciona tu ejercicio"))
    selection = select_exercice.radio(
        "¿Qué deseas practicar?",
        ["**Postura** :camera:", "**Secuencia** :movie_camera:"],
        captions=["Postura concreta de una secuencia especifica.", "Postura a postura, realizarás una secuencia completa."]
    )
    if selection == '**Postura** :camera:':
        st.session_state.secuencia = False
        return up_col1_specific_pose_selection(select_exercice)
    else:
        st.session_state.secuencia = True
        return up_col1_specific_sequence_selection(select_exercice)
    
###############################################################################################
#                           INFO SELECCION DE SECUENCIA + POSTURA                             #
###############################################################################################
def up_col2_update_info_markdown(location, md):
    location.markdown(
        md,
        unsafe_allow_html=True
    )

###############################################################################################
#                                   BARRA DE PROGRESO                                         #
###############################################################################################
def up_col3_update_progress_bar(location):
    if st.session_state.grabando:
        if 0 < st.session_state.frames_success <= 100:
            location.progress(
                st.session_state.frames_success,
                text=progress_text
            )
        else:
            location.progress(
                0,
                text=progress_text_wait
            )

###############################################################################################
#                                       SEMAFORO                                              #                                                         
###############################################################################################
def up_col4_update_status(location, state):
    if st.session_state.grabando:
        if state:
            location.image(
                SEM_GREEN,
                use_column_width="auto"
            )
        else:
            location.image(
                SEM_RED,
                use_column_width="auto"
            )

###############################################################################################
#                                    LATERAL WEBCAM                                           #                                                         
###############################################################################################
def down_col1_choose_model(location):
    selection = location.radio(
        "**Modelo**",
        Modelos.keys(),
        horizontal=True,
        label_visibility='visible'
    )
    return Modelos[selection]

def down_col1_update_kps_vision(location, video_processor):
    see_keypoints = location.toggle(
        "Ver KeyPoints",
        value=True
    )
    video_processor.set_draw(see_keypoints)

def down_col1_update_tips_or_vids(location, video_path, sequence, postura, tips_or_video_box):
    tips_or_vid = location.toggle(
        label="TIPS / VIDEO",
        value=False
    )
    if tips_or_vid:
        down_col1_update_video(
            tips_or_video_box,
            video_path
        )
    else:
        down_col1_update_tips(
            tips_or_video_box,
            sequence,
            postura
        )

def down_col1_update_video(location, video_path):
    location.video(
        data=video_path,
        loop=True,
        autoplay=True,
        muted=True
    )

def down_col1_update_tips(location, sequence, postura):
    for tip in TRANSICIONESTIPS[sequence][postura]:
        location.markdown(
            f"- {tip}<br>",
            unsafe_allow_html=True
        )

###############################################################################################
#                                     WEBCAM                                                  #                                                         
###############################################################################################
def frame_counter_increment():
    DEBUG and print(f"Aumento frame_count de: {st.session_state.frame_count}")
    st.session_state.frame_count += 1
    DEBUG and print(f"a {st.session_state.frame_count}")

def reset_frame_success():
    DEBUG and print(f"Reseteo frame_success de {st.session_state.frames_success}")
    st.session_state.frames_success = 0
    DEBUG and print(f"a {st.session_state.frames_success}")

def check_postura(user_pose, kps):
    user_pose.update_keypoints(kps)
    return user_pose.postura()

def next_sequence_step(user_pose):
    st.session_state.step += 1
    postura, _, _ = set_pose_for_sequence(user_pose.actual_sequence)
    user_pose.set_pose(postura)

def pose_success(user_pose, semaforo):
    up_col4_update_status(
        semaforo,
        True
    )
    time.sleep(1)
    DEBUG and print(st.session_state.secuencia)
    reset_frame_success()
    if st.session_state.secuencia:
        next_sequence_step(user_pose)

def down_col2_webcam(webrtc_ctx, user_pose, progress, semaforo):
    while webrtc_ctx.state.playing:
        st.session_state.grabando = True
        keypoints = keypoint_queue.get()
        if st.session_state.frame_count % 10 == 0:
            frame_counter_increment()
            estado_usuario = check_postura(
                user_pose,
                keypoints
            )
            if estado_usuario:
                st.session_state.frames_success += FRAMES_SUCCESS_RATIO
                up_col3_update_progress_bar(progress)
                if st.session_state.frames_success == 100:
                    pose_success(
                        user_pose,
                        semaforo
                    )
            else:
                up_col3_update_progress_bar(progress)
                up_col4_update_status(semaforo, False)
                reset_frame_success()
        else:
            frame_counter_increment()
    else:
        keypoint_queue.empty()
        st.session_state.grabando = False

###############################################################################################
#                                 AUDIOS - Falta Implementacion                               #                                                         
###############################################################################################
# def play_audios(files):
#     st.sidebar.image("streamlit_sources/page3/fullet_tortuga.png")
#     with st.sidebar.status("Consejos del sabio Mutenroshi"):
#         for file in files:
#             st.audio(
#                 data=file,
#                 format='audio',
#                 autoplay=True
#             )
#             time.sleep(3.5)

# def mutenroshi_player(postura, set):
#     files = []
#     if postura:
#         path = list(sounds_dict[postura].keys())[0]
#         cdad_audios = list(sounds_dict[postura].values())[0]
#         for i in cdad_audios:
#             file_path = f"{path}/{i}.mp3"
#             files.append(file_path)
#     if st.session_state.grabando and set:
#         play_audios(files)