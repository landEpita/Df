import streamlit as st

from config import LOGO_PATH
from src.utils import add_logo, load_css

import insightface
from insightface.app import FaceAnalysis
import pandas as pd
import cv2

# STATE

WEBCAMNUM = 0 # from videocapture_index_check.py
PATH_DATA = 'data/db.csv'
COLS_ENCODE = [f'{i}' for i in range(512)]


@st.cache_data
def load_known_data():
    DB = pd.read_csv(PATH_DATA,index_col=0)
    return (
        DB.index.to_numpy(), 
        DB[COLS_ENCODE].values,
        DB
        )

def get_key_from_value(search_value, my_dict):
    for key, value in my_dict.items():
        if value["text_long"] == search_value:
            return key


def main(
    title: str
) -> None:
    st.set_page_config(layout="wide", page_title=title, page_icon="🚀")

    if 'video_capture' not in st.session_state:
        st.session_state['video_capture'] = cv2.VideoCapture(WEBCAMNUM)

    if 'model' not in st.session_state:
        st.session_state['model'] = FaceAnalysis(providers=['CUDAExecutionProvider'],allowed_modules=['detection', 'recognition'] , name="buffalo_s")
        st.session_state['model'].prepare(ctx_id=0)

    if 'model_swap' not in st.session_state:
        st.session_state['model_swap'] = insightface.model_zoo.get_model("src/model/inswapper_128.onnx", providers=['CUDAExecutionProvider'])

    if 'vector_base' not in st.session_state or 'name_base' not in st.session_state or 'DB' not in st.session_state:
        name, emb, DB = load_known_data()
        st.session_state['vector_base'] = emb
        st.session_state['name_base'] = name
        st.session_state['DB'] = DB

    load_css()
    add_logo(LOGO_PATH)

    # Body
    st.title("Reconnaissance Faciale")
    st.markdown("""
La reconnaissance faciale est une technologie sophistiquée qui permet d'identifier ou de vérifier l'identité d'une personne à partir de son visage.

## Principe de Fonctionnement
La reconnaissance faciale fonctionne en capturant, analysant et comparant des motifs faciaux. Le processus peut se diviser en trois étapes principales:

- **Capture:** Une image ou une vidéo de la personne est capturée par une caméra.
- **Analyse:** L'image ou la vidéo capturée est ensuite analysée pour extraire des caractéristiques uniques du visage.
- **Comparaison:** Ces caractéristiques sont ensuite comparées à une base de données d'images pour trouver une correspondance.

## Applications de la Reconnaissance Faciale  
                
La reconnaissance faciale a de nombreuses applications pratiques:

- **Sécurité:** Elle est largement utilisée dans la surveillance de la sécurité pour identifier des individus dans les aéroports, les stades ou les centres commerciaux.
- **Smartphones:** Elle est aussi utilisée pour le déverrouillage des appareils mobiles.
- **Réseaux Sociaux:** Les plateformes comme Facebook l'utilisent pour suggérer des tags sur les photos.
                
## Défis et Controverses  
                
Bien que la reconnaissance faciale soit une technologie puissante, elle soulève également des problèmes importants:

- **Vie privée:** Le risque d'atteinte à la vie privée est une préoccupation majeure, car la technologie peut être utilisée pour surveiller les gens sans leur consentement.
- **Précision:** La précision de la technologie est une autre préoccupation. Des études ont montré que certains systèmes de reconnaissance faciale peuvent présenter des biais, notamment envers certaines ethnies, genres ou âges.
- **Réglementation:** Enfin, il y a un manque de réglementation claire autour de l'utilisation de cette technologie.
                """)


if __name__ == "__main__":
    main("Face Recognition")
