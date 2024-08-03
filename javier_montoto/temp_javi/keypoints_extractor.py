import cv2
from ultralytics import YOLO

def obtener_keypoints_halasana(imagen_path):
    # Cargar el modelo de YOLOv8
    model = YOLO('yolov8n-pose.pt')  # Puedes cambiar 'n' por 's', 'm', 'l' o 'x' dependiendo de la versión que quieras usar

    # Cargar la imagen
    image = cv2.imread(imagen_path)

    # Realizar la detección de poses
    results = model(image)

    # Extraer keypoints de la primera detección
    if results and results[0].keypoints:
        keypoints = results[0].keypoints[0]  # Obtener los keypoints del primer resultado
        keypoints = keypoints.xy.numpy()  # Convertir a numpy array
        
        # Crear el diccionario de keypoints
        kps_input = {
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
        return kps_input
    else:
        raise ValueError("No se detectaron poses en la imagen.")
