import streamlit as st
from inc.basic import *

st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

# Título principal
col1, col2 = st.columns([3, 1])
with col1:
#    st.title(PROYECT_TITLE, anchor = False)
    st.image(PAGE_LOGO, use_column_width="auto")
with col2:
    st.image(LOGO_PATH, width=100)


st.header("Presentación del Proyecto", anchor = False, divider="red")
st.subheader("Proyecto de:", anchor = False, divider="gray")

autores()