import mediapipe as mp
import importlib
import os

print(f"MediaPipe path: {mp.__path__}")

try:
    import mediapipe.python.solutions as solutions
    print("Successfully imported mediapipe.python.solutions")
    print(f"Solutions dir: {dir(solutions)}")
except ImportError as e:
    print(f"Failed to import mediapipe.python.solutions: {e}")

try:
    from mediapipe.python.solutions import holistic
    print("Successfully imported holistic")
except ImportError as e:
    print(f"Failed to import holistic: {e}")

# Check file structure
base_path = mp.__path__[0]
print("Listing mediapipe dir:")
try:
    print(os.listdir(base_path))
    python_path = os.path.join(base_path, 'python')
    if os.path.exists(python_path):
        print("Listing mediapipe/python dir:")
        print(os.listdir(python_path))
        sol_path = os.path.join(python_path, 'solutions')
        if os.path.exists(sol_path):
            print("Listing mediapipe/python/solutions dir:")
            print(os.listdir(sol_path))
    else:
        print("mediapipe/python does not exist")
except Exception as e:
    print(f"Error listing dir: {e}")
