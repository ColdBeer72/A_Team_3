import os
import random
import shutil
import scipy.io

# Función para verificar si todos los keypoints están presentes
def has_all_keypoints(annopoints):
    # Verificar si hay puntos de anotación
    if hasattr(annopoints, 'point'):
        points = annopoints.point
        # Asegurarse de que todos los puntos esperados están presentes
        joint_ids = {point.id for point in points}  # Cambiar el acceso a point
        # Hay 16 articulaciones esperadas
        expected_joint_ids = set(range(16))
        return expected_joint_ids.issubset(joint_ids)
    return False

# Cargar el archivo .mat
mat_path = './Dataset2_anotations/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1.mat'
mat = scipy.io.loadmat(mat_path, squeeze_me=True, struct_as_record=False)

# Extraer la lista de anotaciones y las imágenes de entrenamiento
annotations = mat['RELEASE'].annolist
img_train = mat['RELEASE'].img_train

# Configuración de rutas
source_folder = '../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie'  # Carpeta con imágenes filtradas
destination_folder = '../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie_FINAL'  # Carpeta donde se copiarán las imágenes seleccionadas
fraction = 0.20  # Fracción de imágenes a seleccionar

# Crear la carpeta de destino si no existe
os.makedirs(destination_folder, exist_ok=True)

# Filtrar las imágenes que tienen todos los keypoints
filtered_images = []
for img_idx, annotation in enumerate(annotations):
    image_name = annotation.image.name
    if img_train[img_idx] == 1:  # Solo considerar imágenes de entrenamiento
        if hasattr(annotation, 'annorect'):
            rects = annotation.annorect
            # Asegurarse de que sea iterable
            if not isinstance(rects, list):
                rects = [rects]
            for rect in rects:
                if hasattr(rect, 'annopoints') and has_all_keypoints(rect.annopoints):
                    filtered_images.append(image_name)
                    break  # Solo necesitamos añadir una vez si cualquier rectángulo tiene todos los keypoints

# Obtener una lista de todas las imágenes en la carpeta de origen que pasan el filtro
all_images = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
filtered_images_set = set(filtered_images)

# Intersectar con las imágenes disponibles
valid_images = list(filtered_images_set.intersection(all_images))

# Determinar cuántas imágenes seleccionar
num_images_to_select = int(len(valid_images) * fraction)

# Seleccionar aleatoriamente las imágenes
selected_images = random.sample(valid_images, num_images_to_select)

# Copiar las imágenes seleccionadas a la carpeta de destino
for image in selected_images:
    src_path = os.path.join(source_folder, image)
    dest_path = os.path.join(destination_folder, image)
    shutil.copy(src_path, dest_path)  # Usar shutil.copy para copiar el archivo
    print(f"Imagen {image} copiada a {destination_folder}.")

print("Selección aleatoria y copia completadas.")
