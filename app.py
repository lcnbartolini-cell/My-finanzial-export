import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd

# CONFIGURAZIONE
st.set_page_config(page_title="Financial Pilot AI", page_icon="📊", layout="wide")
st.title("📊 Financial Pilot AI")

# RECUPERO CHIAVE DAI SECRETS (Sicuro al 100%)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY nei Secrets di Streamlit.")
    st.stop()

@st.cache_data(ttl=300)
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d", interval="1m")
        if hist.empty: hist = stock.history(period="5d")
        return hist
    except:
        return pd.DataFrame()

# DASHBOARD
tickers_fissi = ["NVDA", "BTC-USD", "GC=F", "CL=F"]
cols = st.columns(len(tickers_fissi))
for i, t in enumerate(tickers_fissi):
    hist = get_data(t)
    if not hist.empty:
        last_p = hist['Close'].iloc[-1]
        cols[i].metric(label=t, value=f"{last_p:.2f}")

st.divider()

# RICERCA E IA
user_query = st.text_input("Cerca Ticker Mondiale:", "NVDA").upper()
if user_query:
    hist_user = get_data(user_query)
    if not hist_user.empty:
        price = hist_user['Close'].iloc[-1]
        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            response = model.generate_content(f"Analizza l'asset {user_query} a {price:.2f}. Dimmi trend e consiglio in 3 righe.")
            st.success(f"💡 AI: {response.text}")
        except Exception as e:
            st.error(f"Errore IA: {e}")
        st.line_chart(hist_user['Close'])
