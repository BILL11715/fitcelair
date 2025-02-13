import streamlit as st
from PIL import Image


def app():
    image = Image.open("./public/business.png")

    st.image(image, width=250)

    st.title("Real-Time Financial Data Analysis")
