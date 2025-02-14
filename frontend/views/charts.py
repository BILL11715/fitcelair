import streamlit as st
from PIL import Image
import pandas as pd, numpy as np
import plotly.express as px
import base64
import matplotlib.pyplot as plt
import joblib
from PIL import Image
from pathlib import Path
# ---------------------------------#
# Page layout
# Page expands to full width
# ---------------------------------#

# Charger l'encodeur sauvegardé
label_encoder = joblib.load("model_classification/label_encoder.pkl")
#xgboost_model = joblib.load("model_classification/xgboost_model.pkl")
random_forest_model = joblib.load("model_classification/random_forest_model.pkl")
svm_model = joblib.load("model_classification/svm_model.pkl")
model = joblib.load("model_classification/joblib_model.sav")
        

    # Mapping des labels avec les chemins des images
image_paths = {
    "Bas du dos": "public/schema/bas_du_dos.png",
    "Gauche": "public/schema/gauche.png",
    "Haut gauche": "public/schema/patient_915_haut_gauche.png",
    "Bas gauche": "public/schema/bas_gauche.png",
    "Droite": "public/schema/droite.png",
    "Droite copie": "public/schema/droite_copie.png",
    "Haut du dos": "public/schema/haut_du_dos.png",
    "Haut droite": "public/schema/patient_886_haut_droit.png",
    "Bas droite": "public/schema/patient_918_bas_droit.png"
}
def app():
    # Header
    set_header()

    sexe = st.sidebar.selectbox("Sexe", ["Homme", "Femme"])
    age = st.sidebar.number_input("Age (ans)", min_value=0.0, max_value=300.0, step=1.0)
    taille = st.sidebar.number_input("Taille (cm)", min_value=0.0, max_value=300.0, step=1.0)
    poids = st.sidebar.number_input("Poids (kg)", min_value=0.0, max_value=300.0, step=1.0)
    des_posture = st.sidebar.selectbox("Déséquilibre postural", ["Genoux valgum", "Cyphose dorsale", "Épaule antépulsée", "Hyperlordose lombaire", "Aucun"])
    typepied = st.sidebar.selectbox("Type de pied", ["Creux", "Plat", "Normal"]) 
    dist_ag = st.sidebar.number_input("Distance Acromion Gauche (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_ad = st.sidebar.number_input("Distance Acromion Droit (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_eg = st.sidebar.number_input("Distance EIPS Gauche (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_ed = st.sidebar.number_input("Distance EIPS Droit (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_t4 = st.sidebar.number_input("Distance T4 (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_l1 = st.sidebar.number_input("Distance L1 (cm)", min_value=0.0, max_value=100.0, step=0.1)

    if st.sidebar.button("Valider"):
        data = process_data(age, taille, poids, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1)

        if data is not None:
            n_features = model.n_features_in_  # Nombre de caractéristiques attendues
            inputs = []
            
            for row in data[1:]:
                for value in row:
                    inputs.append(value)

            # Convertir en tableau numpy
            X_input = np.array(inputs).reshape(1, -1)
            prediction = model.predict(X_input)
            
            presence_tension = "oui"
            if (prediction[0] > 0.01):
                presence_tension = "oui"
            else:
                presence_tension = "non"
            
            X_test_transformed = pd.DataFrame([[age, sexe, taille, poids, typepied, presence_tension, des_posture, prediction[0], dist_ag, dist_ad, dist_eg, dist_ed, dist_t4, dist_l1]], columns=[
                "Âge", "Sexe", "Taille (cm)", "Poids (kg)", "Type de pied", 
                "Présence de tensions", "Déséquilibres posturaux",
                "Epaisseur_Tension", "Distance_Acromion_G", "Distance_Acromion_D", 
                "Distance_EIPS_G", "Distance_EIPS_D", "Distance_T4", "Distance_L1"
            ])
            # Prédire les classes
            y_pred = random_forest_model.predict(X_test_transformed)

            y_pred_decoded = label_encoder.inverse_transform(y_pred)
            

        st.write("### Localisation de la tension :", y_pred_decoded[0])
        st.write("### Epaisseur de la tension :", round(prediction[0], 4))

        st.write("### Score de confiance globale :", "38 %")

        
        # Vérification et affichage de l'image
        label = y_pred_decoded[0]
        image_path = Path(image_paths.get(label, ""))

        if image_path.exists():
            image = Image.open(image_path)

        # Redimensionner l'image
            image = image.resize((300, 300))  # Ajuste la taille ici si nécessaire

        # Centrer l'image
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.image(image, caption=f"Zone : {label}")
            
        else:
            st.error(f"Image introuvable pour {label} : {image_path}")

    # Footer
    set_footer()
    



def process_data(age, taille, poids, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1):
    # Créer un tableau sous forme de liste de listes
    tableau = [
        ["age", "Taille", "Poids", "Dist Ad", "Dist Ag", "Dist Ed", "Dist Eg", "Dist T4", "Dist L1"],
        [age, taille, poids, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1]
    ]
    return tableau


import base64

# Fonction pour afficher le header personnalisé
def set_header():
    st.markdown("""
        <style>
        .header {
            text-align: center;
            color: #4CAF50;
            font-size: 50px;
            font-weight: bold;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        .subtitle {
            text-align: center;
            color: #8BC34A;
            font-size: 25px;
            margin-bottom: 50px;
        }
        .description {
            text-align: center;
            color: #555;
            font-size: 18px;
            margin-bottom: 50px;
        }
        </style>
        <div class="header">
            Kinésithérapie & Analyse Posturale
        </div>
        <div class="subtitle">
            Améliorez votre posture grâce à Fitcelair
        </div>
        <div class="description">
            Utilisez nos outils pour analyser votre posture et obtenir des recommandations personnalisées.
        </div>
    """, unsafe_allow_html=True)

# Fonction pour afficher le footer personnalisé
def set_footer():
    st.markdown("""
        <style>
        .footer {
            position: absolute;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px 0;
            background-color: #4CAF50;
            color: white;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.2);
        }
        </style>
        <div class="footer">
            Développé par phoenix - Fitcelair
        </div>
    """, unsafe_allow_html=True)

# Appliquez le header et le footer à votre page




