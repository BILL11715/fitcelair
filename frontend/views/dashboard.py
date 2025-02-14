import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np

# Charger les modèles et l'encodeur
label_encoder = joblib.load("model_classification/label_encoder.pkl")
random_forest_model = joblib.load("model_classification/random_forest_model.pkl")
svm_model = joblib.load("model_classification/svm_model.pkl")
model = joblib.load("model_classification/joblib_model.sav")

def load_patient_data():
    """ Fonction simulant le chargement des données patients """
    data = {
        "Âge": np.random.randint(18, 65, 50),
        "Taille (cm)": np.random.randint(150, 200, 50),
        "Poids (kg)": np.random.randint(50, 100, 50),
        "Type de pied": np.random.choice(["Creux", "Plat", "Normal"], 50),
        "Déséquilibres posturaux": np.random.choice(
            ["Genoux valgum", "Cyphose dorsale", "Hyperlordose lombaire", "Épaule antépulsée "], 50
        ),
        "Présence de tensions": np.random.choice(["Oui", "Non"], 50),
    }
    return pd.DataFrame(data)

def app():
    # Mise en page et design
    st.markdown(
        """
        <style>
        .header {
            text-align: center;
            color: #4CAF50;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .description {
            text-align: center;
            font-size: 18px;
            color: #555;
            margin-bottom: 40px;
        }
        </style>
        <div class="header">Tableau de Bord - Analyse Posturale</div>
        <div class="description">
            Découvrez les tendances et statistiques sur les déséquilibres posturaux grâce à notre IA.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Chargement des données patients
    df = load_patient_data()

    # Affichage des données sous forme de tableau
    st.subheader("Aperçu des données patients 📊")
    st.dataframe(df.head(10))

    # Visualisation des déséquilibres posturaux
    st.subheader("Distribution des déséquilibres posturaux")
    fig1 = px.histogram(df, x="Déséquilibres posturaux", color="Présence de tensions",
                        barmode="group", text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Analyse des types de pieds et tensions
    st.subheader("Corrélation entre le type de pied et les tensions")
    fig2 = px.pie(df, names="Type de pied", title="Répartition des types de pied",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig2, use_container_width=True)

    # Statistiques générales
    st.subheader("Statistiques générales")
    col1, col2, col3 = st.columns(3)
    col1.metric("Âge moyen", f"{df['Âge'].mean():.1f} ans")
    col2.metric("Taille moyenne", f"{df['Taille (cm)'].mean():.1f} cm")
    col3.metric("Poids moyen", f"{df['Poids (kg)'].mean():.1f} kg")

    st.markdown(
        """
        <div style="text-align: center; margin-top: 30px;">
            <h3>Analyse approfondie</h3>
            <p>Ces données permettent d'affiner nos recommandations pour améliorer la posture et réduire les tensions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    app()



# # Charger et préparer les données
# df = load_patient_data()
# df = preprocess_data(df)

# # Configuration du tableau de bord
# st.title("Analyse des Déséquilibres Posturaux et Prédiction des Tensions")
# st.text("Ce tableau de bord permet d'analyser les déséquilibres posturaux et de prédire les tensions corporelles associées.")

# # Sélection du patient
# patients = df["ID"].unique()
# selected_patient = st.selectbox("Sélectionnez un patient :", patients)

# # Extraction des données du patient
# data_patient = df[df["ID"] == selected_patient]

# if not data_patient.empty:
#     st.subheader(f"Prédiction des tensions pour le patient {selected_patient}")
#     prediction = predict_tension(data_patient)
    
#     st.metric(label="Probabilité de tension", value=f"{prediction['probability']*100:.2f}%")
#     st.metric(label="Localisation prédite", value=prediction['location'])
#     st.metric(label="Intensité estimée", value=prediction['intensity'])
    
#     # Affichage du schéma associé
#     fig = get_visual_representation(data_patient)
#     st.plotly_chart(fig)
# else:
#     st.write("Aucune donnée disponible pour ce patient.")
