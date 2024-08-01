import cv2
from inc.basic import *
from inc.state_machine import UserPose
from inc.joan_YOLO_process import process_frame

def captura_video(camara=0):
    cap = cv2.VideoCapture(camara)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_WIDTH)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        yield frame
    cap.release()

def func_video(secuencia: str, postura: str, camera: int):
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
        for frame in captura_video(camera):
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