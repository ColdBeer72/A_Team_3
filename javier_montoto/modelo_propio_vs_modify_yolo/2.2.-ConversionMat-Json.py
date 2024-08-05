import scipy.io
import json
import numpy as np
import os

def mat_to_json_filtered_sorted(mat_file_path, json_file_path, image_folder_path):
    # Cargar el archivo .mat
    mat_data = scipy.io.loadmat(mat_file_path, squeeze_me=True, struct_as_record=False)
    
    # Obtener el campo de anotaciones
    release_data = mat_data['RELEASE']
    annolist = release_data.annolist

    # Obtener los nombres de los archivos de imagen en la carpeta específica
    image_files = set(os.listdir(image_folder_path))

    # Crear una lista para almacenar los datos en formato JSON
    json_data = []

    # Recorrer las anotaciones de cada imagen
    for img_annotations in annolist:
        # Obtener el nombre de la imagen
        image_name = img_annotations.image.name
        
        # Comprobar si la imagen está en la carpeta
        if image_name in image_files:
            # Crear una lista para almacenar las anotaciones de las articulaciones de cada persona en la imagen
            persons_data = []

            # Comprobar si annorect es una lista o un solo objeto
            annorects = img_annotations.annorect
            if isinstance(annorects, np.ndarray):
                annorects = annorects.tolist()  # Convertir ndarray a lista

            if not isinstance(annorects, list):
                annorects = [annorects]  # Asegurarse de que annorects sea una lista

            # Recorrer las anotaciones de cada persona
            for person in annorects:
                if hasattr(person, 'annopoints') and hasattr(person.annopoints, 'point'):
                    # Lista para almacenar las articulaciones de la persona
                    joints_data = []

                    points = person.annopoints.point
                    if isinstance(points, np.ndarray):
                        points = points.tolist()  # Convertir ndarray a lista

                    if not isinstance(points, list):
                        points = [points]  # Asegurarse de que points sea una lista

                    for point in points:
                        joint_info = {
                            'id': int(point.id),  # Convertir a int para asegurarse de que sea JSON serializable
                            'name': get_joint_name(int(point.id)),
                            'x': int(point.x),
                            'y': int(point.y),
                            'is_visible': bool(point.is_visible) if hasattr(point, 'is_visible') else None
                        }
                        joints_data.append(joint_info)

                    person_data = {
                        'head_rect': {
                            'x1': int(person.x1),
                            'y1': int(person.y1),
                            'x2': int(person.x2),
                            'y2': int(person.y2)
                        },
                        'joints': joints_data
                    }

                    persons_data.append(person_data)

            # Añadir la información de la imagen y sus personas a la lista de datos JSON
            json_data.append({
                'image_name': image_name,
                'persons': persons_data
            })

    # Ordenar los datos JSON por el nombre de la imagen (asumiendo que son números)
    json_data_sorted = sorted(json_data, key=lambda x: int(os.path.splitext(x['image_name'])[0]))

    # Guardar los datos en formato JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data_sorted, json_file, indent=4)

def get_joint_name(joint_id):
    # Mapeo de los IDs a los nombres de las articulaciones
    joint_names = {
        0: 'right_ankle',
        1: 'right_knee',
        2: 'right_hip',
        3: 'left_hip',
        4: 'left_knee',
        5: 'left_ankle',
        6: 'pelvis',
        7: 'thorax',
        8: 'upper_neck',
        9: 'head_top',
        10: 'right_wrist',
        11: 'right_elbow',
        12: 'right_shoulder',
        13: 'left_shoulder',
        14: 'left_elbow',
        15: 'left_wrist'
    }
    return joint_names.get(joint_id, 'unknown')


# Uso de la función
mat_file_path = './Dataset2_anotations/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1FINAL.mat'
json_file_path = './Dataset2_anotations/mpii_human_pose_v1_u12_2/labels.json'
image_folder_path = '../../../../human_pose_images_filtrado_1_persona//images_almenos_un_pie_FINAL'
mat_to_json_filtered_sorted(mat_file_path, json_file_path, image_folder_path)
