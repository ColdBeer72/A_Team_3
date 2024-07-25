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
        self.state = ''
        self.cam = False
        self.de_pie = False
        self.tadasana_state = False

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
        if self.ojo_izdo is not None and self.ojo_dcho is not None:
            # Check de [1] "altura de ojos"
            if abs(self.ojo_izdo[1] - self.ojo_dcho[1]) < 10:
                self.cam = True
    # Check de @looking_to_camera
    def check_camera(self):
        return self.cam

    # Determinar si se esta de pie
    def de_pie(self):
        self.de_pie = False
        if self.nariz is not None and self.cadera_izda is not None:
            if self.nariz[1] > self.cadera_izda[1]:
                self.de_pie = True
    
    # Check de @de_pie
    def check_de_pie(self):
        print(self.de_pie)
        return self.de_pie

    # Determinar si Extremidad esta recta (limb1 inicio, limb2 medio, limb3 punto final)
    def limb_straight(self, limb1, limb2, limb3):
        umbral = 1
        if limb1 is not None and limb2 is not None and limb3 is not None:
            x1, y1 = limb1
            x2, y2 = limb2
            x3, y3 = limb3
            # Check recto vertical
            if x1 == x2 == x3:
                return True
            # Check recto horizontal
            if y1 == y2 == y3:
                return True
            # Evitar dividir por 0
            if x2 == x1 or x3 == x2:
                return False
            # Calculo de pendiente entre p1-p2 y entre p2-p3
            m1 = (y2 - y1) / (x2 - x1)
            m2 = (y3 - y2) / (x3 - x2)
            return abs(m1 - m2) < umbral
        return False

    def tadasana(self):
        self.tadasana_state = False
        tadasana_brazo_dcho = False
        tadasana_brazo_izdo = False
        tadasana_pies_hombros = False
        tadasana_brazo_dcho = self.limb_straight(self.hombro_dcho, self.codo_dcho, self.muneca_dcha)
        tadasana_brazo_izdo = self.limb_straight(self.hombro_izdo, self.codo_izdo, self.muneca_izda)
        tadasana_pies_hombros = abs(self.hombro_izdo[0] - self.tobillo_izdo[0]) < 20 and abs(self.hombro_dcho[0] - self.tobillo_dcho[0]) < 20
        if tadasana_brazo_dcho & tadasana_brazo_izdo & tadasana_pies_hombros:
            self.tadasana_state = True

    def check_tadasana(self):
        return self.tadasana_state
    
    def mandasana(self):
        pass
    
    def check_mandasana(self):
        pass

postura_usuario = UserPose()

seleccion = 'de pie' # st.sliderbox()
postura_usuario.set_pose(seleccion)

# Ejemplo de 1 Frame
kps_input = {'nariz': [(333.2094), (333.2410)], 'ojo_izdo': [(352.3026), (324.5705)], 'ojo_dcho': [(326.5327), (320.9801)], 'oreja_izda': [(390.7050), (346.7842)], 'oreja_dcha': [(0.), (0.)], 'hombro_izdo': [(412.7013), (432.4510)], 'hombro_dcho': [(307.0843), (436.1861)], 'codo_izdo': [(477.3592), (488.3250)], 'codo_dcho': [(267.1187), (532.0804)], 'muneca_izda': [(549.3138), (556.2413)], 'muneca_dcha': [(222.0347), (597.1157)], 'cadera_izda': [(379.9662), (642.2715)], 'cadera_dcha': [(315.9659), (639.9982)], 'rodilla_izda': [(379.1678), (846.4087)], 'rodilla_dcha': [(335.6664), (830.6968)], 'tobillo_izdo': [(390.4984), (1027.4502)], 'tobillo_dcho': [(367.1116), (1002.5483)]}

for parte, kps in kps_input.items():
    setattr(postura_usuario, parte, kps)

# Imprimir los valores asignados
print(f"Nariz: {postura_usuario.nariz}")
print(f"Ojo izquierdo: {postura_usuario.ojo_izdo}")
print(f"Ojo derecho: {postura_usuario.ojo_dcho}")
print(f"Oreja izquierda: {postura_usuario.oreja_izda}")
print(f"Oreja derecha: {postura_usuario.oreja_dcha}")
print(f"Hombro izquierdo: {postura_usuario.hombro_izdo}")
print(f"Hombro derecho: {postura_usuario.hombro_dcho}")
print(f"Codo izquierdo: {postura_usuario.codo_izdo}")
print(f"Codo derecho: {postura_usuario.codo_dcho}")
print(f"Muñeca izquierda: {postura_usuario.muneca_izda}")
print(f"Muñeca derecha: {postura_usuario.muneca_dcha}")
print(f"Cadera izquierda: {postura_usuario.cadera_izda}")
print(f"Cadera derecha: {postura_usuario.cadera_dcha}")
print(f"Rodilla izquierda: {postura_usuario.rodilla_izda}")
print(f"Rodilla derecha: {postura_usuario.rodilla_dcha}")
print(f"Tobillo izquierdo: {postura_usuario.tobillo_izdo}")
print(f"Tobillo derecho: {postura_usuario.tobillo_dcho}")

if postura_usuario.name == 'de pie':
    while postura_usuario.check_de_pie == False:
        postura_usuario.de_pie()
    print("De pie!")