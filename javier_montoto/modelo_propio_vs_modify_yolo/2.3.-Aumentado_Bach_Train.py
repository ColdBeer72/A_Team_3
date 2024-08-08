from keras import layers
import tensorflow as tf

from imgaug.augmentables.kps import KeypointsOnImage
from imgaug.augmentables.kps import Keypoint
import imgaug.augmenters as iaa

from pprint import pprint

from PIL import Image
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import json
import os

#HIPERPARAMETROS
IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 5
NUM_KEYPOINTS = 17 * 2

#Leer datos JSON Dict
IMG_DIR = "../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie_FINAL/"
JSON = "./labelsDEF.json"

# Load the ground-truth annotations.
with open(JSON) as infile:
    json_data = json.load(infile)

# Crear diccionario asociando anotaciones de la imagen imagen a path.
json_dict = {i["img_path"]: i for i in json_data}

#pprint(json_dict)

# Utility for reading an image and for getting its annotations.
import os
import json
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# HIPERPARÁMETROS
IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 5
NUM_KEYPOINTS = 17 * 2

# Leer datos JSON Dict
IMG_DIR = "../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie_FINAL/"
JSON = "./labelsDEF.json"

# Cargar las anotaciones del archivo JSON.
with open(JSON) as infile:
    json_data = json.load(infile)

# Crear diccionario asociando anotaciones de la imagen con la ruta completa de la imagen.
json_dict = {i["img_path"]: i for i in json_data}

# Imprimir las primeras claves para verificar
print("Primeras claves en el diccionario JSON:", list(json_dict.keys())[:3])

# Utilidad para leer una imagen y obtener sus anotaciones.
def get_image(name):
    # Construir la ruta completa de la imagen
    img_full_path = os.path.join(IMG_DIR, name)
    
    try:
        data = json_dict[img_full_path]
    except KeyError:
        print(f"Imagen {name} no encontrada en los datos JSON.")
        return None

    img_data = plt.imread(img_full_path)
    # Si la imagen es RGBA convertirla a RGB.
    if img_data.shape[-1] == 4:
        img_data = img_data.astype(np.uint8)
        img_data = Image.fromarray(img_data)
        img_data = np.array(img_data.convert("RGB"))
    data["img_data"] = img_data

    return data

# Probar la función con depuración
image_data = get_image("050442104.jpg")
if image_data:
    pprint(image_data)


#Funcion comprobacion visualizacion data
# def visualize_keypoints(images, keypoints):
#     fig, axes = plt.subplots(nrows=len(images), ncols=2, figsize=(16, 12))
#     [ax.axis("off") for ax in np.ravel(axes)]

#     for (ax_orig, ax_all), image, current_keypoint in zip(axes, images, keypoints):
#         ax_orig.imshow(image)
#         ax_all.imshow(image)

#         # If the keypoints were formed by `imgaug` then the coordinates need
#         # to be iterated differently.
#         if isinstance(current_keypoint, KeypointsOnImage):
#             for idx, kp in enumerate(current_keypoint.keypoints):
#                 ax_all.scatter(
#                     [kp.x],
#                     [kp.y],
#                     marker="x",
#                     s=50,
#                     linewidths=5,
#                 )
#         else:
#             current_keypoint = np.array(current_keypoint)
#             # Since the last entry is the visibility flag, we discard it.
#             current_keypoint = current_keypoint[:, :2]
#             for idx, (x, y) in enumerate(current_keypoint):
#                 ax_all.scatter([x], [y], marker="x", s=50, linewidths=5)

#     plt.tight_layout(pad=2.0)
#     plt.show()


# # Select four samples randomly for visualization.
# samples = list(json_dict.keys())
# num_samples = 4
# selected_samples = np.random.choice(samples, num_samples, replace=False)

# images, keypoints = [], []

# for sample in selected_samples:
#     data = get_image(sample)
#     image = data["img_data"]
#     keypoint = data["joints"]

#     images.append(image)
#     keypoints.append(keypoint)

# visualize_keypoints(images, keypoints)


