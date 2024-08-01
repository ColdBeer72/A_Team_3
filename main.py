import streamlit as st

# Versión Grupal
from inc.basic import *
from inc.config import *
from inc.joan_video_stream import *
from inc.manu_manage_cameras import *

def main():

    page1 = st.Page("pages/page1.py", title="Presentación", icon=":material/support_agent:", default=True)
    page2 = st.Page("pages/page2.py", title="Sobre el Estudio", icon=":material/delete:")
    page3 = st.Page("pages/page3.py", title="Practica Yoga", icon=":material/self_improvement:")
    

    pg = st.navigation([page1, page2, page3])
    # Configuración de la página
    st.set_page_config(page_title=PAGE_TITLE, layout="wide", initial_sidebar_state="collapsed",
                       page_icon=":material/self_improvement:")
    pg.run()

if __name__ == "__main__":
    main()