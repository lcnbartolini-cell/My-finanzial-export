import streamlit as st
import yfinance as f
import google.generativeai as genai

# Forza la lettura della chiave dai Secrets
api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Collega la tua Chiave IA nei Secrets di Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

st.title("Financial Pilot AI")

# Lista ticker
tickers = ["NVDA", "BTC-USD", "GC=F", "CL=F"]
data_summary = ""

for t in tickers:
    stock = f.Ticker(t)
    hist = stock.history(period="1mo")
    if not hist.empty:
        last_price = hist['Close'].iloc[-1]
        data_summary += f"{t}: {last_price:.2f}\n"
        st.write(f"📊 {t}: {last_price:.2f}")

st.subheader("Il Consiglio dell'IA")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(f"Analizza brevemente questi prezzi e dai un consiglio: {data_summary}")
st.info(response.text)
