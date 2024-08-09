import streamlit as st
from inc.basic import *

# Título principal
col1, col2 = st.columns([3, 1])
with col1:
#    st.title(PROYECT_TITLE, anchor = False)
    st.image(PAGE_LOGO, use_column_width="auto")
with col2:
    st.image(LOGO_PATH, width=100)
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

st.header("Presentación del Proyecto", anchor = False, divider="red")
st.subheader("Proyecto de:", anchor = False, divider="gray")

autores()