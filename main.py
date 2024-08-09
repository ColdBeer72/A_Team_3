import streamlit as st

# Versión Grupal
from inc.basic import *
from inc.config import *
from inc.video_stream import *

def main():

    # Configuración de la página
    st.set_page_config(page_title=PAGE_TITLE, layout="wide", initial_sidebar_state="collapsed",
                       page_icon=":material/self_improvement:")
    st.logo(PAGE_LOGO, icon_image = PAGE_ICON, link = None)

    st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

    page1 = st.Page("hojas/01_Presentation.py", title="Presentación", icon=":material/support_agent:", default=True)
    page2 = st.Page("hojas/02_Sobre_el_Estudio.py", title="Sobre el Estudio", icon=":material/book:")
    page3 = st.Page("hojas/03_AsanAI.py", title="AsanAI", icon=":material/self_improvement:")
    page4 = st.Page("hojas/04_Sabiduria_y_asanas.py", title='Sabiduría y Asanas', icon= '🙏🏻')

    pg = st.navigation([page1, page2, page3, page4])

    pg.run()

if __name__ == "__main__":
    main()