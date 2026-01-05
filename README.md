# Sign Voice Translator

A bidirectional AI-powered translator that converts sign language to voice and voice to sign language.

## Features

- **Sign to Voice**: Uses computer vision to interpret sign language gestures and converts them to spoken audio.
- **Voice to Sign**: Converts spoken language into sign language animations or visuals.
- **Real-time Processing**: Designed for low-latency communication.

## Setup

1.  **Prerequisites**:
    - Python 3.8+
    - Docker (optional, for containerized deployment)

2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Running the Application**:
    ```bash
    python app/sign_to_voice.py
    ```
    Or use the Docker setup:
    ```bash
    start_docker.bat
    ```

## Project Structure

- `app/`: Source code for the application.
- `app/utils/`: Utility functions (landmarks, etc.).
- `requirements.txt`: Python dependencies.
