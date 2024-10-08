from ultralytics import YOLO
import cv2
from pathlib import Path
import shutil
import os

# Cargar el modelo YOLOv8 preentrenado
model = YOLO('yolov8n.pt')  # Puedes cambiar a otros modelos como 'yolov8s.pt', 'yolov8m.pt', etc.

def cumple_condicion_imagen_y_pies(imagen_ruta, min_umbral_area=0.25, max_umbral_area=0.4, umbral_pies=0.1):
    # Leer la imagen
    img = cv2.imread(imagen_ruta)
    altura_imagen, ancho_imagen = img.shape[:2]
    area_imagen = altura_imagen * ancho_imagen
    
    # Realizar la detección
    resultados = model(img, classes=[0])  # Filtrar solo la clase 'person' (índice 0)

    # Revisar si alguna persona cumple la condición de área y si los pies son visibles
    for box in resultados[0].boxes:
        x1, y1, x2, y2 = box.xyxy.cpu().numpy()[0]
        altura_persona = y2 - y1
        ancho_persona = x2 - x1
        area_persona = altura_persona * ancho_persona
        
        # Calcular la proporción del área de la persona con respecto al área total de la imagen
        proporcion_area = area_persona / area_imagen
        
        # Comprobar si la proporción del área está entre los umbrales
        if min_umbral_area <= proporcion_area <= max_umbral_area:
            # Comprobar si los pies son visibles
            # Se asume que los pies están en el 10% inferior de la imagen
            margen_pies = altura_imagen * umbral_pies
            if y2 > altura_imagen - margen_pies:
                return True
    return False

def filtrar_y_copiar_imagenes(origen, destino):
    # Crear el directorio de destino si no existe
    os.makedirs(destino, exist_ok=True)

    # Contador de imágenes que cumplen la condición
    contador = 0

    # Obtener todas las imágenes del directorio de origen
    imagenes = list(Path(origen).glob('*.jpg'))  # Cambia la extensión si es necesario

    for imagen in imagenes:
        if cumple_condicion_imagen_y_pies(str(imagen)):
            contador += 1
            # Copiar la imagen al directorio de destino
            shutil.copy(str(imagen), destino)
            print(f"Imagen {imagen.name} copiada a {destino}")

    return contador

# Directorios de origen y destino
directorio_origen = '../../../../human_pose_images_filtrado_1_persona/images'
directorio_destino = '../../../../human_pose_images_filtrado_1_persona/images_cuerpo_completo'

# Filtrar y copiar imágenes
imagenes_filtradas = filtrar_y_copiar_imagenes(directorio_origen, directorio_destino)
print(f"Total de imágenes copiadas que cumplen con la condición: {imagenes_filtradas}")
