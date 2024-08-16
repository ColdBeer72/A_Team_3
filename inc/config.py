from ultralytics import YOLO
from streamlit_webrtc import RTCConfiguration

#Activar/Desactivar modo Debug
DEBUG = True
# Ancho de Columna por defecto en StreamLit
DEFAULT_COLUMN_WIDTH = 30
MIN_COLUMN_WIDTH = 15
MAX_COLUMN_WIDTH = 50
# Título de la Página
PAGE_TITLE = "DSB10RT Grupo A"
# Título del Proyecto
PROYECT_TITLE = "Proyecto Yoga"
# Logotipo de la Pagina
PAGE_LOGO = "streamlit_sources/iconoyoga.png"
PAGE_ICON = "streamlit_sources/iconoyoga_mini.png"
FAVICON = "streamlit_sources/favicon.png"
# Semáforo
SEM_GREEN = "streamlit_sources/semaphore_green.png"
SEM_RED = "streamlit_sources/semaphore_red.png"
# Path al Logotipo de HackaBoss
HAB_LOGO_PATH = "streamlit_sources/page1/hab_logo.png"
# Autores y referencias
LISTA_AUTORES = [
        ["juan", "Juan Crescenti", "https://www.linkedin.com/in/juancrescenti/"],
        ["manu", "Manuel Tornos", "https://www.linkedin.com/in/mtornos/"],
        ["jordi", "Jordi Porcel", "https://www.linkedin.com/in/jordi-porcel-mezquida-60168bb1/"],
        ["javi", "Javier Montoto", "https://www.linkedin.com/in/javier-montoto/"]
    ]
TRANSICIONESTIPS = {
        'Saludo al sol': {
            'Tadasana':         ['Equilibra el peso en ambos pies',
                                'Abre las manos hacia delante.', 
                                'Activa piernas, glúteos y abdomen'],
            'Urdhva Hastasana': ['Palmas en forma de rezo', 
                                'Mira tus manos', 
                                'Empuja caderas hacia delante', 
                                'Intención de tocar el cielo'],
            'Uttanasana':       ['Manten la espalda recta', 
                                'Flexiona rodillas si es necesario',
                                'Mirada al ombligo, cuello relajado'], 
            'Ardha Uttanasana': ['Mirada hacia delante',
                                'Toca el suelo con los dedos',
                                'Apoya manos en tibias si es necesario'],
            'Chaturanga Dandasana': ['Manos bien abiertas',
                                'Reparte bien el peso',
                                'Mirada hacia delante'],
            'Urdhva Mukha Svanasana': ['Empuja el suelo, junta las escápulas',
                                'Hombros alejados de las orejas y relajados',
                                'Apoya ligeramente los pies con el empeine',],
            'Adho Mukha Svanasana': ['Recoloca los pies adelante',
                                'Talones intentan tocar el suelo',
                                'Mirada al ombligo, cuello relajado',
                                 'Intención de tocar el cielo con los glúteos']
                        } 
                    }
# SECUENCIAS
FRAMES_SUCCESS_RATIO = 10
TRANSICIONES_SECUENCIA = {
    'Saludo al sol': {
        'Paso_1': 'Tadasana',
        'Paso_2' : 'Urdhva Hastasana',
        'Paso_3': 'Uttanasana',
        'Paso_4': 'Ardha Uttanasana',
        'Paso_5': 'Chaturanga Dandasana',
        'Paso_6': 'Urdhva Mukha Svanasana',
        'Paso_7': 'Adho Mukha Svanasana',
        'Paso_8': 'Uttanasana',
        'Paso_9': 'Ardha Uttanasana',
        'Paso_10': 'Urdhva Hastasana',
        'Paso_11': 'Tadasana'
    }
}
# Variables Page3
lista_sequences = list(TRANSICIONESTIPS.keys())
secuencias = lista_sequences + ["Postura concreta"]
postura = ""
secuencia_concreta = ""
upper_col2_text = '''
            '''
progress_text_wait = "Iniciando detección de postura..."
progress_text = "**¡Postura detectada!** Aguante unos instantes..."
posturas = []
#Formato de CAPTURA de vídeo
CAM_WIDTH = 640
CAM_HEIGHT = 480
# Origen del vídeo
VIDEO_DIR = "data/Secuencias"
VIDEO_PATH = VIDEO_DIR
# WEBRTC_PARAMS
rtc_configuration = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})
media_stream_constraints = {
    "video": {
        "width": {"ideal": CAM_WIDTH},
        "height": {"ideal": CAM_HEIGHT},
        "frameRate": {"exact": 15} #"min":20, "max": 40}
    },
    "audio": False
}
# Modelos
Modelos = {
    'YOLO': YOLO("../data/models/yolov8n-pose.pt"),
    'I+D': None
}
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
sounds_path = "streamlit_sources/page3/yoga_sounds"
sounds_dict = {
    'Tadasana': {
        f'{sounds_path}/tadasana': [1, 2, 3]
    },
    'Urdhva Hastasana': {
        f'{sounds_path}/urdhva_hastasana': [1, 2, 3]
    },
    'Uttanasana': {
        f'{sounds_path}/utanasana': [1, 2, 3]
    }, 
    'Ardha Uttanasana': {
        f'{sounds_path}/ardha_utanasana': [1, 2, 3]
    },
    'Chaturanga Dandasana': {
        f'{sounds_path}/chaturanga_dandasana': [1, 2, 3]
    },
    'Urdhva Mukha Svanasana': {
        f'{sounds_path}/urdhva_mukha_svanasana': [1, 2, 3]
    },
    'Adho Mukha Svanasana': {
        f'{sounds_path}/adho_mukha_svanasana': [1, 2, 3, 4],
    },
    # 'consejos': {
    #     f'{sounds_path}/consejos': []
    # }
}
# Umbrales del State Machine
class UMBRALES():
    THREE_POINT_STRAIGHT =              [195, 155]
    MANOS_JUNTAS =                      [40, 15]
    INCLINACION_CABEZA_UTTANASANA =     10
    ANGULO_CUERPO_ARDHA_UTTANASANA =    90
    HOMBRO_DCHO_TAPADO_CARA_ARDHA =     30
    BRAZOS_90_CHATURANGA =              [110, 70]
    CHATURANGA_Y_CODO_MUNECA =          10
    DIST_CODO_CHATURANGA =              45
    ORIENTACION_CABEZA_URDHVA_MUKHA =   10
    ESPALDA_RECTA_ADHO_MUKHA_SVANA =    [190, 150]
    FRAMES_SEMAFORO_EN_VERDE =          20

# Partes formato string
t_nariz: str =      'nariz'
t_ojoi: str =       'ojo_izdo'
t_ojod: str =       'ojo_dcho'
t_orejai: str =     'oreja_izda'
t_orejad: str =     'oreja_dcha'
t_hombroi: str =    'hombro_izdo' 
t_hombrod: str =    'hombro_dcho'
t_codoi: str =      'codo_izdo'
t_codod: str =      'codo_dcho'
t_munecai: str =    'muneca_izda'
t_munecad: str =    'muneca_dcha'
t_caderai: str =    'cadera_izda'
t_caderad: str =    'cadera_dcha'
t_rodillai: str =   'rodilla_izda'
t_rodillad: str =   'rodilla_dcha'
t_tobilloi: str =   'tobillo_izdo'
t_tobillod: str =   'tobillo_dcho'