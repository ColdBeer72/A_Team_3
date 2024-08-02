from ultralytics import YOLO
import cv2
import os

def obtener_keypoints_halasana(imagen_path):
    imagen_path_absoluta = os.path.abspath(imagen_path)
    print(f"Ruta completa de la imagen: {imagen_path_absoluta}")

    if not os.path.exists(imagen_path_absoluta):
        raise FileNotFoundError(f"No such file or directory: '{imagen_path_absoluta}'")
    model = YOLO('yolov8n-pose.pt')  # Asegúrate de tener el modelo YOLOv8 entrenado para pose
    image = cv2.imread(imagen_path_absoluta)
    if image is None:
        raise ValueError(f"Failed to load image from path: '{imagen_path_absoluta}'")
    results = model(image)
    
    keypoints = results[0].keypoints.cpu().numpy()
    keypoints_dict = {
        'nariz': keypoints[0],
        'ojo_izdo': keypoints[1],
        'ojo_dcho': keypoints[2],
        'oreja_izda': keypoints[3],
        'oreja_dcha': keypoints[4],
        'hombro_izdo': keypoints[5],
        'hombro_dcho': keypoints[6],
        'codo_izdo': keypoints[7],
        'codo_dcho': keypoints[8],
        'muneca_izda': keypoints[9],
        'muneca_dcha': keypoints[10],
        'cadera_izda': keypoints[11],
        'cadera_dcha': keypoints[12],
        'rodilla_izda': keypoints[13],
        'rodilla_dcha': keypoints[14],
        'tobillo_izdo': keypoints[15],
        'tobillo_dcho': keypoints[16]
    }
    return keypoints_dict

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
        self.enpie = False
        self.halasana_state = False

    def set_pose(self, pose):
        self.name = pose

    def update_keypoints(self, keypoints):
        for key, value in keypoints.items():
            setattr(self, key, value)

    def limb_straight_horizontal(self, limb1, limb2, limb3):
        umbral = 5
        if limb1 is not None and limb2 is not None and limb3 is not None:
            x1, y1 = limb1
            x2, y2 = limb2
            x3, y3 = limb3
            if y1 == y2 == y3:
                return True
            if y2 == y1 or y3 == y2:
                return False
            m1 = abs((x2 - x1) / (y2 - y1))
            m2 = abs((x3 - x2) / (y3 - y2))
            print(f"Extremidad recta horizontal?: {abs(m1 - m2) < umbral}")
            return abs(m1 - m2) < umbral
        return False

    def halasana(self):
        self.halasana_state = False
        halasana_brazos_rectos = self.limb_straight_horizontal(self.hombro_izdo, self.codo_izdo, self.muneca_izda) and \
                                 self.limb_straight_horizontal(self.hombro_dcho, self.codo_dcho, self.muneca_dcha)
        halasana_piernas_rectas = self.limb_straight_horizontal(self.cadera_izda, self.rodilla_izda, self.tobillo_izdo) and \
                                  self.limb_straight_horizontal(self.cadera_dcha, self.rodilla_dcha, self.tobillo_dcho)
        caderas_sobre_extremidades_superiores = self.cadera_izda[0] > self.hombro_izdo[0] and self.cadera_dcha[0] > self.hombro_dcho[0]
        inclinacion_negativa = (self.tobillo_izdo[1] > self.cadera_izda[1]) and (self.tobillo_dcho[1] > self.cadera_dcha[1])
        cabeza_entre_cadera_rodilla = self.cadera_izda[0] > self.nariz[0] > self.rodilla_izda[0] and \
                                      self.cadera_dcha[0] > self.nariz[0] > self.rodilla_dcha[0]
        # Comprobar que los miembros superiores e inferiores ocupan el mismo espacio en x
        miembros_superiores_en_mismo_x = abs(self.hombro_izdo[0] - self.hombro_dcho[0]) < 10 and \
                                         abs(self.codo_izdo[0] - self.codo_dcho[0]) < 10 and \
                                         abs(self.muneca_izda[0] - self.muneca_dcha[0]) < 10
        miembros_inferiores_en_mismo_x = abs(self.cadera_izda[0] - self.cadera_dcha[0]) < 10 and \
                                         abs(self.rodilla_izda[0] - self.rodilla_dcha[0]) < 10 and \
                                         abs(self.tobillo_izdo[0] - self.tobillo_dcho[0]) < 10

        if halasana_brazos_rectos and halasana_piernas_rectas and caderas_sobre_extremidades_superiores and inclinacion_negativa and cabeza_entre_cadera_rodilla and miembros_superiores_en_mismo_x and miembros_inferiores_en_mismo_x:
            self.halasana_state = True

    def check_halasana(self):
        return self.halasana_state

# Uso del código
imagen_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/3_postura_test_halasana/halasana-postura-arado-yoga.jpg'))
kps_input = obtener_keypoints_halasana(imagen_path)

postura_usuario = UserPose()
postura_usuario.set_pose('Halasana')

for parte, kps in kps_input.items():
    setattr(postura_usuario, parte, kps)

if postura_usuario.name == 'Halasana':
    while not postura_usuario.check_halasana():
        print("Corrige postura")
        postura_usuario.halasana()
    print("Halasana COMPLETE!")
