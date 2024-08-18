import os
import shutil
from ultralytics import YOLO
import cv2
import torch

# Configuración de rutas
input_folder = '../../../../human_pose_images_filtrado_1_persona/images'  # Carpeta con imágenes de entrada
output_folder = '../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie'  # Carpeta donde se moverán las imágenes filtradas

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Cargar el modelo preentrenado YOLOv8 para detección de poses
model = YOLO('yolov8n-pose.pt')  # Modelo para detección de keypoints

# Procesar cada imagen en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Filtrar por extensiones de imagen
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # Realizar la detección
        results = model(image)

        # Inicializar un indicador de si al menos un pie fue detectado
        feet_detected = False

        # Verificar cada detección para ver si contiene keypoints de pies
        for result in results:
            # Usar .cpu() para asegurar que los datos están en la memoria de la CPU
            person_keypoints = result.keypoints.xy[0].cpu()

            # Verificar si person_keypoints no está vacío
            if person_keypoints.size(0) > 0:  # Asegurarse de que hay keypoints detectados
                # Verificar los puntos 15 y 16 (pies)
                for idx in [15, 16]:
                    if idx < person_keypoints.size(0):  # Verificar que el índice está dentro de los límites
                        x, y = person_keypoints[idx]
                        
                        # Si cualquiera de los pies es detectado (x, y no son cero), marcar la imagen
                        if x != 0 and y != 0:
                            feet_detected = True
                            break  # No necesitamos revisar más si ya encontramos un pie
                    else:
                        # Si el índice está fuera de los límites, no hacer nada (continuar)
                        continue

            if feet_detected:
                break  # Detener la revisión si ya encontramos un pie

        # Si se detectó al menos un pie, mover la imagen a la carpeta de salida
        if feet_detected:
            shutil.copy(image_path, output_folder)
            print(f"Imagen {filename} movida a {output_folder}.")

print("Proceso completado.")
