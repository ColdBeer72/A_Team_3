import streamlit as st
from inc.basic import *

st.header("Más sobre el Yoga", anchor = False, divider="red")
st.subheader("Significados", anchor = False, divider="gray")

md_presentation = "streamlit_sources/sn_meaning.md"
txt_presentation = read_markdown_file(md_presentation)
st.markdown(txt_presentation)