import streamlit as st
from streamlit_webrtc import VideoTransformerBase
from av.video.frame import VideoFrame
import cv2
from inc.basic import *
from multiprocessing import Queue

keypoint_queue = Queue()

@st.cache_resource
class VideoProcessor(VideoTransformerBase):
    def __init__(self, _model_input):
        self.model = _model_input
        self.draw = False

    def draw_kps(self, img, keypoints):
        for _, coords in keypoints.items():
            for i in range(0, len(coords), 2):
                x, y = int(coords[i]), int(coords[i +1])
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

    def recv(self, frame: VideoFrame) -> VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        # try:
        results = self.model(img)
        print(results)
        for result in results:
            try:
                keypoints = result.keypoints.xy
                body_dict = {
                    'nariz': [],
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
                # Extraer keypoints y asignar a body_dict
                for kp, body_part in zip(keypoints[0], body_dict):
                    x, y = kp[0], kp[1]
                    body_dict[body_part].extend([x, y])
                # Dibujar keypoints en la imagen
                if self.draw:
                    self.draw_kps(img, body_dict)
                keypoint_queue.put(body_dict)
            except Exception as e:
                print(e)
        return VideoFrame.from_ndarray(img, format="bgr24")
        # except Exception as e:
        #     print(f"Error procesando el frame: {e}")
    
    def set_draw(self, state):
        self.draw = state