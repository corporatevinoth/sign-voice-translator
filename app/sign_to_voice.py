import cv2
import mediapipe as mp
import numpy as np
import os
import time
from app.utils.landmarks import extract_landmarks
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class SignDetector:
    def __init__(self):
        # Load models
        base_options_pose = python.BaseOptions(model_asset_path='models/pose_landmarker_lite.task')
        options_pose = vision.PoseLandmarkerOptions(
            base_options=base_options_pose,
            num_poses=1)
        self.pose_landmarker = vision.PoseLandmarker.create_from_options(options_pose)

        base_options_hand = python.BaseOptions(model_asset_path='models/hand_landmarker.task')
        options_hand = vision.HandLandmarkerOptions(
            base_options=base_options_hand,
            num_hands=2)
        self.hand_landmarker = vision.HandLandmarker.create_from_options(options_hand)

        base_options_face = python.BaseOptions(model_asset_path='models/face_landmarker.task')
        options_face = vision.FaceLandmarkerOptions(
            base_options=base_options_face,
            num_faces=1)
        self.face_landmarker = vision.FaceLandmarker.create_from_options(options_face)

        # Draw util fallback (mediapipe 0.10 tasks doesn't have simple drawing utils matched to tasks results yet easily)
        # We will implement simple drawing or skip for now to save complexity, or try to use mp.solutions.drawing_utils if available (partially broken?)
        # Let's try to import drawing utils safely
        try:
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_pose = mp.solutions.pose
            self.mp_hands = mp.solutions.hands
            self.mp_face_mesh = mp.solutions.face_mesh
            self.can_draw = True
        except AttributeError:
            self.can_draw = False

    def process_frame(self, frame):
        """
        Processes a single frame: detects landmarks and extracts keypoints.
        """
        if frame is None:
            return None, None

        # Conversion for MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Run inference
        pose_result = self.pose_landmarker.detect(mp_image)
        hand_result = self.hand_landmarker.detect(mp_image)
        face_result = self.face_landmarker.detect(mp_image)

        # Draw (if possible)
        output_image = frame.copy()
        if self.can_draw:
           pass # TODO: Mapping tasks result to drawing utils is complex, skipping visual overlay for robustness now
                 # or we can manually draw dots

        # Manually draw simple landmarks if can_draw is broken
        if not self.can_draw:
             # Draw Pose
             if pose_result.pose_landmarks:
                 for lm in pose_result.pose_landmarks[0]:
                     cv2.circle(output_image, (int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])), 2, (0, 255, 0), -1)
             
             # Draw Hands
             if hand_result.hand_landmarks:
                 for hand_lms in hand_result.hand_landmarks:
                     for lm in hand_lms:
                        cv2.circle(output_image, (int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])), 2, (0, 0, 255), -1)

        # Extract keypoints
        keypoints = extract_landmarks(pose_result, hand_result, face_result)
        
        return output_image, keypoints

    def __del__(self):
        # Clean up
        pass
