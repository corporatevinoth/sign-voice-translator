import numpy as np

def extract_landmarks(pose_result, hand_result, face_result):
    """
    Extracts and flattens landmarks from MediaPipe Tasks API results.
    Returns a concatenated numpy array of pose, face, left_hand, and right_hand landmarks.
    """
    # Pose landmarks
    if pose_result and pose_result.pose_landmarks:
        # Assuming single person detection [0]
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in pose_result.pose_landmarks[0]]).flatten()
    else:
        pose = np.zeros(33*4)

    # Face landmarks
    if face_result and face_result.face_landmarks:
        face = np.array([[res.x, res.y, res.z] for res in face_result.face_landmarks[0]]).flatten()
    else:
        face = np.zeros(468*3)
        
    # Hand landmarks
    # hand_result.hand_landmarks is a list of lists (one per hand)
    # hand_result.handedness is a list of lists (one per hand)
    # We need to map left/right correctly
    lh = np.zeros(21*3)
    rh = np.zeros(21*3)

    if hand_result and hand_result.hand_landmarks:
        for i, landmarks in enumerate(hand_result.hand_landmarks):
             # Handedness info
             if i < len(hand_result.handedness):
                 # access category name (Left or Right)
                 # Note: MediaPipe Tasks API: "Left" usually means capture's left (which is person's right? need to verify)
                 # Usually matches index.
                 label = hand_result.handedness[i][0].category_name
                 
                 flat_hand = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
                 
                 if label == "Left":
                     lh = flat_hand
                 elif label == "Right":
                     rh = flat_hand

    return np.concatenate([pose, face, lh, rh])
