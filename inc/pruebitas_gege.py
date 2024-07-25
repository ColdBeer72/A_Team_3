import cv2
from ultralytics import YOLO
import os

def yololo(frame):
    model = YOLO("yolov8n-pose.pt")        
    results = model(frame)
    return results