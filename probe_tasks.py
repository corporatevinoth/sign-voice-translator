import mediapipe as mp
import importlib

print("Probing mp.tasks.vision...")
try:
    from mediapipe.tasks.python import vision
    print(f"Vision module: {dir(vision)}")
    if hasattr(vision, 'HolisticLandmarker'):
        print("HolisticLandmarker FOUND!")
    elif hasattr(vision, 'PoseLandmarker'):
        print("PoseLandmarker FOUND!")
    if hasattr(vision, 'HandLandmarker'):
        print("HandLandmarker FOUND!")
    if hasattr(vision, 'FaceLandmarker'):
        print("FaceLandmarker FOUND!")
except ImportError as e:
    print(f"Failed to import vision tasks: {e}")
except Exception as e:
    print(f"Error: {e}")
