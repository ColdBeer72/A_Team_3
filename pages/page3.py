import streamlit as st
from inc.basic import *
from inc.config import *
from inc.joan_video_stream import *
from inc.manu_manage_cameras import *

st.header("Practica Posturas", anchor = False, divider="red")
st.subheader("Sigue las indicaciones", anchor = False, divider="gray")

lista_camaras = select_camera()
user_camara = int(st.selectbox(
    "Escoja la cámara con la que capturar:",
    lista_camaras,
    index=0,
    placeholder="Escoja una cámara"
))

secuencias = list(TRANSICIONES.keys()) + ["Postura concreta"]
secuencia = st.selectbox("Escoja su Secuencia", secuencias, index=len(secuencias)-1)

if secuencia == "Postura concreta":
    posturas = sublista(TRANSICIONES, "Saludo al sol")

    postura = st.select_slider("Escoja su postura a practicar:", posturas)

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
    st.warning("La selección de SECUENCIA todavía no está disponible.")
    # Se añadirá a postoriori