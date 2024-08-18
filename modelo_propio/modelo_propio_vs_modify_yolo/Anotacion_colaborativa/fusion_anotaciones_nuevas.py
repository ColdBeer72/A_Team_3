import json
import os

def load_json(file_path):
    """Carga un archivo JSON desde la ruta dada."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    """Guarda los datos en un archivo JSON en la ruta dada."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def merge_json_files(annotations_path, points_folder, output_path):
    """Fusiona los puntos en los archivos JSON de una carpeta con un archivo de anotaciones."""
    # Leer el archivo de anotaciones
    annotations_data = load_json(annotations_path)
    
    # Crear un diccionario para almacenar los puntos por imagen
    points_dict = {}
    
    # Leer todos los archivos JSON en la carpeta de puntos
    for file_name in os.listdir(points_folder):
        if file_name.endswith('.json'):
            file_path = os.path.join(points_folder, file_name)
            file_data = load_json(file_path)
            
            # Verificar si file_data es una lista o un diccionario
            if isinstance(file_data, dict):
                file_data = [file_data]  # Asegurar que sea una lista para la siguiente iteración
            
            # Procesar cada archivo de puntos
            for item in file_data:
                # Usar el nombre del archivo (sin extensión) como clave
                image_name = os.path.splitext(file_name)[0] + '.jpg'
                if image_name not in points_dict:
                    points_dict[image_name] = {}
                for shape in item.get('shapes', []):
                    label = shape.get('label')
                    points = shape.get('points')
                    if label and points:
                        points_dict[image_name][label] = points

    # Fusionar los puntos con las anotaciones
    for annotation_item in annotations_data:
        image_name = annotation_item.get('image_name')
        if image_name in points_dict:
            points = points_dict[image_name]
            for person in annotation_item.get('persons', []):
                joints = person.get('joints', [])
                existing_labels = {joint['name'] for joint in joints}
                
                # Añadir nuevos puntos a partir del ID 16
                next_id = 16
                for label, point_list in points.items():
                    if label not in existing_labels:
                        # Asumimos que solo hay un punto por etiqueta
                        if point_list:
                            x, y = point_list[0][0], point_list[0][1]
                            person['joints'].append({
                                "id": next_id,
                                "name": label,
                                "x": x,
                                "y": y,
                                "is_visible": True  # Establecido como True
                            })
                            next_id += 1

    # Guardar el archivo JSON fusionado
    save_json(annotations_data, output_path)

# Rutas a los archivos y carpetas
annotations_path = '../labels.json'  # Cambia a la ruta del archivo de anotaciones
points_folder = '../../../../../images_anotaciones/Anotaciones_Json'  # Cambia a la ruta de la carpeta con archivos de puntos
output_path = '../labelsFusion.json'  # Cambia a la ruta donde quieres guardar el archivo fusionado

# Ejecutar la fusión
merge_json_files(annotations_path, points_folder, output_path)
