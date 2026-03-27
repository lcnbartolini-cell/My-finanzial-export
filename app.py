import streamlit as st
import yfinance as yf
import google.generativeai as genai

# 1. Recupero della chiave dai Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.warning("⚠️ Inserisci la chiave GOOGLE_API_KEY nei Secrets di Streamlit.")
    st.stop()

# 2. Configurazione Google AI
genai.configure(api_key=api_key)

st.title("Financial Pilot AI")

# Elenco titoli da monitorare
tickers = ["NVDA", "BTC-USD", "GC=F", "CL=F"]
data_summary = ""

st.subheader("Quotazioni in tempo reale")

# 3. Recupero dati da Yahoo Finance
for t in tickers:
    try:
        stock = yf.Ticker(t)
        # Usiamo 1d per essere veloci e non essere bloccati
        hist = stock.history(period="5d")
        if not hist.empty:
            last_price = hist['Close'].iloc[-1]
            data_summary += f"{t}: {last_price:.2f}\n"
            st.write(f"📈 **{t}**: {last_price:.2f}")
    except Exception as e:
        st.error(f"Errore su {t}: {e}")

st.divider()
st.subheader("💡 Il Consiglio dell'IA")

# 4. Generazione del consiglio con il nome modello corretto
if data_summary:
    try:
        # Usiamo il percorso completo "models/" richiesto dalle ultime versioni
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        
        prompt = f"Analizza questi dati finanziari e dai un consiglio sintetico di trading: {data_summary}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            st.info(response.text)
        else:
            st.warning("L'IA non ha prodotto una risposta.")
            
    except Exception as e:
        st.error(f"Errore IA: {e}")
else:
    st.error("Non sono riuscito a recuperare dati dai mercati.")
