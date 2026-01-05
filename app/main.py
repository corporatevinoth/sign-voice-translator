import streamlit as st
import cv2
import queue
import time
from app.sign_to_voice import SignDetector
from app.voice_to_sign import VoiceTranslator

# Page Config
st.set_page_config(page_title="Sign-Voice Translator", layout="wide")

# Sidebar - Accessibility
st.sidebar.title("Accessibility Settings")
high_contrast = st.sidebar.checkbox("High Contrast Mode")
font_size = st.sidebar.slider("Font Size", 1, 3, 1)

# Apply accessibility styles
if high_contrast:
    st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

if font_size > 1:
    st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font_size: {font_size * 100}% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("AI-Powered Bidirectional Translator")

# Initialize modules in session state to persist across reruns
if 'sign_detector' not in st.session_state:
    st.session_state['sign_detector'] = SignDetector()
if 'voice_translator' not in st.session_state:
    st.session_state['voice_translator'] = VoiceTranslator()
    st.session_state['audio_queue'] = queue.Queue()
    st.session_state['voice_translator'].start_listening(st.session_state['audio_queue'])

col1, col2 = st.columns(2)

with col1:
    st.header("Sign -> Voice")
    st.write("Camera Feed (Detects Signs)")
    camera_placeholder = st.empty()
    st.write("Translated Text: [Placeholder]")

with col2:
    st.header("Voice -> Sign")
    st.write("Spoken Words:")
    text_placeholder = st.empty()
    st.write("Avatar Output:")
    avatar_placeholder = st.empty()

# Main processing loop
# Note: Streamlit execution model reruns the script on interaction. 
# For real-time loops, we typically use a "Start" button or a custom component.
# Here we use a simple checkbox to control the loop.
run_app = st.checkbox("Run Translator", value=False)

cap = cv2.VideoCapture(0)

while run_app:
    # 1. Sign to Voice
    ret, frame = cap.read()
    if ret:
        processed_frame, keypoints = st.session_state['sign_detector'].process_frame(frame)
        if processed_frame is not None:
            # Convert BGR to RGB for Streamlit
            img_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            camera_placeholder.image(img_rgb, channels="RGB")
    
    # 2. Voice to Sign
    try:
        # Get latest text from queue (non-blocking)
        while not st.session_state['audio_queue'].empty():
            text = st.session_state['audio_queue'].get_nowait()
            text_placeholder.markdown(f"**{text}**")
            
            # Simple logic to show animation placeholder
            words = text.lower().split()
            for word in words:
                if word in st.session_state['voice_translator'].gloss_map:
                    anim_file = st.session_state['voice_translator'].gloss_map[word]
                    avatar_placeholder.info(f"Playing animation: {anim_file}")
                    # In a real app, st.video(path) would go here
    except queue.Empty:
        pass

    # Small sleep to yield control
    time.sleep(0.05)

cap.release()
