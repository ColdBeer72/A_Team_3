import json
import random
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Diccionario para mapear los IDs de los puntos a nombres de articulaciones
joint_names = {
    0: 'nariz',
    1: 'ojo_izdo',
    2: 'ojo_dcho',
    3: 'oreja_izdo',
    4: 'oreja_dcho',
    5: 'left_shoulder',
    6: 'right_shoulder',
    7: 'left_elbow',
    8: 'right_elbow',
    9: 'left_wrist',
    10: 'right_wrist',
    11: 'left_hip',
    12: 'right_hip',
    13: 'left_knee',
    14: 'right_knee',
    15: 'left_ankle',
    16:'right_ankle',
    17:'pelvis',
    18:'thorax',
    19:'upper_neck',
    20:'head_top',
    21:'pulgar_izdo',
    22:'pulgar_dcho',
    25:'talon_izdo',
    26:'talon_dcho',
    27:'punta_izdo',
    28:'punta_dcho',
    29:'ombligo',

}

def cargar_anotaciones(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def seleccionar_imagenes_aleatorias(image_folder_path, num_images=10):
    # Obtener la lista de archivos de imagen
    imagenes = [f for f in os.listdir(image_folder_path) if f.endswith('.jpg')]
    # Seleccionar aleatoriamente un número de imágenes
    return random.sample(imagenes, num_images)

def dibujar_anotaciones(imagen_path, anotaciones):
    # Cargar la imagen
    imagen = Image.open(imagen_path)
    fig, ax = plt.subplots(1)
    ax.imshow(imagen)

    # Dibujar las anotaciones
    for persona in anotaciones.get('persons', []):
        # Dibujar rectángulo de cabeza si las coordenadas existen
        if 'x1' in persona and 'y1' in persona and 'x2' in persona and 'y2' in persona:
            rect = patches.Rectangle((persona['x1'], persona['y1']),
                                     persona['x2'] - persona['x1'],
                                     persona['y2'] - persona['y1'],
                                     linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

        # Dibujar puntos de articulación si existen
        for punto in persona.get('joints', []):
            x, y = punto['x'], punto['y']
            ax.plot(x, y, 'bo')  # Marcador azul para cada punto
            joint_id = punto['id']
            joint_name = joint_names.get(joint_id, '')
            # Mostrar el nombre del punto
            ax.text(x, y, f"{joint_name}", color='yellow', fontsize=8)

    plt.show()

def verificar_asociacion(imagenes_seleccionadas, anotaciones, image_folder_path):
    for imagen in imagenes_seleccionadas:
        print(f"Procesando imagen: {imagen}")
        # Obtener anotaciones para esta imagen
        anotacion_imagen = next((item for item in anotaciones if item['image_name'] == imagen), None)
        
        if anotacion_imagen is not None:
            # Ruta completa de la imagen
            imagen_path = os.path.join(image_folder_path, imagen)
            # Dibujar y mostrar la imagen con sus anotaciones
            dibujar_anotaciones(imagen_path, anotacion_imagen)
        else:
            print(f"No se encontraron anotaciones para la imagen {imagen}")

# Uso de las funciones
json_file_path = './labelsFusionDEF.json'  # Ruta al archivo JSON de etiquetas
image_folder_path = '../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie_FINAL/'  # Ruta a la carpeta de imágenes

# Cargar anotaciones
anotaciones = cargar_anotaciones(json_file_path)

# Seleccionar 10 imágenes aleatorias
imagenes_seleccionadas = seleccionar_imagenes_aleatorias(image_folder_path, 10)

# Verificar y dibujar anotaciones
verificar_asociacion(imagenes_seleccionadas, anotaciones, image_folder_path)