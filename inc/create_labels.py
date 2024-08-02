import os
import json

# Ruta a la carpeta principal que contiene los videos de yoga
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/Raw'))

# Diccionario para almacenar las etiquetas
labels = {}

# Recorrer las carpetas y videos
for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path):
        for video in os.listdir(folder_path):
            if video.endswith(('.mp4', '.avi', '.mov')):
                # Obtener la ruta absoluta del video
                video_path = os.path.relpath(os.path.join(folder_path, video), start=os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))
                labels[video_path] = folder

# Guardar las etiquetas en un archivo JSON
output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/labels.json'))
with open(output_file, 'w') as f:
    json.dump(labels, f, indent=4)

print(f'Etiquetas guardadas en {output_file}')
