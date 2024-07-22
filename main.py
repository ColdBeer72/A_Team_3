import streamlit as st

# Configuración de la página
st.set_page_config(page_title="DSB10RT Grupo A", layout="wide", initial_sidebar_state="collapsed")

# Título principal
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Proyecto Final")
with col2:
    logo_path = "streamlit_sources/hab_logo.png"
    st.image(logo_path, width=100)

# Barra lateral con submenús
menu = st.sidebar.radio(
    "¿Qué quieres visitar?:",
    ("Presentación del Proyecto", "Presentación del Estudio", "Desarrollo del Estudio")
)

# 1. Presentación del Proyecto
if menu == "Presentación del Proyecto":
    st.header("Presentación del Proyecto")
    st.subheader("Proyecto de:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("""[Joan Crescenti](https://www.linkedin.com/in/juancrescenti/)""")
        joan = "streamlit_sources/joan.jpg"
        st.image(joan, width=100)
    with col2:
        st.write("[Manuel Tornos](https://www.linkedin.com/in/mtornos/)")
        manu = "streamlit_sources/manu.jpg"
        st.image(manu, width=100)
    with col3:
        st.write("[Jordi Porcel](https://www.linkedin.com/in/jordi-porcel-mezquida-60168bb1/)")
        jordi = "streamlit_sources/jordi.png"
        st.image(jordi, width=100)
    with col4:
        st.write("[Javier Montoto](https://www.linkedin.com/in/javier-montoto/)")
        javi = "streamlit_sources/javier.jpg"
        st.image(javi, width=100)

# 2. Presentación del Estudio
elif menu == "Presentación del Estudio":
    st.header("Presentación del Estudio")
    st.write("""
        Prueba
    """)
    # Añade más contenido aquí según lo que quieras presentar

# 3. Desarrollo del Estudio
elif menu == "Desarrollo del Estudio":
    st.header("Desarrollo del Estudio")
    st.write("""
        Prueba
    """)
    # Aprox. = % continuo, Tonif. = Bien solo con +70%, Perf. = Bien solo con +90%
    difficulty = st.selectbox("Escoja la exigencia:", ["Aproximación", "Tonificación", "Perfección"])
    duration = st.slider("¿De cuánto tiempo dispones?", 5, 30)
    postura = "Tadasana"
    
    DEFAULT_WIDTH = 30
    VIDEO_DATA = "data/01_Tadasana/Figura1_Tadasana_Postura de equilibro.mov"
    width = st.sidebar.slider(
        label= "Tamaño del Video:",
        min_value=15,
        max_value=50,
        value=DEFAULT_WIDTH,
        format="%d%%")
    width = max(width, 0.01)
    side = max((100 - width) / 2, 0.01)
    _, container, _ = st.columns([side, width, side])
    container.subheader(f"Video ejemplo de la postura {postura}:")
    container.video(data=VIDEO_DATA)
    user_input = st.camera_input(f"Inicie la postura {postura}")