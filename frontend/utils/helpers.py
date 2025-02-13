import streamlit as st
import pymongo
import pandas as pd
import plotly.graph_objects as go

from utils.tools import COLUMNS_CHART, QUERY_FIELDS, SYMBOLS


# Initialize connection with mongodb
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])


def get_data_from_ticker(ticker, stocks):
    stock_found = []
    for stock in stocks:
        if stock["_id"] == ticker:
            stock_found = stock["data"]
            break
    return stock_found

def preprocess_data( sexe ):
    return 

def predict_tension():
    return 

def get_visual_representation():
    return 

def load_patient_data():
    return 

# get stocks in streaming mongo database after 1 min
@st.cache_data(ttl=60)
def get_stocks(_client):
    stock_db = _client.streaming_db
    stocks = stock_db.get_collection("stocks")
    data = list(
        stocks.aggregate(
            [
                {
                    "$project": QUERY_FIELDS,
                },
                {
                    "$match": {
                        "symbol": {"$in": SYMBOLS},
                    },
                },
                {
                    "$group": {"_id": "$symbol", "data": {"$push": "$$ROOT"}},
                },
            ],
        )
    )

    return data


# return the figure from chart associate to the specific symbol parameter and data frame
def get_figure(data_ticker, symbol):

    df = pd.DataFrame(
        data_ticker,
        columns=COLUMNS_CHART,
    )
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            name=symbol,
            x=pd.to_datetime(df["time"]),
            open=df["open"],
            high=df["high"],
            close=df["close"],
            low=df["low"],
        )
    )

    return fig

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# Charger les données patients
@st.cache_data
def load_patient_data():
    file_path = "C://KOHE//OneDrive - KOHE//Bureau//Dathaton IA School//streamlet_pjt//patients (1).csv"
    df = pd.read_csv(file_path)
    return df

# Prétraitement des données
def preprocess_data(df):
    df = df.dropna()
    numerical_cols = ["Taille (cm)", "Poids (kg)", "Epaisseur_Tension", "Distance_Acromion_G", "Distance_Acromion_D", 
                      "Distance_EIPS_G", "Distance_EIPS_D", "Distance_T4", "Distance_L1"]
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    df["Rapport_Taille_Poids"] = df["Taille (cm)"] / df["Poids (kg)"]
    return df

# Charger le modèle pré-entraîné
model_path = "C://KOHE//OneDrive - KOHE//Bureau//Dathaton IA School//streamlet_pjt//joblib_model.sav"
model = joblib.load(model_path) if joblib.os.path.exists(model_path) else None

# Prédiction de la tension
def predict_tension(data_patient):
    if model:
        features = ["Taille (cm)", "Poids (kg)", "Epaisseur_Tension", "Distance_Acromion_G", "Distance_Acromion_D", 
                    "Distance_EIPS_G", "Distance_EIPS_D", "Distance_T4", "Distance_L1", "Rapport_Taille_Poids"]
        X_patient = data_patient[features]
        prediction = model.predict_proba(X_patient)[0][1]  # Probabilité de tension
        return {
            "probability": prediction,
            "location": "Épaule" if prediction > 0.5 else "Bassin",
            "intensity": round(prediction * 10, 2),
        }
    else:
        return {"probability": 0, "location": "Inconnu", "intensity": 0}

# Générer une représentation graphique des tensions
def get_visual_representation(data_patient):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=["Distance_Acromion_G", "Distance_Acromion_D", "Distance_EIPS_G", "Distance_EIPS_D", "Distance_T4", "Distance_L1"],
            y=data_patient.iloc[0, 5:].values,
            mode='lines+markers',
            name='Posture Analysis'
        )
    )
    return fig
