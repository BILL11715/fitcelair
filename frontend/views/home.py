# import streamlit as st
# from PIL import Image


# def app():
#     image = Image.open("./public/2.png")

#     st.image(image, width=250)

#     st.title("Real-Time Financial Data Analysis")
#     st.markdown(
#         """
#     This app retrieves stock --- from the **---**!

#     """
#     )

#     st.markdown(
#         """
#     ## Welcome
#     ### Let's analyze together!
#     ### Let's go!
#     """
#     )

import streamlit as st
from PIL import Image

def app():
    # Affichage de l'image avec une meilleure mise en page
    st.markdown(
        """
        <style>
        .centered-image {
            display: flex;
            justify-content: center;
        }
        .title {
            text-align: center;
            color: #4CAF50;
            font-size: 36px;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #8BC34A;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .description {
            text-align: justify;
            font-size: 18px;
            color: #555;
            margin: 20px auto;
            max-width: 800px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Charger et afficher l'image en grand format
    image = Image.open("./public/2.png")
    st.image(image, caption="Analyse Posturale et Kinésithérapie Assistée par IA")

    # Titre principal
    st.markdown('<div class="title">Kinésithérapie & Analyse Posturale avec Fitcelair</div>', unsafe_allow_html=True)

    # Sous-titre
    st.markdown('<div class="subtitle">Améliorez votre posture grâce aux nouvelles technologies</div>', unsafe_allow_html=True)

    # Présentation du projet
    st.markdown(
        '<div class="description">'
        "Bienvenue sur notre plateforme d'analyse posturale assistée par intelligence artificielle ! "
        "Notre outil innovant vous aide à détecter et comprendre les déséquilibres posturaux en utilisant des modèles avancés "
        "de Machine Learning. Grâce à une analyse détaillée de plusieurs paramètres physiologiques, nous fournissons des recommandations "
        "personnalisées pour améliorer votre posture et votre bien-être général."
        "</div>",
        unsafe_allow_html=True,
    )

    # Appel à l'action
    st.markdown(
        '<div style="text-align: center; margin-top: 30px;">'
        '<h3>Prêt à analyser votre posture ?</h3>'
        '<p>Entrez vos informations et découvrez comment améliorer votre équilibre corporel.</p>'
        "</div>",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    app()

