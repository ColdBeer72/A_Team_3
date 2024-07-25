import cv2
from ultralytics import YOLO
import os


# Cargar el modelo
model = YOLO("yolov8n-pose.pt")
print("Modelo cargado con éxito")

video_path = "data/Raw/01_Tadasana/Figura1_Tadasana_Postura de equilibro.mov"
<<<<<<< HEAD
if not os.path.isfile(video_path):
    print(f"El archivo de video no se encuentra en: {video_path}")
else:
    print(f"El archivo de video se encuentra en: {video_path}")
=======
>>>>>>> a500c7493ed984d85e4d47545d72529a98050577
# Abrir el video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error al abrir el video.")
    exit()

# Configurar variables para el control del video
playing = True
frame_step = 10  # Número de frames a avanzar o retroceder

# Configurar el tamaño deseado de la ventana (ancho, alto)
window_width = 600
window_height = 800

def draw_kp(frame, kps):
    for part, coords in kps.items():
        for i in range(0, len(coords), 2):  # Cada par de coordenadas (x, y)
            x, y = int(coords[i]), int(coords[i+1])
            cv2.circle(frame, (x, y), 5, (0, 0, 255), 1)

while cap.isOpened():
    if playing:
        ret, frame = cap.read()
        if not ret:
            print("No se puede leer el frame del video.")
            break

        # Realizar detección de posturas
        results = model(frame)
        print(f"Resultados: {results}")

        for result in results:
            keypoints = result.keypoints.xy
            print(f"Keypoints: {keypoints}")

            body_dict = {'nariz': [],
                         'ojo_izdo': [],
                         'ojo_dcho': [],
                         'oreja_izda': [],
                         'oreja_dcha': [],
                         'hombro_izdo': [],
                         'hombro_dcho': [],
                         'codo_izdo': [],
                         'codo_dcho': [],
                         'muneca_izda': [],
                         'muneca_dcha': [],
                         'cadera_izda': [],
                         'cadera_dcha': [],
                         'rodilla_izda': [],
                         'rodilla_dcha': [],
                         'tobillo_izdo': [],
                         'tobillo_dcho': []
                         }
            for kp, body_part in zip(keypoints[0], body_dict):
                x, y = kp[0], kp[1]
                body_dict[body_part].append(x)
                body_dict[body_part].append(y)
                print(f"{body_part}: {body_dict[body_part]}")

            draw_kp(frame, body_dict)

        # Redimensionar el frame
        resized_frame = cv2.resize(frame, (window_width, window_height))

        # Mostrar el frame con anotaciones
        cv2.imshow('Detection', resized_frame)
    
    # Leer teclas
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # Salir
        break
    elif key == ord('p'):  # Pausar/Reanudar
        playing = not playing
    elif key == ord('n'):  # Avanzar
        current_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_pos + frame_step)
    elif key == ord('b'):  # Retroceder
        current_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(current_pos - frame_step, 0))

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
