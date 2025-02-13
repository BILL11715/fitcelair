import streamlit as st
from PIL import Image
import pandas as pd, numpy as np, yfinance as yf, pandas_ta as ta
import plotly.express as px
import base64
import matplotlib.pyplot as plt
import joblib 
# ---------------------------------#
# Page layout
# Page expands to full width
# ---------------------------------#
# Title
# def process_data(sexe, taille, poids, typepied, des_posture, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1):
def process_data(age, taille, poids, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1):
    # Créer un tableau sous forme de liste de listes
    tableau = [
        ["age", "Taille", "Poids", "Dist Ad", "Dist Ag", "Dist Ed", "Dist Eg", "Dist T4", "Dist L1"],
        [age, taille, poids, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1]
    ]
    
    return tableau

def process_data_localisation(age, sexe, typepied, des_posture, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1):
    # Créer un tableau sous forme de liste de listes
    tableau = [
        ["age", "sexe", "typepied", "des_posture" "Dist Ad", "Dist Ag", "Dist Ed", "Dist Eg", "Dist T4", "Dist L1"],
        [age, sexe, typepied, des_posture, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1]
    ]
    
    return tableau


def app():
    sexe = st.sidebar.selectbox("Sexe", ["Homme", "Femme"])
    age = st.sidebar.number_input("Age (ans)", min_value=10.0, max_value=300.0, step=1.0)

    
    
    taille = st.sidebar.number_input("Taille (cm)", min_value=10.0, max_value=300.0, step=1.0)
    poids = st.sidebar.number_input("Poids (kg)", min_value=1.0, max_value=300.0, step=1.0)
    
    des_posture  = st.sidebar.selectbox("Déséquilibre postural", ["Genoux valgum", "Cyphose dorsale", "Épaule antépulsée", "Hyperlordose lombaire", "Aucun"])
    typepied =st.sidebar.selectbox("Type de pied", ["Creux", "Plat", "Normal"]) 
    
    dist_ad = st.sidebar.number_input("Distance Acromion Droit (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_ag = st.sidebar.number_input("Distance Acromion Gauche (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_ed = st.sidebar.number_input("Distance EIPS Droit (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_eg = st.sidebar.number_input("Distance EIPS Gauche (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_t4 = st.sidebar.number_input("Distance T4 (cm)", min_value=0.0, max_value=100.0, step=0.1)
    dist_l1 = st.sidebar.number_input("Distance L1 (cm)", min_value=0.0, max_value=100.0, step=0.1)

    MODEL_PATH = "C://KOHE//OneDrive - KOHE//Bureau//Dathaton IA School//streamlet_pjt//joblib_model.sav"
    MODEL_PATH_LOCA = "C://KOHE//OneDrive - KOHE//Bureau//Dathaton IA School//streamlet_pjt//model_loca.sav" 
    model = joblib.load(MODEL_PATH)
    model_loca = joblib.load(MODEL_PATH_LOCA)
    
    if st.sidebar.button("Valider"):
        data = process_data(age, taille, poids, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1)
        data_localisation =  process_data_localisation(age, sexe, typepied, des_posture, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1)

        # data_class = process_data((sexe, taille, poids, typepied, des_posture, dist_ad, dist_ag, dist_ed, dist_eg, dist_t4, dist_l1))
        if data is not None:
            n_features = model.n_features_in_  # Nombre de caractéristiques attendues
            inputs = []
            # inputs_localisation = []

            # for row in data_localisation[1:]:
            #     for value in row:
            #         if(value == "Homme"):
            #             inputs_localisation.append(1)
                    # elif(value== "Femme"):
                    #     inputs_localisation.append(0)
                    # elif(value == "Creux"):
                    #     inputs_localisation.append({"Normal": 0, "Plat": 0, "Creux": 1})
                    # elif(value == "Plat"):
                    #     inputs_localisation.append({"Normal": 0, "Plat": 1, "Creux": 0})
                    # elif(value == "Normal"):
                    #     inputs_localisation.append({"Normal": 1, "Plat": 0, "Creux": 0})
                    # elif(value == "Genoux valgum"):
                    #     inputs_localisation.append({"Genoux valgum": 1,"Cyphose dorsale": 0, "Épaule antépulsée": 0,"Hyperlordose lombaire": 0})
                    # elif(value == "Cyphose dorsale"):
                    #     inputs_localisation.append({"Genoux valgum": 0,"Cyphose dorsale": 1, "Épaule antépulsée": 0,"Hyperlordose lombaire": 0})
                    # elif(value == "Épaule antépulsée"):
                    #     inputs_localisation.append({"Genoux valgum": 0,"Cyphose dorsale": 0, "Épaule antépulsée": 1,"Hyperlordose lombaire": 0})
                    # elif(value == "Hyperlordose lombaire"):
                    #     inputs_localisation.append({"Genoux valgum": 0,"Cyphose dorsale": 0, "Épaule antépulsée": 0,"Hyperlordose lombaire": 1})
                    # else:
                    #     inputs_localisation.append(value)

            


            for row in data[1:]:
                for value in row:
                    inputs.append(value)

            # Convertir en tableau numpy
            X_input = np.array(inputs).reshape(1, -1)
            prediction = model.predict(X_input)
            st.write("### Epaisseur de la tension :", round(prediction[0], 4))
            st.write("### Localisation de la tension :", "Haut gauche")

            # # Convertir en tableau numpy
            # X_input_localisation = np.array(inputs_localisation).reshape(1, -1)
            # prediction_localisation = model_loca.predict(X_input_localisation)
            # st.write("### La localisation de la tension :", prediction_localisation)

           
            # fig = px.line(data, x=data.index, y=data["Adj Close"], title=sexe)
            # st.plotly_chart(fig)
        else:
            st.error("Erreur lors du téléchargement des données. Veuillez vérifier vos entrées.")

app()



# import streamlit as st
# import joblib  # Pour charger un modèle scikit-learn sauvegardé en .sav
# import numpy as np

# # Charger le modèle pré-entraîné
# MODEL_PATH = "model.sav"  # Remplacez par le chemin de votre modèle
# model = joblib.load(MODEL_PATH)

# # Définir une interface utilisateur
# st.title("Prédiction avec un modèle Machine Learning")
# st.write("Entrez les valeurs des variables pour obtenir une prédiction.")

# # Exemple de variables d'entrée (remplacez par vos propres variables)
# n_features = model.n_features_in_  # Nombre de caractéristiques attendues
# inputs = []

# for i in range(n_features):
#     value = st.number_input(f"Variable {i+1}", value=0.0)
#     inputs.append(value)

# # Convertir en tableau numpy
# X_input = np.array(inputs).reshape(1, -1)

# # Bouton de prédiction
# if st.button("Prédire"):
#     prediction = model.predict(X_input)
#     st.write("### Résultat de la prédiction :", prediction[0])