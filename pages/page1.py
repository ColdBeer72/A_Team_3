import streamlit as st
from inc.basic import *

# Título principal
col1, col2 = st.columns([3, 1])
with col1:
    st.title(PROYECT_TITLE)
with col2:
    st.image(LOGO_PATH, width=100)

st.header("Presentación del Proyecto")
st.subheader("Proyecto de:")
autores()