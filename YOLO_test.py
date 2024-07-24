from ultralytics import YOLO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import math
import cv2

model = YOLO("yolov8n-pose.pt")

vid_path = "data/01_Tadasana/Figura1_Tadasana_Postura de equilibro.mp4"

vid_reader = imageio.get_reader(vid_path)

# Obtencion de metadata y desglose
meta_data = vid_reader.get_meta_data()
width = meta_data['size'][0]
height = meta_data['size'][1]
fps = meta_data['fps']
duration = meta_data['duration']
frame_count = int(math.ceil(fps * duration))
print(f"Video metadata: width={width}, height={height}, fps={fps}, duration={duration}, frame_count={frame_count}")

# Creacion frame2frame del video
video_frames = []
for i, frame in enumerate(vid_reader):
    if i >= frame_count:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if frame_rgb.shape[0] == 0 or frame_rgb.shape[1] == 0:
        print(f"Error: Frame {i} has invalid dimensions {frame_rgb.shape}")
        continue
    frame_rgb = frame_rgb / 255.0
    video_frames.append(frame_rgb)
# Finalizamos visionado del video
vid_reader.close()

video_np = np.array(video_frames)

try:
    results = model(video_np, augment=False)
    metrics = results[0].keypoints
    print("YOLO evaluation completed successfully")
except Exception as e:
    print(f"Error during YOLO evaluation: {e}")