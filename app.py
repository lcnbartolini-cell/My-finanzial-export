import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd

# ========================
# CONFIGURAZIONE PAGINA
# ========================
st.set_page_config(page_title="Financial Pilot AI", page_icon="📊", layout="wide")
st.title("📊 Financial Pilot AI - Analisi Globale")

# ========================
# CHIAVE API (Inserita direttamente)
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
        # Prova dati recenti, se chiusi (weekend) ne prende 5 giorni
        hist = stock.history(period="1d", interval="1m")
        if hist.empty:
            hist = stock.history(period="5d")
        return hist
    except:
        return pd.DataFrame()

# ========================
# 1. I TUOI PREFERITI (Monitoraggio Fissato)
# ========================
tickers_fissi = ["NVDA", "BTC-USD", "GC=F", "CL=F"]
st.subheader("🚀 Asset di Riferimento")
cols = st.columns(len(tickers_fissi))

for i, t in enumerate(tickers_fissi):
    hist = get_data(t)
    if not hist.empty:
        last_p = hist['Close'].iloc[-1]
        prev_p = hist['Close'].iloc[-2] if len(hist) > 1 else last_p
        change = last_p - prev_p
        
        label = t
        if t == "GC=F": label = "ORO (Gold)"
        if t == "CL=F": label = "PETROLIO (Crude)"
        
        cols[i].metric(label=label, value=f"{last_p:.2f}", delta=f"{change:.2f}")

st.divider()

# ========================
# 2. RICERCA LIBERA E ANALISI IA
# ========================
st.subheader("🔍 Analisi Qualsiasi Azione nel Mondo")
st.write("Inserisci il ticker di Yahoo Finance (es: AAPL per Apple, RACE.MI per Ferrari, ETH-USD per Ethereum)")

user_query = st.text_input("Cerca Ticker:", "NVDA").upper()

if user_query:
    hist_user = get_data(user_query)
    
    if not hist_user.empty:
        price = hist_user['Close'].iloc[-1]
        st.info(f"Dato attuale per **{user_query}**: {price:.2f}")

        # --- CHIAMATA IA ---
        try:
            # Prefisso "models/" aggiunto per evitare Errore 404
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            
            prompt = f"""
            Sei un analista finanziario. Analizza l'asset {user_query} che quota attualmente {price:.2f}.
            Considera il contesto di mercato globale.
            Fornisci: Trend, Rischi e un Consiglio operativo (compra/vendi/attendi) in max 4 righe.
            """
            
            response = model.generate_content(prompt)
            
            if response.text:
                st.success(f"💡 **L'Analisi di Gemini:**\n\n{response.text}")
        except Exception as e:
            st.error(f"Errore nell'analisi IA: {e}")

        # --- GRAFICO ---
        st.line_chart(hist_user['Close'])
    else:
        st.warning("Nessun dato trovato per questo ticker. Controlla il simbolo su Yahoo Finance.")

# ========================
# PIÈ DI PAGINA
# ========================
st.caption("Dati forniti da Yahoo Finance. L'analisi IA non costituisce sollecito al risparmio.")
