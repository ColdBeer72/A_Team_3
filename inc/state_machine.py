import math
from inc.basic import *
from inc.config import *

class KeypointsHandler:
    def __init__(self):
        self.keypoints = {
            'nariz': None,
            'ojo_izdo': None,
            'ojo_dcho': None,
            'oreja_izda': None,
            'oreja_dcha': None,
            'hombro_izdo': None,
            'hombro_dcho': None,
            'codo_izdo': None,
            'codo_dcho': None,
            'muneca_izda': None,
            'muneca_dcha': None,
            'cadera_izda': None,
            'cadera_dcha': None,
            'rodilla_izda': None,
            'rodilla_dcha': None,
            'tobillo_izdo': None,
            'tobillo_dcho': None
        }

    # Actualizar keypoints
    def update_keypoints(self, keypoints: dict) -> None:
        for key, value in keypoints.items():
            try:
                self.keypoints[key] = value
            except:
                continue

    # Metodo para obtener KPs
    def get_keypoint(self, name: str) -> list:
        return self.keypoints.get(name)

class Pose_Calculator:
    def calcular_angulo(punto1: list, punto2: list, punto3: list) -> float:
        try:
            vector1 = (punto2[0] - punto1[0], punto2[1] - punto1[1])
            vector2 = (punto3[0] - punto2[0], punto3[1] - punto2[1])
            # Producto escalar
            producto_escalar = vector1[0] * vector2[0] + vector1[1] * vector2[1]
            # Magnitudes de los vectores
            magnitud_vector1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
            magnitud_vector2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
            # Coseno del ángulo
            coseno_angulo = producto_escalar / (magnitud_vector1 * magnitud_vector2)
            # Ángulo en grados
            angulo = math.acos(coseno_angulo) * 180 / math.pi
            return angulo
        except ZeroDivisionError:
            return None

    # Saber si 3 puntos estan rectos
    def limb_straight(self, limb1: list, limb2: list, limb3: list, threshold: int) -> bool:
        angulo_llano = 180
        angulo = Pose_Calculator.calcular_angulo(limb1, limb2, limb3)
        if angulo is None:
            return False
        return (angulo_llano - threshold) <= angulo <= (angulo_llano + threshold)

class UserPose:
    eye_level = CAM_HEIGHT // 100

    def __init__(self): # (self, keypoints)
        self.actual_state = ''
        self.actual_sequence = ''
        # Obtener KPS por algun metodo que haga de Traductor > Modelo : KPs
        self.kps = KeypointsHandler()
        self.cam = False
        self.suelo = None
        self.enpie = False
        self.tumbado_boca_arriba = False
        self.tumbado_bocabajo = False
        self.pino = False

    # Establecer secuencia
    def set_sequence(self, sequence):
        self.actual_sequence = sequence

    # Establecer postura
    def set_pose(self, pose):
        self.actual_state = pose

    # Actualizar KPs
    def update_keypoints(self, keypoints):
        self.kps.update_keypoints(keypoints)
    
    # Calculo del angulo entre 3 puntos
    def calcular_angulo(punto1: list, punto2: list, punto3: list) -> float:
        """
        Calcula el ángulo entre dos líneas en 2D definidas por tres puntos.
        Args:
            punto1: Tuple o lista con las coordenadas (x, y) del primer punto.
            punto2: Tuple o lista con las coordenadas (x, y) del segundo punto.
            punto3: Tuple o lista con las coordenadas (x, y) del tercer punto.

        Returns:
            El ángulo en grados entre las dos líneas.
        """
        # Calcular vectores
        vector1 = (punto2[0] - punto1[0], punto2[1] - punto1[1])
        vector2 = (punto3[0] - punto2[0], punto3[1] - punto2[1])
        # Producto escalar
        producto_escalar = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        # Magnitudes de los vectores
        magnitud_vector1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
        magnitud_vector2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
        # Coseno del ángulo
        coseno_angulo = producto_escalar / (magnitud_vector1 * magnitud_vector2)
        # Ángulo en grados
        angulo = math.acos(coseno_angulo) * 180 / math.pi
        return angulo
    
    # Determinar si 3 puntos(X o Y) estan alineados horizontal/verticalmente
    def casi_horizontal_casi_vertical(p1: int, p2: int, p3: int, threshold: int) -> bool:
        return abs(p1 - p2) <= threshold and abs(p2 - p3) <= threshold

    # Determinar si user esta mirando a cam
    def looking_2_camera(self) -> bool:
        self.cam = False
        ojo_dcho = self.kps.get_keypoint(t_ojod)
        ojo_izdo = self.kps.get_keypoint(t_ojoi)
        if ojo_izdo and ojo_dcho and abs(ojo_izdo[1] - ojo_dcho[1]) < self.eye_level:
            self.cam = True
        return self.cam

    # Setear el suelo
    def update_floor_for_pose(self, pose_kps: list) -> None:
        if not pose_kps:
            return
        self.suelo = pose_kps[1]

    # Determinar si Extremidad esta recta (limb1 inicio, limb2 medio, limb3 punto final)
 


    # Determinar como se encuentra el cuerpo
    def update_body_status(self) -> None:
        nariz = self.kps.get_keypoint(t_nariz)
        oreja_izda = self.kps.get_keypoint(t_orejai)
        hombro_izdo = self.kps.get_keypoint(t_hombroi)
        cadera_izda = self.kps.get_keypoint(t_caderai)
        tobillo_izdo = self.kps.get_keypoint(t_tobilloi)
        self.enpie = False
        self.tumbado_boca_arriba = False
        self.tumbado_bocabajo = False
        self.pino = False
        print(nariz)
        if nariz[1] < cadera_izda[1] < tobillo_izdo[1]:
            self.enpie = True
        if hombro_izdo[1] == cadera_izda[1] == tobillo_izdo[1] and nariz[1] < oreja_izda[1]:
            self.tumbado_boca_arriba = True
        if hombro_izdo[1] == cadera_izda[1] == tobillo_izdo[1] and nariz[1] > oreja_izda[1]:
            self.tumbado_bocabajo = True
        if nariz[1] > cadera_izda[1] > tobillo_izdo[1]:
            self.pino = True

    def pies_dentro_hombros(hombro_dcho: list, hombro_izdo: list, tobillo_dcho: list, tobillo_izdo: list) -> bool:
        return ((hombro_izdo[0] - tobillo_izdo[0]) > 0) and ((hombro_dcho[0] - tobillo_dcho[0]) < 0)

    # Menu de posturas
    def postura(self, postura):
    ### DEFINIR utilizando la función 'sublista' de basic.py
    ### posturas = sublista(TRANSICIONES, "Saludo al sol")
    ### Habrá que obtener en la entrada de la función la SECUENCIA
    ### sobre la que trabajamos
        pose_dict = {
            'Tadasana': self.tadasana(),
            'Urdhva Hastasana': self.urdhva_hastasana(),
            'Uttanasana': self.uttanasana(),
            'Ardha Uttanasana': self.ardha_uttanasana(),
            'Chaturanga Dandasana': self.chaturanga_dandasana(),
            'Urdhva Mukha Svanasana': self.urdhva_mukha_svanasana(),
            'Adho Mukha Svanasana': self.adho_mukha_svanasana()
            }
        return pose_dict[postura]

    # Determinar si la postura TADASANA esta correcta
    def tadasana(self):
        # Definir partes clave para postura
        hombro_dcho = self.kps.get_keypoint(t_hombrod)
        hombro_izdo = self.kps.get_keypoint(t_hombroi)
        codo_dcho = self.kps.get_keypoint(t_codod)
        codo_izdo = self.kps.get_keypoint(t_codoi)
        muneca_dcha = self.kps.get_keypoint(t_munecad)
        muneca_izda = self.kps.get_keypoint(t_munecai)
        tobillo_dcho = self.kps.get_keypoint(t_tobillod)
        tobillo_izdo = self.kps.get_keypoint(t_tobilloi)
        # Definir diferentes States Clave de postura
        tadasana_brazo_dcho = False
        tadasana_brazo_izdo = False
        tadasana_pies_hombros = False
        self.update_body_status()
        if self.enpie:
            tadasana_brazo_dcho = self.limb_straight(hombro_dcho, codo_dcho, muneca_dcha, LIMB_STRAIGHT_ANGLE)
            tadasana_brazo_izdo = self.limb_straight(hombro_izdo, codo_izdo, muneca_izda, LIMB_STRAIGHT_ANGLE)
            tadasana_pies_hombros = self.pies_dentro_hombros(hombro_izdo, hombro_dcho, tobillo_izdo, tobillo_dcho)
        return tadasana_brazo_dcho and tadasana_brazo_izdo and tadasana_pies_hombros

    def urdhva_hastasana(self):
        # brazos arriba > codos altura de hombros
        # cadera hacia rodilla + hombros mas distancia de caderas
        # muneca juntas
        # inclinacion angulo oreja nariz > cabeza mirando hacia arriba
        # pies dentro hombros == tadasana >> hacer FT
        print("urdhva_hastasana")

    def uttanasana(self):
        # manos Y == tobillo
        # brazos rectos
        # rodilla - cadera - hombro > Angulo de amplio aspecto
        # pies dentro hombros == tadasana >> hacer FT
        # **** cabeza ombligo > ojo oreja por debajo nivel flotacion
        print("uttanasana")

    def ardha_uttanasana(self):
        # comprobar angulo tobillo - cadera - hombro < 90 (+ umbral hasta 45)
        # straight > cadera, hombro, oreja (izda)
        # muneca en "area": "hombro" - "tobillo"
        print("ardha_uttanasana")

    def chaturanga_dandasana(self):
        # muneca Y == tobillo
        # hombro - codo - muneca > 90 grados
        # hombro - cadera > Linea > codo pegado
        # hombro - rodilla - tobillo > RECTAS
        # oreja - nariz > mire hacia "delante"
        print("chaturanga_dandasana")

    def urdhva_mukha_svanasana(self):
        # brazo recto
        # muneca Y por debajo de Tobillo + hombro Y por encima de Tobillo
        # oreja o nariz por encima de hombro
        # oreja - nariz > mire hacia "arriba"
        # eje X: por orden, nariz < hombro < cadera < rodilla < tobillo
        print("urdhva_mukha_svanasana")

    def adho_mukha_svanasana(self):
        # cadera Y sea lo que esta mas arriba
        # cadera - hombro - muneca > recta
        # muneca Y por debajo de Tobillo
        print("adho_mukha_svanasana")

    def transicionar_a_nueva_postura(self, new_pose):
        if new_pose in TRANSICIONES[self.actual_sequence][self.actual_state]:
            self.actual_state = new_pose

################################################################################################################
################################################################################################################
################################################################################################################

# postura_usuario = UserPose()

# seleccion = 'Tadasana' # st.sliderbox()
# postura_usuario.set_pose(seleccion)

# # Ejemplo de 1 Frame
# kps_input = {
#     'nariz': [(325.0830), (335.0106)],
#     'ojo_izdo': [(347.7314), (322.9567)],
#     'ojo_dcho': [(317.7649), (320.4380)],
#     'oreja_izda': [(390.0474), (343.0667)],
#     'oreja_dcha': [(0.), (0.)],
#     'hombro_izdo': [(408.5303),(436.8804)],
#     'hombro_dcho': [(312.1650), (440.9208)],
#     'codo_izdo': [(443.8503), (531.5388)],
#     'codo_dcho': [(295.6314), (553.2158)],
#     'muneca_izda': [(496.4920), (638.1014)],
#     'muneca_dcha': [(269.3600), (649.3030)],
#     'cadera_izda': [(378.1819), (658.8590)],
#     'cadera_dcha': [(317.2220), (658.2573)],
#     'rodilla_izda': [(382.8687), (851.3861)],
#     'rodilla_dcha': [(338.8528), (842.0581)],
#     'tobillo_izdo': [(388.1775), (1023.7861)],
#     'tobillo_dcho': [(364.8663), (1012.7568)]
#     }

# for parte, kps in kps_input.items():
#     setattr(postura_usuario, parte, kps)

# Imprimir los valores asignados
# print(f"Nariz: {postura_usuario.nariz}")
# print(f"Ojo izquierdo: {postura_usuario.ojo_izdo}")
# print(f"Ojo derecho: {postura_usuario.ojo_dcho}")
# print(f"Oreja izquierda: {postura_usuario.oreja_izda}")
# print(f"Oreja derecha: {postura_usuario.oreja_dcha}")
# print(f"Hombro izquierdo: {postura_usuario.hombro_izdo}")
# print(f"Hombro derecho: {postura_usuario.hombro_dcho}")
# print(f"Codo izquierdo: {postura_usuario.codo_izdo}")
# print(f"Codo derecho: {postura_usuario.codo_dcho}")
# print(f"Muñeca izquierda: {postura_usuario.muneca_izda}")
# print(f"Muñeca derecha: {postura_usuario.muneca_dcha}")
# print(f"Cadera izquierda: {postura_usuario.cadera_izda}")
# print(f"Cadera derecha: {postura_usuario.cadera_dcha}")
# print(f"Rodilla izquierda: {postura_usuario.rodilla_izda}")
# print(f"Rodilla derecha: {postura_usuario.rodilla_dcha}")
# print(f"Tobillo izquierdo: {postura_usuario.tobillo_izdo}")
# print(f"Tobillo derecho: {postura_usuario.tobillo_dcho}")

# if postura_usuario.name == 'Tadasana':
#     # postura_usuario.init_de_pie()
#     while postura_usuario.check_tadasana() == False:
#         print("Corrige postura, IMBECIL! Samanté")
#         postura_usuario.tadasana()
#     print("Tadasana COMPLETE!!! MADAFAKA!")