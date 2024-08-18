import streamlit as st
from inc.basic import *

st.markdown(
    HIDE_IMG_FS,
    unsafe_allow_html=True
)

st.header(
    "Presentación del Estudio",
    anchor=False,
    divider="red"
)

md_presentation = "streamlit_sources/page2/presentation.md"
txt_presentation = read_markdown_file(md_presentation)
st.markdown(txt_presentation)