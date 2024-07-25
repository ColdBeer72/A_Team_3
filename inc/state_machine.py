import numpy as np
import math

class UserPose:
    def __init__(self):
        self.name = ''
        self.nariz: None
        self.ojo_izdo: None
        self.ojo_dcho: None
        self.oreja_izda: None
        self.oreja_dcha: None
        self.hombro_izdo: None
        self.hombro_dcho: None
        self.codo_izdo: None
        self.codo_dcho: None
        self.muneca_izda: None
        self.muneca_dcha: None
        self.cadera_izda: None
        self.cadera_dcha: None
        self.rodilla_izda: None
        self.rodilla_dcha: None
        self.tobillo_izdo: None
        self.tobillo_dcho: None

    def set_pose(self, pose):
        self.name = pose

    def is_looking_to_camera(self):
        self.cam = False
        if :
            self.cam = True

    def check_camera(self):
        return self.cam

    def de_pie(self):
        self.de_pie = False
        if self.nariz[1] > self.cadera_dcha[1]:
            self.de_pie = True
    
    def check_de_pie(self):
        print(self.de_pie)
        return self.de_pie

    def tadasana(self):
        self.tadasana_state = False
        self.tadasana_brazo_dcho = False
        self.tadasana_brazo_izdo = False
        self.tadasana_pies_hombros = False
        if :
            self.tadasana_brazo_dcho = True
        if :
            self.tadasana_brazo_izdo = True
        if :
            self.tadasana_pies_hombros = True
        if self.tadasana_brazo_dcho == True & self.tadasana_brazo_izdo == True & self.tadasana_pies_hombros == True:
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