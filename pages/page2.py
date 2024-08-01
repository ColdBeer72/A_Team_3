import streamlit as st
from inc.basic import *

st.header("Presentación del Estudio")
md_presentation = "streamlit_sources/presentation.md"
txt_presentation = read_markdown_file(md_presentation)
st.markdown(txt_presentation)