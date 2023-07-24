import streamlit as st

from config import LOGO_PATH
from src.utils import add_logo, load_css

import cv2
import numpy as np
import pandas as pd

from insightface.app import FaceAnalysis
import base64
import pandas as pd
import numpy as np
from PIL import Image
from io import BytesIO
from datetime import datetime

add_logo(LOGO_PATH)
load_css()

# CONSTANTS
WEBCAMNUM = 0 # from videocapture_index_check.py

def capture_face(video_capture, source_face, FRAME_WINDOW):
    for i in range(3):
        video_capture.read()

    while(True):
        ret, frame = video_capture.read()
        if frame is not None:
            # face detection
            small_frame = frame
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = st.session_state['model'].get(np.asarray(rgb_small_frame))

            if len(face_locations) > 0:
                new_frame = st.session_state['model_swap'].get(np.asarray(rgb_small_frame), face_locations[0], source_face, paste_back=True)

            FRAME_WINDOW.image(new_frame[:, :, ::-1])


def main():
    source = np.array(Image.open("./LBC/DEEP_Johnny.png").convert('RGB'))
    source_face = st.session_state['model'].get(np.asarray(source))[0]
    st.title("Face Swap")

    FRAME_WINDOW = st.image([])
    capture_face(st.session_state.video_capture, source_face,FRAME_WINDOW)

main()

