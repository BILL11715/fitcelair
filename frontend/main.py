import streamlit as st
from streamlit_option_menu import option_menu
from views import home, dashboard, charts, infos, about
from utils.tools import OPTION_MENU_ICONS, OPTION_MENU_ITEMS, OPTION_MENU_STYLE

# from PIL import Image

# st.set_page_config(layout="wide")


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run():
        # app = st.sidebar(
        with st.sidebar:
            app = option_menu(
                menu_title="Analysis",
                options=OPTION_MENU_ITEMS,
                icons=OPTION_MENU_ICONS,
                menu_icon="chat-text-fill",
                default_index=1,
                styles=OPTION_MENU_STYLE,
            )

        if app == "Home":
            home.app()
        if app == "Dashboard":
            dashboard.app()
        if app == "Charts":
            charts.app()
        # if app == "Infos":
        #     infos.app()
        # if app == "About":
        #     about.app()

    run()
