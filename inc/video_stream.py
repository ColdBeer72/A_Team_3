from av.video.frame import VideoFrame
from numpy import ndarray
import streamlit as st
from streamlit_webrtc import VideoTransformerBase
import cv2
from inc.basic import *

class VideoProcessor(VideoTransformerBase):
    def __init__(self, model_input, user_pose):
        self.model = model_input
        self.user_pose = user_pose
        self.estado_usuario = False

    def draw_kps(self, img, keypoints):
        for _, coords in keypoints.items():
            for i in range(0, len(coords), 2):
                x, y = int(coords[i]), int(coords[i +1])
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

    def process_frame(self, img):
        results = self.model(img)
        for result in results:
            keypoints = result.keypoints.xy
            body_dict = {
                'nariz': [],
                'ojo_izdo': [],
                'ojo_dcho': [],
                'oreja_izda': [],
                'oreja_dcha': [],
                'hombro_izdo': [],
                'hombro_dcho': [],
                'codo_izdo': [],
                'codo_dcho': [],
                'muneca_izda': [],
                'muneca_dcha': [],
                'cadera_izda': [],
                'cadera_dcha': [],
                'rodilla_izda': [],
                'rodilla_dcha': [],
                'tobillo_izdo': [],
                'tobillo_dcho': []
            }
            # Extraer keypoints y asignar a body_dict
            for kp, body_part in zip(keypoints[0], body_dict):
                x, y = kp[0], kp[1]
                body_dict[body_part].extend([x, y])
            # Guardar kps en estado de la app
            print("1r print")
            self.user_pose.update_keypoints(body_dict)
            print("2o print")
            self.estado_usuario = self.user_pose.postura()
            print(f"3r print {self.estado_usuario}")
            # Dibujar keypoints en la imagen
            self.draw_kps(img, body_dict)
            print("4o print")
        return img

    def transform(self, frame: VideoFrame) -> ndarray:
        # Convertir el frame a un array de NumPy
        img = frame.to_ndarray(format="bgr24")
        # Procesar el frame para detectar y dibujar keypoints
        processed_frame = self.process_frame(img)
        # Devolver el frame procesado
        return processed_frame