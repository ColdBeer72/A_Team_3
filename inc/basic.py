from pathlib import Path
import streamlit as st

CAM_WIDTH = 640
CAM_HEIGHT = 480

def read_markdown_file(markdown_file):
    """Devuelve el contenido de un archivo MarkDown.

    Args:
        markdown_file (string): Ruta y nombre del Archivo

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
    lista = [["juan", "Juan Crescenti", "https://www.linkedin.com/in/juancrescenti/"],
             ["manu", "Manuel Tornos", "https://www.linkedin.com/in/mtornos/"],
             ["jordi", "Jordi Porcel", "https://www.linkedin.com/in/jordi-porcel-mezquida-60168bb1/"],
             ["javi", "Javier Montoto", "https://www.linkedin.com/in/javier-montoto/"]]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write(f"[{lista[0][1]}]({lista[0][2]})")
        img = f"streamlit_sources/{lista[0][0]}.jpg"
        st.image(img, width=100)
    with col2:
        st.write(f"[{lista[1][1]}]({lista[1][2]})")
        img = f"streamlit_sources/{lista[1][0]}.jpg"
        st.image(img, width=100)
    with col3:
        st.write(f"[{lista[2][1]}]({lista[2][2]})")
        img = f"streamlit_sources/{lista[2][0]}.jpg"
        st.image(img, width=100)
    with col4:
        st.write(f"[{lista[3][1]}]({lista[3][2]})")
        img = f"streamlit_sources/{lista[3][0]}.jpg"
        st.image(img, width=100)

def prueba_vacia():
    pass