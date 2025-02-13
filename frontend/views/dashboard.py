import streamlit as st
from utils.helpers import (
    get_data_from_ticker,
    get_figure,
    get_stocks,
    init_connection,
)
from utils.tools import SYMBOLS
import streamlit as st
from utils.helpers import (
    load_patient_data,
    preprocess_data,
    predict_tension,
    get_visual_representation,
)

# get client connection
client = init_connection()


def app():

    st.title("Candlestick chart for tickers in tab section below")

    st.text("This dashboard allow user to show chart associate to specific ticker.")

    st.subheader("Click on ticker tab below that you want to show the chart")

    stocks = get_stocks(client)

    tabs = st.tabs(tabs=SYMBOLS)

    for i, tab in enumerate(tabs):

        with tab:
            data_ticker = get_data_from_ticker(ticker=SYMBOLS[i], stocks=stocks)
            if len(data_ticker) > 0:
                st.subheader(f"Candlestick Chart for {SYMBOLS[i]} ticker ")
                fig = get_figure(data_ticker=data_ticker, symbol=SYMBOLS[i])
                st.plotly_chart(fig)
            else:
                st.write(f"Candlestick Chart for {SYMBOLS[i]} not available ")





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
