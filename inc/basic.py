from pathlib import Path
from inc.config import *
import streamlit as st
from multiprocessing import Queue
import queue
from inc.video_stream import VideoProcessor

from typing import Annotated

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

def read_markdown_file(markdown_file : Annotated[str, "md_file: Ruta y nombre del Archivo"]):
    """Devuelve el contenido de un archivo MarkDown.

    Returns:
        mdtext: Devuelve el contenido del archivo
    """
    return Path(markdown_file).read_text()

def autores():
    """Genera 4 columnas con los autores del Proyecto
    Args:
        None

    Returns:
        None
    """

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write(f"[{LISTA_AUTORES[0][1]}]({LISTA_AUTORES[0][2]})")
        img = f"./streamlit_sources/{LISTA_AUTORES[0][0]}.jpg"
        st.image(img, width=100)
    with col2:
        st.write(f"[{LISTA_AUTORES[1][1]}]({LISTA_AUTORES[1][2]})")
        img = f"./streamlit_sources/{LISTA_AUTORES[1][0]}.jpg"
        st.image(img, width=100)
    with col3:
        st.write(f"[{LISTA_AUTORES[2][1]}]({LISTA_AUTORES[2][2]})")
        img = f"./streamlit_sources/{LISTA_AUTORES[2][0]}.jpg"
        st.image(img, width=100)
    with col4:
        st.write(f"[{LISTA_AUTORES[3][1]}]({LISTA_AUTORES[3][2]})")
        img = f"./streamlit_sources/{LISTA_AUTORES[3][0]}.jpg"
        st.image(img, width=100)

def sublista(diccionario=TRANSICIONES, clave_superior="Saludo al sol"):
  """
  Esta función extrae todos los índices (posturas) de un subdiccionario dentro de un diccionario principal.

  Args:
      diccionario: Diccionario principal que contiene subdiccionarios.
      clave_superior: Clave del subdiccionario del que se quieren extraer las posiciones (opcional, por defecto "Saludo al sol").

  Returns:
      Lista con todas las posiciones (posturas) del subdiccionario especificado.
  """
  if clave_superior in diccionario:
    return list(diccionario[clave_superior].keys())
  else:
    return []

def class_2_dict(clase: type) -> dict:
    new_dict = {}
    for clave, valor in vars(clase).items():
        if not clave.startswith('__'):
            new_dict[clave] = valor
    return new_dict

# Updatear estado del semaforo
def update_semaforo(state, sitio):
    if state:
        sitio.image(SEM_GREEN, use_column_width="auto")
    else:
        sitio.image(SEM_RED, use_column_width="auto")

def update_keypoints(keypoint_queue, user_pose):
    while True:
        try:
            keypoints = keypoint_queue.get(timeout=1)
            if keypoints is None:
                break
            user_pose.update_keypoints(keypoints)
        except queue.Empty:
            continue

def get_current_body_dict():
    return VideoProcessor.get_body_dict()