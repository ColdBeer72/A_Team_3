import cv2

def select_camera():
    lista_camaras = []
    for i in range(10):  # Más de 10 suena imposible
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            lista_camaras.append(i)
            cap.release()
    return lista_camaras