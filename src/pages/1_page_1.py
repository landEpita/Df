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
COLOR_DARK = (0, 255, 0)
COLOR_WHITE = (0, 0, 0)
COLS_ENCODE = [f'{i}' for i in range(512)]

def draw_boxes_and_keypoints(image, detections, index_people):
    frames = []
    for i, detection in enumerate(detections):
        bbox = detection['bbox'].astype(int)
        frames.append(cv2.resize(image[bbox[1]:bbox[3], bbox[0]:bbox[2]], (300,300)))

        # Draw bounding box
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), COLOR_DARK, 2) #  (left, top),(right, bottom)

        cv2.rectangle(
            image, (bbox[0], bbox[3] + 35),
            (bbox[2], bbox[3]), COLOR_DARK, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        if index_people[i] == -1:
            cv2.putText(
                image, f"???", (bbox[0] + 5, bbox[3] + 25),
                font, .55, COLOR_WHITE, 1)
        else:
            cv2.putText(
                image, f"{st.session_state['name_base'][index_people[i]]}", (bbox[0] + 5, bbox[3] + 25),
                font, .55, COLOR_WHITE, 1)
    return frames

def distance_L2(embeddings, requetes):
    res = []
    for requete in requetes:
        distances = [np.linalg.norm(np.array(e) - np.array(requete)) for e in embeddings]
        min_dist = np.min(distances)
        # print(min_dist, np.argmin(distances))
        if min_dist < 30:
            res.append(np.argmin(distances))
        else:
            res.append(-1)
    return res

def add_hist(face, index, df):
    if index == -1:
        nom = "???"
    else:
        nom = st.session_state['name_base'][index]
    img = face[:, :, ::-1]
    # Convertir le tableau numpy en une image PIL
    img = Image.fromarray((img).astype(np.uint8))

    # Créer un buffer pour sauvegarder l'image en format PNG
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    # Créer la data URL
    img_data_url = "data:image/png;base64," + img_str

    # Créer un nouveau DataFrame pour cette ligne
    new_row = pd.DataFrame([[nom, img_data_url, datetime.now()]], columns=['Nom', 'Image', "DateTime"])

    # Ajouter la nouvelle ligne au DataFrame
    my_df = pd.concat([df, new_row], ignore_index=True)
        
    return my_df

def temporality_embedding(rolling_list, requetes, frames, index_people, TAB_WINDOW, df):
    for j , req in enumerate(requetes):         
        check_add = False
        list_emb = list(rolling_list.keys())
        distances = [np.linalg.norm(np.fromstring(e, dtype=req.dtype) - req) for e in list_emb]
        for i in range(len(distances)):
            rolling_list[list_emb[i]]["value"] = rolling_list[list_emb[i]]["value"] - 1
            if distances[i] < 9:
                rolling_list[list_emb[i]]["value"] = rolling_list[list_emb[i]]["value"] + 2
                if rolling_list[list_emb[i]]["value"] == 10 and rolling_list[list_emb[i]]["add"] == False:
                    rolling_list[list_emb[i]]["add"] = True
                    df = add_hist(frames[j], index_people[j], df)
                    TAB_WINDOW.dataframe(
                        df, 
                        use_container_width=True,         
                        column_config={
                            "Image": st.column_config.ImageColumn(
                                "Face", help="Streamlit app preview screenshots"
                            ),
                            "DataTime": st.column_config.DatetimeColumn(
                                "DataTime",
                                format="D MMM YYYY, h:mm a",
                                step=60,
                            ),
                        },
                        hide_index=True)
                check_add=True
            if rolling_list[list_emb[i]]["value"]  <= 0:
                del rolling_list[list_emb[i]]
        if check_add == False:
            rolling_list[req.tostring()] = {"value":1, "add": False}
    return rolling_list, df

def capture_face(video_capture, FRAME_WINDOW, TAB_WINDOW, CHART_WINDOW):
    df = pd.DataFrame(columns=['Nom', 'Image', 'DateTime'])
    count_faces = []
    rolling_list = {}
    for i in range(3):
        video_capture.read()

    while(True):
        ret, frame = video_capture.read()
        if frame is not None:
            initial_size = frame.shape
            # face detection
            small_frame = frame
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = st.session_state['model'].get(np.asarray(rgb_small_frame))

            if len(face_locations) > 0:
                requetes = np.array([face.embedding for face in face_locations])
                index_people = distance_L2(st.session_state['vector_base'], requetes)
                frames = draw_boxes_and_keypoints(small_frame, face_locations, index_people)
                rolling_list, df = temporality_embedding(rolling_list, requetes, frames, index_people, TAB_WINDOW, df)
                frame = small_frame

            count_faces.append(len(face_locations))
            FRAME_WINDOW.image(frame[:, :, ::-1])
            CHART_WINDOW.line_chart(count_faces, use_container_width=True, x=None, y=None)


def main():

    st.title("Face Recognition")

    col1, col2 = st.columns([1, 1])

    FRAME_WINDOW = col1.image([])
    TAB_WINDOW = col2.dataframe(pd.DataFrame(), use_container_width=True,  hide_index=True)

    CHART_WINDOW = st.line_chart([])

    capture_face(st.session_state.video_capture, FRAME_WINDOW, TAB_WINDOW, CHART_WINDOW)

main()

