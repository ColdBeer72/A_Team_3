import streamlit as st
from inc.basic import *

st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

# Título principal
col1, col2 = st.columns([3, 1])
with col1:
    st.image(
        PAGE_LOGO,
        use_column_width="auto"
    )
with col2:
    st.image(
        HAB_LOGO_PATH,
        width=100
    )
# Presentacion del Proyecto
st.header("Presentación del Proyecto", anchor = False, divider="red")
presentacion_path = "streamlit_sources/page1/presentation.md"
presentacion = read_markdown_file(presentacion_path)
st.markdown(presentacion)
with st.expander("**Tecnologías Utilizadas:**"):
    techs_md_path = "streamlit_sources/page1/techs.md"
    techs_md = read_markdown_file(techs_md_path)
    st.markdown(techs_md)
st.markdown("#### AI + ML + UXUI:")
col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("**AI - Inteligencia Artificial**"):
        ia_md_path = "streamlit_sources/page1/ia.md"
        ia_md = read_markdown_file(ia_md_path)
        st.markdown(ia_md)
with col2:
    with st.expander("**ML - Machine Learning**"):
        ml_md_path = "streamlit_sources/page1/ml.md"
        ml_md = read_markdown_file(ml_md_path)
        st.markdown(ml_md)
with col3:
    with st.expander("**UX/UI - Experiencia de Usuario / Interfaz de Usuario**"):
        uxui_md_path = "streamlit_sources/page1/uxui.md"
        uxui_md = read_markdown_file(uxui_md_path)
        st.markdown(uxui_md)

# Firma
st.subheader("Proyecto de:", anchor = False, divider="gray")
autores()