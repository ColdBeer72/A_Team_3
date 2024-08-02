<<<<<<< HEAD
from ultralytics import YOLO
import cv2
from pathlib import Path
import shutil
import os

# Cargar el modelo YOLOv8 preentrenado
model = YOLO('yolov8n.pt')  # Puedes cambiar a otros modelos como 'yolov8s.pt', 'yolov8m.pt', etc.

def contar_personas_en_imagen(imagen_ruta):
    # Leer la imagen
    img = cv2.imread(imagen_ruta)
    
    # Realizar la detección
    resultados = model(img, classes=[0])  # Filtrar solo la clase 'person' (índice 0)

    # Obtener el número de personas detectadas
    num_personas = len(resultados[0].boxes)

    # Retornar el número de personas detectadas
    return num_personas

def procesar_imagenes(origen, destino):
    # Crear el directorio de destino si no existe
    os.makedirs(destino, exist_ok=True)

    # Obtener todas las imágenes del directorio de origen
    imagenes = list(Path(origen).glob('*.jpg'))  # Cambia la extensión si es necesario

    for imagen in imagenes:
        num_personas = contar_personas_en_imagen(str(imagen))
        print(f"Imagen: {imagen.name}, Número de personas detectadas: {num_personas}")

        # Si hay exactamente una persona, copiar la imagen al directorio de destino
        if num_personas == 1:
            shutil.copy(str(imagen), destino)
            print(f"Imagen {imagen.name} copiada a {destino}")

# Directorios de origen y destino
directorio_origen = '../../../../mpii_human_pose_v1/images'
directorio_destino = '../../../../human_pose_images_filtrado_1_persona/images'

# Procesar las imágenes
procesar_imagenes(directorio_origen, directorio_destino)
=======
from ultralytics import YOLO
import cv2
from pathlib import Path
import shutil
import os

# Cargar el modelo YOLOv8 preentrenado
model = YOLO('yolov8n.pt')  # Puedes cambiar a otros modelos como 'yolov8s.pt', 'yolov8m.pt', etc.

def contar_personas_en_imagen(imagen_ruta):
    # Leer la imagen
    img = cv2.imread(imagen_ruta)
    
    # Realizar la detección
    resultados = model(img, classes=[0])  # Filtrar solo la clase 'person' (índice 0)

    # Obtener el número de personas detectadas
    num_personas = len(resultados[0].boxes)

    # Retornar el número de personas detectadas
    return num_personas

def procesar_imagenes(origen, destino):
    # Crear el directorio de destino si no existe
    os.makedirs(destino, exist_ok=True)

    # Obtener todas las imágenes del directorio de origen
    imagenes = list(Path(origen).glob('*.jpg'))  # Cambia la extensión si es necesario

    for imagen in imagenes:
        num_personas = contar_personas_en_imagen(str(imagen))
        print(f"Imagen: {imagen.name}, Número de personas detectadas: {num_personas}")

        # Si hay exactamente una persona, copiar la imagen al directorio de destino
        if num_personas == 1:
            shutil.copy(str(imagen), destino)
            print(f"Imagen {imagen.name} copiada a {destino}")

# Directorios de origen y destino
directorio_origen = '../../../../mpii_human_pose_v1/images'
directorio_destino = '../../../../human_pose_images_filtrado_1_persona/images'

# Procesar las imágenes
procesar_imagenes(directorio_origen, directorio_destino)
>>>>>>> de170e30eea247a929ba6a4059126c69af25b756
