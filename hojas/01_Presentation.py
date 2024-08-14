import streamlit as st
from inc.basic import *

@st.dialog("Tecnologías Utilizadas")
def techies(item):
    st.markdown(item, unsafe_allow_html=True)

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

# with st.expander("**Tecnologías Utilizadas:**"):
#     techs_md_path = "streamlit_sources/page1/techs.md"
#     techs_md = read_markdown_file(techs_md_path)
#     st.markdown(techs_md)

techs_md_path = "streamlit_sources/page1/techs.md"
techs_md = read_markdown_file(techs_md_path)
if st.button("Tecnologías Utilizadas"):
    techies(techs_md)

_, columna, _ = st.columns([1,3,1], gap ="small", vertical_alignment = "top")

tab1, tab2, tab3, tab4 = columna.tabs([":bulb: **AI**",
                                 ":robot_face: **ML**",
                                 ":soap: **UX/UI**",
                                 ":1234: **Código**"])

with tab1:
    ia_md_path = "streamlit_sources/page1/ia.md"
    ia_md = read_markdown_file(ia_md_path)
    st.markdown(ia_md)
with tab2:
    ml_md_path = "streamlit_sources/page1/ml.md"
    ml_md = read_markdown_file(ml_md_path)
    st.markdown(ml_md)
with tab3:
    coding_md_path = "streamlit_sources/page1/uxui.md"
    coding_md = read_markdown_file(coding_md_path)
    st.markdown(coding_md)
with tab4:
    coding_md_path = "streamlit_sources/page1/coding.md"
    coding_md = read_markdown_file(coding_md_path)
    st.markdown(coding_md)

# Firma
st.subheader("Proyecto de:", anchor = False, divider="gray")
autores()