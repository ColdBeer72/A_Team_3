from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Cargar el modelo YOLOv8 preentrenado
model = YOLO('yolov8n.pt')  # Puedes cambiar a otros modelos como 'yolov8s.pt', 'yolov8m.pt', etc.

def contar_personas_en_imagen(imagen_ruta):
    # Leer la imagen
    img = cv2.imread(imagen_ruta)
    
    # Realizar la detección
    resultados = model(img, classes=[0])  # Filtrar solo la clase 'person' (índice 0)

    # Obtener el número de personas detectadas
    num_personas = len(resultados[0].boxes)

    # Mostrar la imagen con las detecciones
    annot_img = resultados[0].plot()
    plt.imshow(cv2.cvtColor(annot_img, cv2.COLOR_BGR2RGB))
    plt.title(f"Personas detectadas: {num_personas}")
    plt.axis('off')
    plt.show()

    # Retornar el número de personas detectadas
    return num_personas

# Ruta a la imagen
imagen_ruta = '../../../../mpii_human_pose_v1/images/000001163.jpg'  

# Contar personas y mostrar resultados
num_personas = contar_personas_en_imagen(imagen_ruta)
print(f"Número de personas detectadas: {num_personas}")
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Cargar el modelo YOLOv8 preentrenado
model = YOLO('yolov8n.pt')  # Puedes cambiar a otros modelos como 'yolov8s.pt', 'yolov8m.pt', etc.

def contar_personas_en_imagen(imagen_ruta):
    # Leer la imagen
    img = cv2.imread(imagen_ruta)
    
    # Realizar la detección
    resultados = model(img, classes=[0])  # Filtrar solo la clase 'person' (índice 0)

    # Obtener el número de personas detectadas
    num_personas = len(resultados[0].boxes)

    # Mostrar la imagen con las detecciones
    annot_img = resultados[0].plot()
    plt.imshow(cv2.cvtColor(annot_img, cv2.COLOR_BGR2RGB))
    plt.title(f"Personas detectadas: {num_personas}")
    plt.axis('off')
    plt.show()

    # Retornar el número de personas detectadas
    return num_personas

# Ruta a la imagen
imagen_ruta = '../../../../mpii_human_pose_v1/images/000001163.jpg'  

# Contar personas y mostrar resultados
num_personas = contar_personas_en_imagen(imagen_ruta)
print(f"Número de personas detectadas: {num_personas}")