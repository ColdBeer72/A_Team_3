import cv2
from ultralytics import YOLO
import os


# Cargar modelo
model = YOLO("yolov8n-pose.pt")

def draw_kp(frame, kps):
    for part, coords in kps.items():
        for i in range(0, len(coords), 2):
            x, y = int(coords[i]), int(coords[i +1])
            cv2.circle(frame, (x, y), 5, (0, 0, 255), 1)

def process_frame(frame):
    results = model(frame)
    
    for result in results:
        keypoints = result.keypoints.xy
        body_dict = {'nariz': [],
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
        for kp, body_part in zip(keypoints[0], body_dict):
            x, y = kp[0], kp[1]
            body_dict[body_part].append(x)
            body_dict[body_part].append(y)
        draw_kp(frame, body_dict)
    return body_dict, frame