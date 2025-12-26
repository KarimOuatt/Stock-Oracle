import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly

st.set_page_config(layout="wide") # Utilise tout l'écran
st.title("📈 Stock Oracle - Analyse Boursière")

# 1. Barre latérale pour choisir l'action
with st.sidebar:
    st.header("Configuration")
    ticker = st.text_input("Symbole de l'action (ex: AAPL, TSLA, MSFT, GOOG)", value="AAPL")
    periode = st.selectbox("Période d'analyse", ["1mo", "3mo", "6mo", "1y", "5y", "max"], index=3)

# 2. Récupération des données (Yahoo Finance)
if ticker:
    st.write(f"Chargement des données pour **{ticker}**...")
    # On télécharge les données
    try:
        data = yf.download(ticker, period=periode)
        
        # 3. Création du Graphique "Candlestick" (Le truc de Pro)
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Prix du Marché"
        )])

        # Mise en forme du graphique
        fig.update_layout(
            title=f"Cours de l'action {ticker}",
            yaxis_title="Prix ($)",
            xaxis_rangeslider_visible=False, # On cache le slider moche du bas
            template="plotly_dark", # Mode sombre pour faire "Hacker"
            height=600
        )

        # Affichage
        st.plotly_chart(fig, use_container_width=True)

        # Petit tableau de données brutes en dessous
        with st.expander("Voir les données brutes"):
            st.dataframe(data)

    except Exception as e:
        st.error(f"Erreur : Impossible de trouver l'action '{ticker}'. Vérifie le symbole.")