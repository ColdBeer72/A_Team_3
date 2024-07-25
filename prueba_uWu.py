import streamlit as st
import pandas as pd
from inc.state_machine import UserPose
from inc.pruebitas_gege import yololo
import cv2

# Versión Grupal
from inc.basic import *

# Configuración de la página
md_presentation = "streamlit_sources/presentation.md"
st.set_page_config(page_title="DSB10RT Grupo A", layout="wide", initial_sidebar_state="collapsed")

# Título principal
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Proyecto Final")
with col2:
    logo_path = "streamlit_sources/hab_logo.png"
    st.image(logo_path, width=100)

# Barra lateral con submenús
menu = st.sidebar.radio(
    "¿Qué quieres visitar?:",
    ("Presentación del Proyecto", "Presentación del Estudio", "Desarrollo del Estudio")
)

# 1. Presentación del Proyecto
if menu == "Presentación del Proyecto":
    st.header("Presentación del Proyecto")
    st.subheader("Proyecto de:")
    autores()

# 2. Presentación del Estudio
elif menu == "Presentación del Estudio":
    st.header("Presentación del Estudio")
    txt_presentation = read_markdown_file(md_presentation)
    st.markdown(txt_presentation)

# 3. Desarrollo del Estudio
elif menu == "Desarrollo del Estudio":
    st.header("Desarrollo del Estudio")
    st.write("""
        Prueba
    """)
    # df = pd.read_csv("data/Yoga_figure_surya_namaskar_A - Hoja 1.csv")
    # st.dataframe(df)
    # Aprox. = % continuo, Tonif. = Bien solo con +70%, Perf. = Bien solo con +90%
    difficulty = st.selectbox("Escoja la exigencia:", ["Aproximación", "Tonificación", "Perfección"])
    
    level = st.selectbox("Escoja el nivel de tu clase:", ["Básico", "Medio", "Experto"])

    duration = st.slider("¿De cuánto tiempo dispones?", 30, 90)
    
    DEFAULT_WIDTH = 30
    VIDEO_DATA = "data/Raw/01_Tadasana/Figura1_Tadasana_Postura de equilibro.mp4"
    width = st.sidebar.slider(
        label= "Tamaño del Video:",
        min_value=15,
        max_value=50,
        value=DEFAULT_WIDTH,
        format="%d%%")
    width = max(width, 0.01)
    side = max((100 - width) / 2, 0.01)
    # Creacion de 2 columnas side para centrar el Container del Vid
    _, container, _ = st.columns([side, width, side])
    postura = st.selectbox("Escoja su posturita, marija", ["Tadasana", "Madasana", "Culito de rana"])
    container.subheader(f"Video ejemplo de la postura {postura}:")
    container.video(data=VIDEO_DATA)
    user_input = st.camera_input(f"Inicie la postura {postura}")
    user_input = cv2.VideoCapture(VIDEO_DATA)
    while user_input.isOpened():
        ret, frame = user_input.read()
        posturita = UserPose()
        posturita.set_pose(postura)
        results = yololo(frame)
        body_dict = {'nariz': [],
                'ojo_izdo': [],
                'ojo_dcho': [],
                'oreja_izda': [],
                'oreja_dcha': [],
                'hombro_izdo': [],
                'hombro_dcho': [],
                'codo_izdo': [],
                'codo_dcho': [],
                'muneca_izda': [],
                'muneca_dcha': [],
                'cadera_izda': [],
                'cadera_dcha': [],
                'rodilla_izda': [],
                'rodilla_dcha': [],
                'tobillo_izdo': [],
                'tobillo_dcho': []
                }
        for result in results:
            keypoints = result.keypoints.xy
            for kp, body_part in zip(keypoints[0], body_dict):
                x, y = kp[0], kp[1]
                body_dict[body_part].append(x)
                body_dict[body_part].append(y)
        
        for parte, kps in body_dict.items():
            setattr(posturita, parte, kps)

        if posturita.name == 'Tadasana':
            while posturita.check_tadasana() == False:
                print("Corrige postura, IMBECIL! Samanté")
                posturita.tadasana()
            st.status("Success", expanded = True)
            print("Tadasana COMPLETE!!! MADAFAKA!")
    user_input.release()
