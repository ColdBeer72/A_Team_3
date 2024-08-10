import streamlit as st
from inc.basic import *

st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

# Título principal
col1, col2 = st.columns([3, 1])
with col1:
    st.image(PAGE_LOGO, use_column_width="auto")
with col2:
    st.image(HAB_LOGO_PATH, width=100)

# Presentacion del Proyecto
st.header("Presentación del Proyecto", anchor = False, divider="red")
presentacion_path = "streamlit_sources/page1_presentation.md"
presentacion = read_markdown_file(presentacion_path)
st.markdown(presentacion)

# Firma
st.subheader("Proyecto de:", anchor = False, divider="gray")
autores()