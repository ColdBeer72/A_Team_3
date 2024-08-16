import json

# Ruta al archivo JSON original
input_path = './labelsFusionDEF.json'

# Ruta para guardar el nuevo archivo JSON
output_path = './labelsFusionDEFINITIVO.json'

# Prefijo para el image_name
prefix = "../../../../human_pose_images_filtrado_1_persona/images_almenos_un_pie_FINAL/"

# Cargar el archivo JSON original
with open(input_path, 'r') as f:
    data = json.load(f)

# Lista para almacenar los datos transformados
new_format_data = []

# Transformar los datos
for item in data:
    img_path = item['image_name']
    full_img_path = prefix + img_path
    
    # Iterar sobre las personas en cada imagen
    for person in item.get('persons', []):
        # Obtener datos de las articulaciones
        joints = person.get('joints', [])
        
        # Dividir head_rect en dos puntos
        head_rect = person.get('head_rect', {})
        x1, y1 = head_rect.get('x1', 0), head_rect.get('y1', 0)
        x2, y2 = head_rect.get('x2', 0), head_rect.get('y2', 0)
        
        # Añadir head_rect como dos puntos en joints
        head_rect_points = [
            [x1, y1, 1],
            [x2, y2, 1]
        ]
        
        # Incluir los puntos de head_rect en los joints
        transformed_joints = head_rect_points + [
            [joint['x'], joint['y'], 1 if joint['is_visible'] else 0] for joint in joints
        ]
        
        # Crear la entrada transformada
        entry = {
            "img_path": full_img_path,
            "joints": transformed_joints
        }
        
        # Añadir la entrada a la lista de datos transformados
        new_format_data.append(entry)

# Guardar los datos transformados en un nuevo archivo JSON
with open(output_path, 'w') as f:
    json.dump(new_format_data, f, indent=4)

print(f'Archivo guardado en {output_path}')
