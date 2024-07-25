import numpy as np
import cv2
from ultralytics import YOLO

# Load a pre-trained YOLOv10x model
model = YOLO("yolov10x.pt")

# Perform object detection on an image or video (0 for webcam)
results = model.track(0, save=True, show=True, conf=0.2)

# Display the results
results[0].show()

