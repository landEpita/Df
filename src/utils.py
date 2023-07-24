import base64

import streamlit as st

from config import STYLE_CSS_PATH, DESCRIPTION_APP


@st.cache_data
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="10%",
    image_width="60%",
    image_height="",
    description=""
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
                [data-testid="stSidebarNav"]::before {
                content: "%s";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 16px;
                position: relative;
                top: 100px;
                color: white;
            }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
        description
    )


def add_logo(png_file, description=DESCRIPTION_APP):
    logo_markup = build_markup_for_logo(png_file, description=description)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_css(file_name=STYLE_CSS_PATH):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
