import streamlit as st
from inc.basic import *

st.markdown(hide_img_fs, unsafe_allow_html=True)

st.header("Presentación del Estudio", anchor = False, divider="red")
st.subheader("Para HackaBoss", anchor = False, divider="gray")

md_presentation = "streamlit_sources/presentation.md"
txt_presentation = read_markdown_file(md_presentation)
st.markdown(txt_presentation)