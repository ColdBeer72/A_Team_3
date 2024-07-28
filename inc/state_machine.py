import numpy as np
import math

class UserPose:
    def __init__(self):
        self.name = ''
        self.nariz = None
        self.ojo_izdo = None
        self.ojo_dcho = None
        self.oreja_izda = None
        self.oreja_dcha = None
        self.hombro_izdo = None
        self.hombro_dcho = None
        self.codo_izdo = None
        self.codo_dcho = None
        self.muneca_izda = None
        self.muneca_dcha = None
        self.cadera_izda = None
        self.cadera_dcha = None
        self.rodilla_izda = None
        self.rodilla_dcha = None
        self.tobillo_izdo = None
        self.tobillo_dcho = None
        self.cam = False
        self.suelo = None
        self.enpie = False
        self.tumbado_boca_arriba = False
        self.tumbado_bocabajo = False
        self.tadasana_state = False
        self.pino = False

    # Establecer postura
    def set_pose(self, pose):
        self.name = pose

    # Actualizar keypoints
    def update_keypoints(self, keypoints):
        for key, value in keypoints.items():
            setattr(self, key, value)

    # Determinar si user esta mirando a cam
    def looking_to_camera(self):
        self.cam = False
        if self.ojo_izdo and self.ojo_dcho:
            # Check de [1] "altura de ojos"
            if abs(self.ojo_izdo[1] - self.ojo_dcho[1]) < 10:
                self.cam = True
        return self.cam

    # Setear el suelo para cada postura
    def update_floor_for_pose(self, pose_kps):
        if not pose_kps:
            return
        self.suelo = pose_kps[1]

    # Determinar si se esta de pie
    def update_body_status(self):
        self.enpie = False
        self.tumbado_boca_arriba = False
        self.tumbado_bocabajo = False
        self.pino = False
        if self.nariz and self.tobillo_izdo:
            if self.nariz[1] < self.cadera_izda[1] < self.tobillo_izdo[1]:
                print(self.tobillo_izdo[1])
                self.update_floor_for_pose(self.tobillo_izdo)
                self.enpie = True
            if self.hombro_izdo[1] == self.cadera_izda[1] == self.tobillo_izdo[1] and self.nariz[1] < self.oreja_izda[1]:
                self.update_floor_for_pose(self.tobillo_izdo)
                self.tumbado_boca_arriba = True
            if self.hombro_izdo[1] == self.cadera_izda[1] == self.tobillo_izdo[1] and self.nariz[1] > self.oreja_izda[1]:
                self.update_floor_for_pose(self.nariz)
                self.tumbado_bocabajo = True
            if self.nariz[1] > self.cadera_izda[1] > self.tobillo_izdo[1]:
                self.update_floor_for_pose(self.muneca_izda)
                self.pino = True
        
    # Determinar si Extremidad esta recta (limb1 inicio, limb2 medio, limb3 punto final)
    def limb_straight(self, limb1, limb2, limb3):
        umbral = 3
        if limb1 and limb2 and limb3:
            x1, y1 = limb1
            x2, y2 = limb2
            x3, y3 = limb3
            if (x1 > x2 > x3 or x1 < x2 < x3) and (y1 > y2 > y3 or y1 < y2 < y3):
                # Check recto vertical/ horizontal
                if x1 == x2 == x3 or y1 == y2 == y3:
                    return True
                try:
                    # Calculo de pendiente entre p1-p2 y entre p2-p3
                    m1 = abs((y2 - y1) / (x2 - x1))
                    m2 = abs((y3 - y2) / (x3 - x2))
                    return abs(m1 - m2) < umbral
                except ZeroDivisionError:
                    return False
        return False

    # Determinar si la postura de la montaña esta correcta
    def tadasana(self):
        self.tadasana_state = False
        self.update_body_status()
        if self.enpie:
            tadasana_brazo_dcho = self.limb_straight(self.hombro_dcho, self.codo_dcho, self.muneca_dcha)
            tadasana_brazo_izdo = self.limb_straight(self.hombro_izdo, self.codo_izdo, self.muneca_izda)
            tadasana_pies_hombros = ((self.hombro_izdo[0] - self.tobillo_izdo[0]) > 0) and ((self.hombro_dcho[0] - self.tobillo_dcho[0]) < 0)
            self.tadasana_state = tadasana_brazo_dcho and tadasana_brazo_izdo and tadasana_pies_hombros
        return self.tadasana_state

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