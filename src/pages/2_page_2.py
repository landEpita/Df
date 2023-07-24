import os
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

from config import LOGO_PATH
from src.utils import add_logo, load_css

add_logo(LOGO_PATH)
load_css()




# Chemin du dossier contenant les images
images_folder = "LBC"
PATH_DATA = 'data/db.csv'

# Hauteur uniforme pour toutes les images
target_height = 300

def display_images():
    # Liste des fichiers dans le dossier
    image_files = os.listdir(images_folder)

    # Filtre les fichiers pour ne conserver que les images (basé sur l'extension du fichier)
    image_files = [file for file in image_files if file.endswith(('.png', '.jpg', '.jpeg'))]

    # Organise les images en une grille 3x3
    for i in range(0, len(image_files), 3):
        row_files = image_files[i:i+3]
        col1, col2, col3 = st.columns(3)
    
        with col1:
            if len(row_files) > 0:
                image = Image.open(os.path.join(images_folder, row_files[0]))
                width = int(image.width * target_height / image.height)
                image = image.resize((width, target_height))
                st.image(image)
                st.write(row_files[0].split(".")[0])  # Affiche le nom sans l'extension du fichier

        with col2:
            if len(row_files) > 1:
                image = Image.open(os.path.join(images_folder, row_files[1]))
                width = int(image.width * target_height / image.height)
                image = image.resize((width, target_height))
                st.image(image)
                st.write(row_files[1].split(".")[0])  # Affiche le nom sans l'extension du fichier

        with col3:
            if len(row_files) > 2:
                image = Image.open(os.path.join(images_folder, row_files[2]))
                width = int(image.width * target_height / image.height)
                image = image.resize((width, target_height))
                st.image(image)
                st.write(row_files[2].split(".")[0])  # Affiche le nom sans l'extension du fichier


def upload_image():
    st.sidebar.title("Ajouter une nouvelle photo")

    uploaded_file = st.sidebar.file_uploader("Choisissez une image", type=['png', 'jpg', 'jpeg'])
    name = st.sidebar.text_input("Entrez le nom et le prénom de la personne")

    if st.sidebar.button("Envoyer"):
        if uploaded_file is not None and name:
            image = Image.open(uploaded_file)
            image.save(os.path.join(images_folder, name + '.png'))  # Sauvegarde en format png
            face_locations = st.session_state['model'].get(np.asarray(image))
            if len(face_locations) > 0:
                st.session_state['DB'].loc[name] = face_locations[0].embedding
                st.session_state['DB'].to_csv(PATH_DATA)


            st.sidebar.success("Image ajoutée avec succès !")




def main():
    st.title("Galerie de visages")
    display_images()
    upload_image()

main()
