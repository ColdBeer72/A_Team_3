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
    def update_kps(self, keypoints: dict) -> None:
        for key, value in keypoints.items():
            try:
                self.keypoints[key] = value
            except:
                continue

    # Metodo para obtener KPs
    def get_keypoint(self, name: str) -> list:
        return self.keypoints.get(name)



class Pose_Calculator:
    @staticmethod
    def calcular_angulo(punto1: list, punto2: list, punto3: list) -> float:
        try:
            # Vectores a partir de los puntos
            vector1 = (punto2[0] - punto1[0], punto2[1] - punto1[1])
            vector2 = (punto3[0] - punto2[0], punto3[1] - punto2[1])
            # Producto escalar
            producto_escalar = vector1[0] * vector2[0] + vector1[1] * vector2[1]
            # Magnitudes de los vectores
            magnitud_vector1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
            magnitud_vector2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
            # Si cualquiera de las magnitudes es cero, los puntos no forman un ángulo definido.
            if magnitud_vector1 == 0 or magnitud_vector2 == 0:
                return None
            # Coseno del ángulo
            coseno_angulo = producto_escalar / (magnitud_vector1 * magnitud_vector2)
            # Asegurarse de que el coseno esté en el rango [-1, 1]
            coseno_angulo = max(-1, min(1, coseno_angulo))
            # Ángulo en grados
            angulo = math.acos(coseno_angulo) * 180 / math.pi
            # Asegurarse de que siempre retornemos el ángulo agudo
            return round(180 - angulo, 2)
        except ZeroDivisionError:
            return None

    @staticmethod
    # Saber si 3 puntos estan rectos
    def three_points_straight(limb1: list, limb2: list, limb3: list, threshold: int) -> bool:
        angulo_llano = 180
        angulo = Pose_Calculator.calcular_angulo(limb1, limb2, limb3)
        if angulo is None:
            return False
        return (angulo_llano - threshold) <= angulo <= (angulo_llano + threshold)

    @staticmethod
    # Determinar si 3 puntos(X o Y) estan alineados horizontal/verticalmente
    def casi_horizontal_casi_vertical(p1: int, p2: int, p3: int, threshold: int) -> bool:
        return abs(p1 - p2) <= threshold and abs(p2 - p3) <= threshold

    @staticmethod
    def pies_dentro_hombros(hombro_dcho: list, hombro_izdo: list, tobillo_dcho: list, tobillo_izdo: list) -> bool:
        return ((hombro_izdo[0] - tobillo_izdo[0]) > 0) and ((hombro_dcho[0] - tobillo_dcho[0]) < 0)

    @staticmethod
    def manos_juntas(muneca_dcha: list, muneca_izda: list) -> bool:
        # Checkear el 20X e 10Y si es correcto.
        return (abs(muneca_dcha[0] - muneca_izda[0]) <= 20 and abs(muneca_dcha[1] - muneca_izda[1]) <= 10)

    @staticmethod
    def calcular_distancia_punto_segmento(punto: list, linea_a: list, linea_b: list) -> float:
        # Coordenadas del punto y del segmento
        x0, y0 = punto
        x1, y1 = linea_a
        x2, y2 = linea_b
        # Vector del segmento AB y del punto A al punto C
        ABx, ABy = x2 - x1, y2 - y1
        ACx, ACy = x0 - x1, y0 - y1
        # Proyección escalar t
        t = (ACx * ABx + ACy * ABy) / (ABx**2 + ABy**2)
        if t < 0:
            # El punto más cercano es A
            nearest_x, nearest_y = x1, y1
        elif t > 1:
            # El punto más cercano es B
            nearest_x, nearest_y = x2, y2
        else:
            # La proyección cae dentro del segmento
            nearest_x = x1 + t * ABx
            nearest_y = y1 + t * ABy
        # Calcular la distancia desde C al punto más cercano en el segmento AB
        distancia = math.sqrt((x0 - nearest_x) ** 2 + (y0 - nearest_y) ** 2)
        distancia = round(distancia, 3)
        return distancia

    @staticmethod
    def do_lines_intersect(proyeccion1: list, proyeccion2: list, linea_inicio: list, linea_fin: list) -> bool:
        # Desempaquetar puntos
        x1, y1 = proyeccion1
        x2, y2 = proyeccion2
        x3, y3 = linea_inicio
        x4, y4 = linea_fin
        # Coeficientes para la línea AB
        dx1 = x2 - x1
        dy1 = y2 - y1
        # Coeficientes para la línea CD
        dx2 = x4 - x3
        dy2 = y4 - y3
        # Determinante para las ecuaciones paramétricas
        det = dx1 * dy2 - dy1 * dx2
        # Si el determinante es cero, las líneas son paralelas
        if det == 0:
            return False
        # Cálculo de los parámetros t y s
        dx3 = x3 - x1
        dy3 = y3 - y1
        t = (dx3 * dy2 - dy3 * dx2) / det
        s = (dx1 * dy3 - dy1 * dx3) / det
        # Verificar si la intersección está en el rango de la línea infinita
        if 0 <= t:
            return True
        return False
    
    @staticmethod
    def mano_safe_zone(muneca: list, hombro_izdo: list, tobillo_izdo: list, rodilla_izda: list) -> bool:
        mx, my = muneca
        hx, _ = hombro_izdo
        tx, _ = tobillo_izdo
        _, ry = rodilla_izda
        margen_izdo = hx
        margen_dcho = tx
        margen_sup = ry
        return ((margen_izdo <= mx <= margen_dcho) and (margen_sup <= my))

class UserPose:
    eye_level = CAM_HEIGHT // 100

    def __init__(self):
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
        self.kps.update_kps(keypoints)

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

    # Menu de posturas
    def postura(self, postura):
    ### DEFINIR utilizando la función 'sublista' de basic.py
    ### posturas = sublista(TRANSICIONES, "Saludo al sol")
    ### Habrá que obtener en la entrada de la función la SECUENCIA
    ### sobre la que trabajamos
        pose_dict = {
            'Urdhva Hastasana': self.urdhva_hastasana,
            'Uttanasana': self.uttanasana,
            'Tadasana': self.tadasana,
            'Ardha Uttanasana': self.ardha_uttanasana,
            'Chaturanga Dandasana': self.chaturanga_dandasana,
            'Urdhva Mukha Svanasana': self.urdhva_mukha_svanasana,
            'Adho Mukha Svanasana': self.adho_mukha_svanasana
            }
        return pose_dict[postura]()

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
        tadasana_brazos_rectos = False
        tadasana_pies_hombros = False
        # Check de States
        self.update_body_status()
        if self.enpie:
            tadasana_brazo_dcho = Pose_Calculator.three_points_straight(hombro_dcho, codo_dcho, muneca_dcha, LIMB_STRAIGHT_ANGLE)
            tadasana_brazo_izdo = Pose_Calculator.three_points_straight(hombro_izdo, codo_izdo, muneca_izda, LIMB_STRAIGHT_ANGLE)
            tadasana_pies_hombros = Pose_Calculator.pies_dentro_hombros(hombro_izdo, hombro_dcho, tobillo_izdo, tobillo_dcho)
        if tadasana_brazo_dcho and tadasana_brazo_izdo:
            tadasana_brazos_rectos = True
        return tadasana_brazos_rectos and tadasana_pies_hombros

    # Determinar si la postura URDHVA HASTASANA esta correcta
    def urdhva_hastasana(self):
        # Definir partes clave para postura
        hombro_dcho = self.kps.get_keypoint(t_hombrod)
        hombro_izdo = self.kps.get_keypoint(t_hombroi)
        codo_dcho = self.kps.get_keypoint(t_codod)
        codo_izdo = self.kps.get_keypoint(t_codoi)
        muneca_dcha = self.kps.get_keypoint(t_munecad)
        muneca_izda = self.kps.get_keypoint(t_munecai)
        tobillo_dcho = self.kps.get_keypoint(t_tobillod)
        tobillo_izdo = self.kps.get_keypoint(t_tobilloi)
        # Definir States Urdhva_Hastasana
        urdhva_hastasana_manos_juntas_arriba = False
        urdhva_hastasana_pies_hombros = False
        brazos_arriba = False
        # Check de States
        self.update_body_status()
        brazos_arriba = muneca_izda < codo_izdo < hombro_izdo and muneca_dcha < codo_dcho < hombro_dcho
        if self.enpie:
            urdhva_hastasana_manos_juntas_arriba = Pose_Calculator.manos_juntas(muneca_dcha, muneca_izda) and brazos_arriba
            urdhva_hastasana_pies_hombros = Pose_Calculator.pies_dentro_hombros(hombro_izdo, hombro_dcho, tobillo_izdo, tobillo_dcho)
        return urdhva_hastasana_manos_juntas_arriba and urdhva_hastasana_pies_hombros
        
    # Determinar si la postura UTTANASANA esta correcta
    def uttanasana(self):
        # Definir partes clave para postura
        muneca_dcha = self.kps.get_keypoint(t_munecad)
        muneca_izda = self.kps.get_keypoint(t_munecai)
        tobillo_dcho = self.kps.get_keypoint(t_tobillod)
        tobillo_izdo = self.kps.get_keypoint(t_tobilloi)
        hombro_dcho = self.kps.get_keypoint(t_hombrod)
        hombro_izdo = self.kps.get_keypoint(t_hombroi)
        codo_dcho = self.kps.get_keypoint(t_codod)
        codo_izdo = self.kps.get_keypoint(t_codoi)
        ojo_izdo = self.kps.get_keypoint(t_ojoi)
        oreja_izda = self.kps.get_keypoint(t_orejai)
        # Definir States Uttanasana
        uttanasana_manos_suelo = False
        uttanasana_brazos_rectos = False
        uttanasana_pies_hombros = False
        uttanasana_cabeza_ombligo = False
        # Check de States
        self.update_body_status()
        if self.enpie:
            uttanasana_manos_suelo = muneca_izda[1] > tobillo_izdo[1] and muneca_dcha[1] > tobillo_dcho[1]
            uttanasana_brazos_rectos = Pose_Calculator.three_points_straight(hombro_izdo, codo_izdo, muneca_izda) and Pose_Calculator.three_points_straight(hombro_dcho, codo_dcho, muneca_dcha)
            uttanasana_pies_hombros = Pose_Calculator.pies_dentro_hombros(hombro_izdo, hombro_dcho, tobillo_izdo, tobillo_dcho)
            uttanasana_cabeza_ombligo = oreja_izda[0] < ojo_izdo[0] and abs(oreja_izda[1] - ojo_izdo[1]) < 10
        return uttanasana_manos_suelo and uttanasana_brazos_rectos and uttanasana_pies_hombros and uttanasana_cabeza_ombligo
    
    # Determinar si la postura ARDHA UTTANASANA esta correcta
    def ardha_uttanasana(self):
        # Definir partes clave para postura
        tobillo_izdo = self.kps.get_keypoint(t_tobilloi)
        cadera_izda = self.kps.get_keypoint(t_caderai)
        hombro_izdo = self.kps.get_keypoint(t_hombroi)
        oreja_izda = self.kps.get_keypoint(t_orejai)
        muneca_dcha = self.kps.get_keypoint(t_munecad)
        muneca_izda = self.kps.get_keypoint(t_munecai)
        rodilla_izda = self.kps.get_keypoint(t_rodillai)
        # Definir States Ardha_Uttanasana
        ardha_uttanasana_angulo_cuerpo = False
        ardha_uttanasana_espalda_recta = False
        ardha_uttanasana_manos = False
        # Check de States
        ardha_uttanasana_angulo_cuerpo = Pose_Calculator.calcular_angulo(tobillo_izdo, cadera_izda, hombro_izdo) <= 90
        ardha_uttanasana_espalda_recta = Pose_Calculator.three_points_straight(cadera_izda, hombro_izdo, oreja_izda)
        ardha_uttanasana_manos =  (Pose_Calculator.mano_safe_zone(muneca_izda, hombro_izdo, tobillo_izdo, rodilla_izda) 
                                   and Pose_Calculator.mano_safe_zone(muneca_dcha, hombro_izdo, tobillo_izdo, rodilla_izda))
        return ardha_uttanasana_angulo_cuerpo and ardha_uttanasana_espalda_recta and ardha_uttanasana_manos

    # Determinar si la postura CHATURANGA DANDASANA esta correcta
    def chaturanga_dandasana(self):
        # Definir partes clave para postura
        muneca_izda = self.kps.get_keypoint(t_munecai)
        tobillo_izdo = self.kps.get_keypoint(t_tobilloi)
        hombro_dcho = self.kps.get_keypoint(t_hombrod)
        hombro_izdo = self.kps.get_keypoint(t_hombroi)
        codo_izdo = self.kps.get_keypoint(t_codoi)
        cadera_izda = self.kps.get_keypoint(t_caderai)
        # Definir States Chaturanga Dandasana
        chaturanga_dandasana_manos_suelo = False
        chaturanga_dandasana_brazos_90 = False
        chaturanga_dandasana_codo_pegado = False
        chaturanga_dandasana_espalda_recta = False
        # Check de States
        chaturanga_dandasana_manos_suelo = muneca_izda[1] >= tobillo_izdo[1]
            # Checkear traspasar los 90º a la perspectiva
        chaturanga_dandasana_brazos_90 = 100 > Pose_Calculator.calcular_angulo(hombro_izdo, codo_izdo, muneca_izda) > 80
        chaturanga_dandasana_codo_pegado = Pose_Calculator.calcular_distancia_punto_segmento(codo_izdo, hombro_izdo, cadera_izda) <= 25
        chaturanga_dandasana_espalda_recta = Pose_Calculator.do_lines_intersect(tobillo_izdo, cadera_izda, hombro_izdo, hombro_dcho)
        return chaturanga_dandasana_manos_suelo and chaturanga_dandasana_brazos_90 and chaturanga_dandasana_codo_pegado and chaturanga_dandasana_espalda_recta
    
    # Determinar si la postura URDHVA MUKHA SVANASANA esta correcta
    def urdhva_mukha_svanasana(self):
        # Definir partes clave para postura
        # Definir States Chaturanga Dandasana
        urdhva_mukha_svanasana_brazos_rectos = False
        urdhva_mukha_svanasana_muneca_hombros = False
        urdhva_mukha_svanasana_cabeza_arriba = False
        urdhva_mukha_svanasana_orientacion_cabeza = False
        urdhva_mukha_svanasana_orden_cuerpo = False
        # Check de States
        urdhva_mukha_svanasana_brazos_rectos = None # brazos recto
        urdhva_mukha_svanasana_muneca_hombros = None # muneca Y por debajo de Tobillo + hombro Y por encima de Tobillo
        urdhva_mukha_svanasana_cabeza_arriba = None # nariz por encima de hombro
        urdhva_mukha_svanasana_orientacion_cabeza = None # oreja - nariz > mire hacia "arriba"
        urdhva_mukha_svanasana_orden_cuerpo = None # eje X: por orden, nariz < hombro < cadera < rodilla < tobillo
        return urdhva_mukha_svanasana_brazos_rectos and urdhva_mukha_svanasana_muneca_hombros and urdhva_mukha_svanasana_cabeza_arriba and urdhva_mukha_svanasana_orientacion_cabeza and urdhva_mukha_svanasana_orden_cuerpo

    # Determinar si la postura ADHO MUKHA SVANASANA esta correcta
    def adho_mukha_svanasana(self):
        # cadera Y sea lo que esta mas arriba
        # cadera - hombro - muneca > recta
        # muneca Y por debajo de Tobillo
        adho_mukha_svanasana_cadera = False
        adho_mukha_svanasana_espalda_recta = False
        adho_mukha_svanasana_mano_suelo = False
        adho_mukha_svanasana_cadera = None
        adho_mukha_svanasana_espalda_recta = None
        adho_mukha_svanasana_mano_suelo = None
        return adho_mukha_svanasana_cadera and adho_mukha_svanasana_espalda_recta and adho_mukha_svanasana_mano_suelo

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