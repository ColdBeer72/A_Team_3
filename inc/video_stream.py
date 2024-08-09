import streamlit as st
from streamlit_webrtc import VideoTransformerBase
from av.video.frame import VideoFrame
import cv2
from inc.basic import *
from multiprocessing import Queue

keypoint_queue = Queue()

@st.cache_resource
class VideoProcessor(VideoTransformerBase):
    def __init__(self, _model_input, _user_pose):
        self.model = _model_input
        self.user_pose = _user_pose
        self.body_dict = {}
        # self.keypoint_queue = Queue()

    def draw_kps(self, img, keypoints):
        for _, coords in keypoints.items():
            for i in range(0, len(coords), 2):
                x, y = int(coords[i]), int(coords[i +1])
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

    def recv(self, frame: VideoFrame) -> VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        try:
            results = self.model(img)
            for result in results:
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
                # Guardar kps
                self.body_dict = body_dict
                # Dibujar keypoints en la imagen
                self.draw_kps(img, body_dict)
                keypoint_queue.put(body_dict)
        except Exception as e:
            st.error(f"Error procesando el frame: {e}")
        return VideoFrame.from_ndarray(img, format="bgr24")
    
    def get_body_dict(self):
        return self.body_dict