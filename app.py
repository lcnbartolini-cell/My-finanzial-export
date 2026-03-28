import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd

# ========================
# CONFIGURAZIONE PAGINA
# ========================
st.set_page_config(
    page_title="Financial Pilot AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Pilot AI")

# ========================
# CHIAVE API (Inserita direttamente per sbloccare)
# ========================
API_KEY_LUCIANO = "AIzaSyCF8NN-QtjuJj29t6LIgwd_ipo29cHftDA"
genai.configure(api_key=API_KEY_LUCIANO)

# ========================
# FUNZIONE RECUPERO DATI (Con Cache)
# ========================
@st.cache_data(ttl=300)
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Prova prima i dati dell'ultimo minuto
        hist = stock.history(period="1d", interval="1m")
        # Se i mercati sono chiusi (Weekend), prende gli ultimi 5 giorni
        if hist.empty:
            hist = stock.history(period="5d")
        return hist
    except:
        return pd.DataFrame()

# ========================
# DASHBOARD MERCATI
# ========================
tickers = ["NVDA", "BTC-USD", "GC=F", "CL=F"]
st.subheader("📈 Quotazioni e Variazioni")

cols = st.columns(len(tickers))
data_summary = ""

for i, t in enumerate(tickers):
    hist = get_data(t)
    if not hist.empty:
        last_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else last_price
        change = last_price - prev_price
        
        # Etichette più belle per Oro e Petrolio
        label_display = t
        if t == "GC=F": label_display = "ORO (Gold)"
        if t == "CL=F": label_display = "PETROLIO (Crude Oil)"

        cols[i].metric(
            label=label_display,
            value=f"{last_price:.2f}",
            delta=f"{change:.2f}"
        )
        data_summary += f"{label_display}: {last_price:.2f} (variazione {change:.2f})\n"
    else:
        cols[i].warning(f"Dati {t} non disp.")

st.divider()

# ========================
# ANALISI INTELLIGENZA ARTIFICIALE
# ========================
st.subheader("💡 Il Consiglio dell'Analista AI")

if data_summary:
    try:
        # CORREZIONE 404: aggiunto "models/" davanti
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        
        prompt = f"""
        Sei un analista finanziario esperto. Analizza questi dati e dai un consiglio:
        {data_summary}
        
        Sii sintetico: indica Trend, Opportunità e un consiglio finale in max 4 righe.
        """
        
        response = model.generate_content(prompt)
        
        if response.text:
            st.info(response.text)
        else:
            st.warning("L'IA non ha generato una risposta.")
    except Exception as e:
        st.error(f"Errore IA: {e}")
else:
    st.error("Impossibile analizzare: mancano i dati di mercato.")

# ========================
# GRAFICI
# ========================
st.subheader("📊 Analisi Grafica")
selected = st.selectbox("Seleziona asset da visualizzare", tickers)
hist_plot = get_data(selected)

if not hist_plot.empty:
    st.line_chart(hist_plot['Close'])
else:
    st.warning("Grafico non disponibile.")
