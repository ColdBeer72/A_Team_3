import os
import json

# Lista de carpetas que contienen los archivos JSON
folders = [
    "../../../../../images_anotaciones/Javi_Json",
    "../../../../../images_anotaciones/Joan_Json/Joan_Json",
    "../../../../../images_anotaciones/Manu_Json",
    "../../../../../images_anotaciones/Jordi_Json/jordi_anotaciones"
]

# Lista de todas las etiquetas esperadas
expected_labels = {
    "meñique_dcho",
    "meñique_izdo",
    "nariz",
    "ojo_dcho",
    "ojo_izdo",
    "ombligo",
    "oreja_dcho",
    "oreja_izdo",
    "pulgar_dcho",
    "pulgar_izdo",
    "punta_dcho",
    "talon_dcho",
    "talon_izdo",
    "punta_izdo"
}

# Lista para acumular archivos con etiquetas faltantes
files_with_missing_labels = []

# Función para comprobar las etiquetas en un archivo JSON
def check_labels_in_file(folder_name, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Extraer las etiquetas de los "shapes"
            labels = {shape['label'] for shape in data.get('shapes', [])}
            
            # Calcular las etiquetas faltantes
            missing_labels = expected_labels - labels
            
            # Si faltan etiquetas, añadir a la lista
            if missing_labels:
                files_with_missing_labels.append({
                    "folder": folder_name,
                    "filename": os.path.basename(file_path),
                    "missing_labels": missing_labels
                })

    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON en el archivo {os.path.basename(file_path)}: {e}")
    except Exception as e:
        print(f"Error al procesar el archivo {os.path.basename(file_path)}: {e}")

# Verificar las carpetas
for folder_path in folders:
    if not os.path.exists(folder_path):
        print(f"La ruta {folder_path} no existe. Por favor, verifica la ruta.")
    else:
        # Recorrer todos los archivos JSON en la carpeta
        found_json = False
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                found_json = True
                file_path = os.path.join(folder_path, filename)
                check_labels_in_file(os.path.basename(folder_path), file_path)
        
        if not found_json:
            print(f"No se encontraron archivos JSON en la carpeta {folder_path}.")

# Imprimir los resultados al final
if files_with_missing_labels:
    print("\nArchivos con etiquetas faltantes:")
    for item in files_with_missing_labels:
        print(f"Carpeta: {item['folder']} - Archivo: {item['filename']} - Etiquetas faltantes: {', '.join(item['missing_labels'])}")
else:
    print("\nTodos los archivos tienen todas las etiquetas esperadas en todas las carpetas.")
