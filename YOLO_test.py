import cv2
from ultralytics import YOLO

# Cargar el modelo
model = YOLO("yolov8n-pose.pt")

video_path = "data/Raw/01_Tadasana/Figura1_Tadasana_Postura de equilibro.mp4"
# Abrir el video
cap = cv2.VideoCapture(video_path)

# Configurar variables para el control del video
playing = True
frame_step = 10  # Número de frames a avanzar o retroceder

# Configurar el tamaño deseado de la ventana (ancho, alto)
window_width = 600
window_height = 800

def draw_kp(frame, kps):
    for part, coords in kps.items():
        x, y = int(coords[0]), int(coords[1])
        cv2.circle(frame, (x, y), 5, (0, 0, 255), 1)

while cap.isOpened():
    if playing:
        ret, frame = cap.read()
        if not ret:
            break

        # Realizar detección de posturas
        results = model(frame)

        # Los resultados suelen ser una lista de objetos de detección
        for result in results:
            # print(f"\nResultados: {result}")
            keypoints = result.keypoints.xy
            # print(f"Keypoints: {keypoints}")
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
                # print(f"KPs: {kp}")
                x, y = kp[0], kp[1]
                body_dict[body_part].append(x)
                body_dict[body_part].append(y)
                print(body_dict)
            draw_kp(frame, body_dict)
            # annotated_frame = result.plot()

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