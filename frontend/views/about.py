import streamlit as st
from PIL import Image


def app():
    expander_bar = st.expander("About")
    expander_bar.markdown(
        """
    * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
    * **Data source:** ---.
    * **Credit:** ---.
    """
    )
