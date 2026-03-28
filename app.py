import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd

# ========================
# CONFIGURAZIONE PAGINA
# ========================
st.set_page_config(page_title="Financial Pilot AI", page_icon="📊", layout="wide")
st.title("📊 Financial Pilot AI - Global Analysis")

# ========================
# CHIAVE API
# ========================
API_KEY_LUCIANO = "AIzaSyCF8NN-QtjuJj29t6LIgwd_ipo29cHftDA"
genai.configure(api_key=API_KEY_LUCIANO)

# ========================
# FUNZIONE RECUPERO DATI
# ========================
@st.cache_data(ttl=300)
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d", interval="1m")
        if hist.empty:
            hist = stock.history(period="5d")
        return hist
    except:
        return pd.DataFrame()

# ========================
# 1. I TUOI PREFERITI (Fissi)
# ========================
tickers_fissi = ["NVDA", "BTC-USD", "GC=F", "CL=F"]
st.subheader("🚀 Asset Principali")
cols = st.columns(len(tickers_fissi))

for i, t in enumerate(tickers_fissi):
    hist = get_data(t)
    if not hist.empty:
        last_p = hist['Close'].iloc[-1]
        change = last_p - (hist['Close'].iloc[-2] if len(hist)>1 else last_p)
        label = t
        if t == "GC=F": label = "ORO"
        if t == "CL=F": label = "PETROLIO"
        cols[i].metric(label=label, value=f"{last_p:.2f}", delta=f"{change:.2f}")

st.divider()

# ========================
# 2. RICERCA GLOBALE (Qualsiasi azione)
# ========================
st.subheader("🔍 Ricerca Azione Mondiale")
user_query = st.text_input("Inserisci Ticker (es: AAPL, RACE.MI, ETH-USD, TSLA)", "AAPL").upper()

hist_user = get_data(user_query)

if not hist_user.empty:
    price = hist_user['Close'].iloc[-1]
    st.info(f"Analisi attuale per **{user_query}**: {price:.2f} USD/EUR")
    
    # Prepara dati per l'IA
    data_for_ai = f"Asset: {user_query}, Prezzo: {price:.2f}"
    
    # IA CONSIGLIO
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        prompt = f"Sei un esperto finanziario. Analizza {data_for_ai}. Dimmi trend, rischi e un consiglio operativo in 3 righe."
        response = model.generate_content(prompt)
        st.success(f"💡 **Consiglio IA:**\n\n{response.text}")
    except Exception as e:
        st.error(f"Errore IA: {e}")
        
    # GRAFICO
    st.line_chart(hist_user['Close'])
else:
    st.warning("Inserisci un ticker valido per vedere il grafico e l'analisi.")
