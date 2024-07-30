# Ancho de Columna por defecto en StreamLit
DEFAULT_COLUMN_WIDTH = 30
MIN_COLUMN_WIDTH = 15
MAX_COLUMN_WIDTH = 50
# Título de la Página
PAGE_TITLE = "DSB10RT Grupo A"
# Título del Proyecto
PROYECT_TITLE = "Proyecto Final"
# Path al Logotipo de HackaBoss
LOGO_PATH = "streamlit_sources/hab_logo.png"
# Autores y referencias
LISTA_AUTORES = [["juan", "Juan Crescenti", "https://www.linkedin.com/in/juancrescenti/"],
            ["manu", "Manuel Tornos", "https://www.linkedin.com/in/mtornos/"],
            ["jordi", "Jordi Porcel", "https://www.linkedin.com/in/jordi-porcel-mezquida-60168bb1/"],
            ["javi", "Javier Montoto", "https://www.linkedin.com/in/javier-montoto/"]]
#Formato de CAPTURA de vídeo
CAM_WIDTH = 640
CAM_HEIGHT = 480
# Origen del vídeo
VIDEO_DATA = "data/Raw/01_Tadasana/Figura1_Tadasana_Postura de equilibro.mp4"
# Lista de Transiciones con sus diferentes posturas
TRANSICIONES = {
            'Saludo al sol': {
                'Tadasana': 'Urdhva Hastasana',
                'Urdhva Hastasana': 'Uttanasana',
                'Uttanasana': 'Ardha Uttanasana', 
                'Ardha Uttanasana': ['Chaturanga Dandasana', 'Urdhva Hastasana'],
                'Chaturanga Dandasana': 'Urdhva Mukha Svanasana',
                'Urdhva Mukha Svanasana': 'Adho Mukha Svanasana',
                'Adho Mukha Svanasana': 'Uttanasana'
            }
        }
# Margen (sup. e inf.) para extremidad en posición "recta"
LIMB_STRAIGHT_ANGLE = 10