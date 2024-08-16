import json

def load_json(file_path):
    """Carga un archivo JSON desde la ruta dada."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    """Guarda los datos en un archivo JSON en la ruta dada."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def reorder_and_reassign_ids(annotation_file, output_file):
    """Reordena los joints y reasigna los IDs en el archivo de anotaciones."""
    # Cargar el archivo de anotaciones
    data = load_json(annotation_file)
    
    # Definir el nuevo orden para los joints
    new_order = [
        'nariz', 'ojo_izdo', 'ojo_dcho', 'oreja_izdo', 'oreja_dcho', 
        'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 
        'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 
        'left_knee', 'right_knee', 'left_ankle', 'right_ankle', 
        'pelvis', 'thorax', 'upper_neck', 'head_top', 
        'pulgar_izdo', 'pulgar_dcho', 'meñique_izdo', 'meñique_dcho', 
        'talon_izdo', 'talon_dcho', 'punta_izdo', 'punta_dcho', 'ombligo'
    ]
    
    # Procesar cada imagen en el archivo
    for item in data:
        for person in item.get('persons', []):
            # Obtener los joints y crear un diccionario para facilitar el reordenamiento
            joints = person.get('joints', [])
            joint_dict = {joint['name']: joint for joint in joints}
            
            # Crear una lista vacía para los joints reordenados
            reordered_joints = []
            
            # Añadir los joints en el nuevo orden y reasignar los IDs
            for idx, name in enumerate(new_order):
                if name in joint_dict:
                    joint = joint_dict[name].copy()
                    joint['id'] = idx  # Reasignar el ID
                    joint['is_visible'] = True  # Asegurarse de que is_visible esté en True
                    reordered_joints.append(joint)
            
            # Reemplazar la lista de joints en el archivo con la lista reordenada
            person['joints'] = reordered_joints

    # Guardar el archivo JSON con los joints reordenados y los IDs reasignados
    save_json(data, output_file)

# Rutas a los archivos
annotation_file = '../labelsFusion.json'  # Cambia a la ruta del archivo fusionado
output_file = '../labelsFusionDEF.json'  # Cambia a la ruta del archivo con los joints reordenados

# Ejecutar el reordenamiento y reasignación de IDs
reorder_and_reassign_ids(annotation_file, output_file)
