import pyttsx3

try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Warning: Could not initialize TTS engine: {e}")
    engine = None

def speak(text):
    """
    Converts text to speech.
    """
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error during speech generation: {e}")
    else:
        print(f"TTS Engine not available. Would have said: {text}")
