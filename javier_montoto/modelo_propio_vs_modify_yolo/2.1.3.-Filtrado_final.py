import os
import random
import shutil

# Configuración de rutas
source_folder = '../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie'  # Carpeta con imágenes filtradas
destination_folder = '../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie_FINAL'  # Carpeta donde se copiarán las imágenes seleccionadas
fraction = 0.20  # Fracción de imágenes a seleccionar

# Crear la carpeta de destino si no existe
os.makedirs(destination_folder, exist_ok=True)

# Obtener una lista de todas las imágenes en la carpeta de origen
all_images = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Determinar cuántas imágenes seleccionar
num_images_to_select = int(len(all_images) * fraction)

# Seleccionar aleatoriamente las imágenes
selected_images = random.sample(all_images, num_images_to_select)

# Copiar las imágenes seleccionadas a la carpeta de destino
for image in selected_images:
    src_path = os.path.join(source_folder, image)
    dest_path = os.path.join(destination_folder, image)
    shutil.copy(src_path, dest_path)  # Usar shutil.copy para copiar el archivo
    print(f"Imagen {image} copiada a {destination_folder}.")

print("Selección aleatoria y copia completadas.")
