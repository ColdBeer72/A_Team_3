import streamlit as st

# Versión Grupal
from inc.basic import *
from inc.config import *
from inc.video_stream import *

def main():

    # Configuración de la página
    st.set_page_config(page_title=PAGE_TITLE, layout="wide", initial_sidebar_state="collapsed",
                       page_icon=FAVICON)
    st.logo(PAGE_LOGO, icon_image = PAGE_ICON, link = None)

    st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

    pages = {
        "🔴 El Proyecto": [
            st.Page("hojas/01_Presentation.py", title="Presentación", icon=":material/support_agent:", default=True),
            st.Page("hojas/02_Sobre_el_Estudio.py", title="Sobre el Estudio", icon=":material/book:"),
        ],
        "🔴 La Aplicación": [
            st.Page("hojas/03_Practica_Yoga.py", title="Practica Yoga", icon=":material/self_improvement:"),
            st.Page("hojas/04_Sabiduria_y_asanas.py", title='Sabiduría y Asanas', icon= ':material/school:'),
            st.Page("hojas/05_PROBANDO_WEBCAM_COSAS.py", title="Practica Yoga 2.0", icon=":material/self_improvement:"),
        ],
    }

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main()