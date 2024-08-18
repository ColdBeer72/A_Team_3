from pathlib import Path
from inc.config import *
import streamlit as st
import queue
from inc.video_stream import VideoProcessor
import time

from typing import Annotated

HIDE_IMG_FS = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
<style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 1rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
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
        st.write(f"**[{LISTA_AUTORES[0][1]}]({LISTA_AUTORES[0][2]})**")
        img = f"./streamlit_sources/page1/{LISTA_AUTORES[0][0]}.jpg"
        st.image(img, width=100)
    with col2:
        st.write(f"**[{LISTA_AUTORES[1][1]}]({LISTA_AUTORES[1][2]})**")
        img = f"./streamlit_sources/page1/{LISTA_AUTORES[1][0]}.jpg"
        st.image(img, width=100)
    with col3:
        st.write(f"**[{LISTA_AUTORES[2][1]}]({LISTA_AUTORES[2][2]})**")
        img = f"./streamlit_sources/page1/{LISTA_AUTORES[2][0]}.jpg"
        st.image(img, width=100)
    with col4:
        st.write(f"**[{LISTA_AUTORES[3][1]}]({LISTA_AUTORES[3][2]})**")
        img = f"./streamlit_sources/page1/{LISTA_AUTORES[3][0]}.jpg"
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

# Factoria de VideoProcessor
def video_processor_factory(model):
    model_input = model
    return VideoProcessor(model_input)

def to_minus(str):
    return "_".join(str.split(" ")).lower()