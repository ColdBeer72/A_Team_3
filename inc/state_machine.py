import math
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
    def three_points_straight(limb1: list, limb2: list, limb3: list, threshold = UMBRALES.THREE_POINT_STRAIGHT) -> bool:
        angulo = Pose_Calculator.calcular_angulo(limb1, limb2, limb3)
        if angulo is None:
            return False
        return (threshold[0] >= angulo >= threshold[1])

    @staticmethod
    # Determinar si 3 puntos(X o Y) estan alineados horizontal/verticalmente
    def casi_horizontal_casi_vertical(p1: int, p2: int, p3: int, threshold: int) -> bool:
        return (abs(p1 - p2) <= threshold and abs(p2 - p3) <= threshold)

    @staticmethod
    def pies_dentro_hombros(hombro_dcho: list, hombro_izdo: list, tobillo_dcho: list, tobillo_izdo: list) -> bool:
        return ((hombro_izdo[0] - tobillo_izdo[0]) > 0) and ((hombro_dcho[0] - tobillo_dcho[0]) < 0)

    @staticmethod
    def manos_juntas(muneca_dcha: list, muneca_izda: list) -> bool:
        # Checkear el 20X e 10Y si es correcto.
        return (abs(muneca_dcha[0] - muneca_izda[0]) <= UMBRALES.MANOS_JUNTAS[0] and abs(muneca_dcha[1] - muneca_izda[1]) <= UMBRALES.MANOS_JUNTAS[1])

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
        self.user_state = False
        self.kps = KeypointsHandler()
        self.cam = False
        self.suelo = None
        self.enpie = False
        self.tumbado_boca_arriba = False
        self.tumbado_bocabajo = False
        self.pino = False

    # Establecer posicion "semaforo"
    def update_state(self, state):
        self.user_state = state

    # Establecer postura
    def set_pose(self, pose):
        self.actual_state = pose

    # Establecer secuencia
    def set_sequence(self, sequence):
        self.actual_sequence = sequence
    
    # Actualizar KPs
    def update_keypoints(self, keypoints):
        self.kps.update_kps(keypoints)

    # Determinar si user esta mirando a cam
    def looking_2_camera(self) -> bool:
        self.cam = False
        # Definir partes clave para postura
        key_body_parts = [t_ojod, t_ojoi]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            ojo_dcho, ojo_izdo = puntos_clave
            if ojo_izdo and ojo_dcho and abs(ojo_izdo[1] - ojo_dcho[1]) < self.eye_level:
                self.cam = True
        return self.cam

    # Setear el suelo
    def update_floor_for_pose(self, pose_kps: list) -> None:
        if pose_kps:
            self.suelo = pose_kps[1]

    # Determinar como se encuentra el cuerpo
    def update_body_status(self) -> None:
        self.enpie = False
        self.tumbado_boca_arriba = False
        self.tumbado_bocabajo = False
        self.pino = False
        # Definir partes clave para postura
        key_body_parts = [t_nariz, t_orejai, t_hombroi, t_caderai, t_tobilloi]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            nariz, oreja_izda, hombro_izdo, cadera_izda, tobillo_izdo = puntos_clave
            if nariz[1] < cadera_izda[1] < tobillo_izdo[1]:
                self.enpie = True
            if hombro_izdo[1] == cadera_izda[1] == tobillo_izdo[1] and nariz[1] < oreja_izda[1]:
                self.tumbado_boca_arriba = True
            if hombro_izdo[1] == cadera_izda[1] == tobillo_izdo[1] and nariz[1] > oreja_izda[1]:
                self.tumbado_bocabajo = True
            if nariz[1] > cadera_izda[1] > tobillo_izdo[1]:
                self.pino = True

    # Menu de posturas
    def postura(self):
    ### DEFINIR utilizando la función 'sublista' de basic.py
    ### posturas = sublista(TRANSICIONES, "Saludo al sol")
    ### Habrá que obtener en la entrada de la función la SECUENCIA
    ### sobre la que trabajamos
        postura = self.actual_state
        pose_dict = {
            'Urdhva Hastasana': self.urdhva_hastasana,
            'Uttanasana': self.uttanasana,
            'Tadasana': self.tadasana,
            'Ardha Uttanasana': self.ardha_uttanasana,
            'Chaturanga Dandasana': self.chaturanga_dandasana,
            'Urdhva Mukha Svanasana': self.urdhva_mukha_svanasana,
            # 'Adho Mukha Svanasana': self.test
            'Adho Mukha Svanasana': self.adho_mukha_svanasana           
            }
        return pose_dict[postura]()

    # Pose TEST
    def test(self) -> bool:
        pose_ok = False
        # Definir partes clave para postura
        key_body_parts = [t_nariz, t_orejad]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            nariz, oreja_dcha = puntos_clave
            # Asegurarse de que los keypoints no sean None antes de usarlos
            if nariz and oreja_dcha:
                if nariz[1] < oreja_dcha[1]:
                    pose_ok = True
        return pose_ok

    # Determinar si la postura TADASANA esta correcta
    def tadasana(self) -> bool:
        # Definir diferentes States Clave de postura
        brazos_rectos = False
        pies_hombros = False
        # Definir partes clave para postura
        key_body_parts = [t_hombrod, t_hombroi, t_codod, t_codoi, t_munecad, t_munecai, t_tobillod, t_tobilloi]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            hombro_dcho, hombro_izdo, codo_dcho, codo_izdo, muneca_dcha, muneca_izda, tobillo_dcho, tobillo_izdo = puntos_clave   
            # Check de States
            self.update_body_status()
            if self.enpie:
                brazos_rectos = (Pose_Calculator.three_points_straight(hombro_dcho, codo_dcho, muneca_dcha) and 
                            Pose_Calculator.three_points_straight(hombro_izdo, codo_izdo, muneca_izda))
                pies_hombros = Pose_Calculator.pies_dentro_hombros(hombro_dcho, hombro_izdo, tobillo_dcho, tobillo_izdo)
        return brazos_rectos and pies_hombros

    # Determinar si la postura URDHVA HASTASANA esta correcta
    def urdhva_hastasana(self) -> bool:
        # Definir States Urdhva_Hastasana
        manos_juntas_arriba = False
        pies_hombros = False
        brazos_arriba = False
        # Definir partes clave para postura
        key_body_parts = [t_hombrod, t_hombroi, t_codod, t_codoi, t_munecad, t_munecai, t_tobillod, t_tobilloi]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            hombro_dcho, hombro_izdo, codo_dcho, codo_izdo, muneca_dcha, muneca_izda, tobillo_dcho, tobillo_izdo = puntos_clave
            # Check de States
            self.update_body_status()
            if self.enpie:
                brazos_arriba = muneca_izda[1] < codo_izdo[1] < hombro_izdo[1]\
                        and muneca_dcha[1] < codo_dcho[1] < hombro_dcho[1]
                manos_juntas_arriba = Pose_Calculator.manos_juntas(muneca_dcha, muneca_izda)\
                                    and brazos_arriba
                pies_hombros = Pose_Calculator.pies_dentro_hombros(hombro_dcho, hombro_izdo, tobillo_dcho, tobillo_izdo)
        return manos_juntas_arriba and pies_hombros

    # Determinar si la postura UTTANASANA esta correcta
    def uttanasana(self) -> bool:
        # Definir States Uttanasana
        manos_suelo = False
        brazos_rectos = False
        pies_hombros = False
        cabeza_ombligo = False
        # Definir partes clave para postura
        key_body_parts = [t_munecad, t_munecai, t_tobillod, t_tobilloi, t_hombrod, t_hombroi, t_codod, t_codoi, t_ojoi, t_orejai, t_rodillad, t_rodillai]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            muneca_dcha, muneca_izda, tobillo_dcho, tobillo_izdo, hombro_dcho, hombro_izdo, codo_dcho, codo_izdo, ojo_izdo, oreja_izda, rodilla_dcha, rodilla_izda = puntos_clave
            # Check de States
            manos_suelo = (abs(muneca_izda[1] - tobillo_izdo[1]) <= 10 or (muneca_izda[1] >= tobillo_izdo[1]))\
                    and (abs(muneca_dcha[1] - tobillo_dcho[1]) <= 10 or (muneca_dcha[1] >= tobillo_dcho[1]))
            # brazos_rectos = Pose_Calculator.three_points_straight(hombro_izdo, codo_izdo, muneca_izda)\
            #             and Pose_Calculator.three_points_straight(hombro_dcho, codo_dcho, muneca_dcha)
            pies_hombros = abs(muneca_dcha[0] - tobillo_izdo[0]) <= 60
            cabeza_ombligo = oreja_izda[1] < ojo_izdo[1]
        return manos_suelo and pies_hombros and cabeza_ombligo

    # Determinar si la postura ARDHA UTTANASANA esta correcta
    def ardha_uttanasana(self) -> bool:
        # Definir States Ardha_Uttanasana
        angulo_cuerpo = False
        espalda_recta = False
        manos = False
        # Definir partes clave para postura
        key_body_parts = [t_tobilloi, t_caderai, t_hombroi, t_orejai, t_munecad, t_munecai, t_rodillai, t_hombrod, t_tobillod, t_rodillad]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            tobillo_izdo, cadera_izda, hombro_izdo, oreja_izda, muneca_dcha, muneca_izda, rodilla_izda, hombro_dcho, tobillo_dcho, rodilla_dcha = puntos_clave
            # Corrección sobre Predict Modelo y Posición real de hombro
            hombro_dcho[0] = hombro_dcho[0] - UMBRALES.HOMBRO_DCHO_TAPADO_CARA_ARDHA
            # Check de States
            angulo_cuerpo = (Pose_Calculator.calcular_angulo(tobillo_izdo, cadera_izda, hombro_izdo) <= UMBRALES.ANGULO_CUERPO_ARDHA_UTTANASANA)
            espalda_recta = Pose_Calculator.three_points_straight(cadera_izda, hombro_izdo, oreja_izda)
            manos =  Pose_Calculator.mano_safe_zone(muneca_izda, hombro_izdo, tobillo_izdo, rodilla_izda)\
                and Pose_Calculator.mano_safe_zone(muneca_dcha, hombro_dcho, tobillo_dcho, rodilla_dcha)
        return angulo_cuerpo and espalda_recta and manos

    # Determinar si la postura CHATURANGA DANDASANA esta correcta
    def chaturanga_dandasana(self) -> bool:
        # Definir States Chaturanga Dandasana
        manos_suelo = False
        brazos_90 = False
        codo_pegado = False
        espalda_recta = False
        # Definir partes clave para postura
        key_body_parts = [t_munecai, t_tobilloi, t_hombrod, t_hombroi, t_codoi, t_caderai]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave        
            muneca_izda, tobillo_izdo, hombro_dcho, hombro_izdo, codo_izdo, cadera_izda = puntos_clave
            # Check de States
            manos_suelo = muneca_izda[1] >= tobillo_izdo[1]
            brazos_90 = UMBRALES.BRAZOS_90_CHATURANGA[0] >= Pose_Calculator.calcular_angulo(hombro_izdo, codo_izdo, muneca_izda) >= UMBRALES.BRAZOS_90_CHATURANGA[1]
            codo_pegado = Pose_Calculator.calcular_distancia_punto_segmento(codo_izdo, hombro_izdo, cadera_izda) <= UMBRALES.DIST_CODO_CHATURANGA
            espalda_recta = Pose_Calculator.do_lines_intersect(tobillo_izdo, cadera_izda, hombro_izdo, hombro_dcho)
        return manos_suelo and brazos_90 and codo_pegado and espalda_recta
    
    # Determinar si la postura URDHVA MUKHA SVANASANA esta correcta
    def urdhva_mukha_svanasana(self) -> bool:
        # Definir States Urdhva Mukha Svanasana
        brazos_rectos = False
        muneca_hombros = False
        cabeza_arriba = False
        orientacion_cabeza = False
        orden_cuerpo = False
        # Definir partes clave para postura
        key_body_parts = [t_munecad, t_munecai, t_codod, t_codoi, t_hombrod, t_hombroi, t_tobilloi, t_nariz, t_caderai, t_rodillai, t_ojoi]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            muneca_dcha, muneca_izda, codo_dcho, codo_izdo, hombro_dcho, hombro_izdo, tobillo_izdo, nariz, cadera_izda, rodilla_izda, ojo_izdo = puntos_clave
            # Check de States
            brazos_rectos =  Pose_Calculator.three_points_straight(muneca_dcha, codo_dcho, hombro_dcho)\
                        and Pose_Calculator.three_points_straight(muneca_izda, codo_izdo, hombro_izdo)
            muneca_hombros =  muneca_izda[1] > tobillo_izdo[1] > hombro_izdo[1]
            cabeza_arriba = nariz[1] < hombro_izdo[1]
            orientacion_cabeza =  (abs(nariz[1] - ojo_izdo[1]) < UMBRALES.ORIENTACION_CABEZA_URDHVA_MUKHA)
            orden_cuerpo = nariz[0] < hombro_izdo[0] < cadera_izda[0] < rodilla_izda[0] < tobillo_izdo[0]
        return brazos_rectos and muneca_hombros and cabeza_arriba and orientacion_cabeza and orden_cuerpo

    # Determinar si la postura ADHO MUKHA SVANASANA esta correcta
    def adho_mukha_svanasana(self) -> bool:
        # Definir States Adho Mukha Svanasana
        cadera_arriba_y_manos_suelo = False
        espalda_recta = False
        # Definir partes clave para postura
        key_body_parts = [t_caderai, t_hombroi, t_munecai, t_tobilloi]
        # Key Body Parts con sus KPs
        puntos_clave = [self.kps.get_keypoint(parte) for parte in key_body_parts]
        if all(puntos_clave):
            # Desempaquetar los puntos clave
            cadera_izda, hombro_izdo, muneca_izda, tobillo_izdo = puntos_clave
            # Check de States
            cadera_arriba_y_manos_suelo = cadera_izda[1] < tobillo_izdo[1] < muneca_izda[1]
            espalda_recta =  Pose_Calculator.three_points_straight(cadera_izda, hombro_izdo, muneca_izda, UMBRALES.ESPALDA_RECTA_ADHO_MUKHA_SVANA)
        return cadera_arriba_y_manos_suelo and espalda_recta

    def transicionar_a_nueva_postura(self, new_pose):
        if new_pose in TRANSICIONES[self.actual_sequence][self.actual_state]:
            self.actual_state = new_pose