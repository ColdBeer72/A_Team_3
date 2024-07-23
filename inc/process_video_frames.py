import os
import cv2
import json

# Ruta a la carpeta de datos y archivo de etiquetas
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/Raw'))
labels_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/labels.json'))
output_frames_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/Processed'))

# Cargar etiquetas
with open(labels_file, 'r') as f:
    labels = json.load(f)

# Crear directorios de salida si no existen
if not os.path.exists(output_frames_dir):
    os.makedirs(output_frames_dir)

# Procesar videos
for video_path, label in labels.items():
    video_file = os.path.join(data_dir, video_path)
    output_dir = os.path.join(output_frames_dir, label)
    
    # Crear directorio para frames si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Verificar si el archivo de video existe
    if not os.path.exists(video_file):
        print(f'Advertencia: El archivo de video {video_file} no existe.')
        continue

    # Cargar el video
    cap = cv2.VideoCapture(video_file)
    
    # Verificar si el video se cargó correctamente
    if not cap.isOpened():
        print(f'Error al abrir el archivo de video {video_file}.')
        continue

    frame_idx = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Redimensionar el frame si es necesario
        frame_resized = cv2.resize(frame, (224, 224))
        
        # Guardar el frame
        frame_filename = os.path.join(output_dir, f'{frame_idx:04d}.jpg')
        cv2.imwrite(frame_filename, frame_resized)
        
        frame_idx += 1

    cap.release()
    print(f'Frames extraídos para {video_path} y guardados en {output_dir}')
