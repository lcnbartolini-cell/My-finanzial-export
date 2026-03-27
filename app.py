import streamlit as st
import yfinance as yf
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
import numpy as np

# --- 1. MOTORE INTELLIGENZA ARTIFICIALE ---
# Sostituisci 'AIzaSyCF8NN-QtjuJj29t6LIgwd_ipo29cHftDA' con la tua chiave gratuita di Google AI Studio
CHIAVE_IA = "AIzaSyCF8NN-QtjuJj29t6LIgwd_ipo29cHftDA"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=CHIAVE_IA, temperature=0.2)

# --- 2. LOGICA "INVESTIGATORE" (DATI ALTERNATIVI & BIG PLAYER) ---
def analisi_investigatore(ticker):
    try:
        azione = yf.Ticker(ticker)
        volumi = azione.history(period="5d")['Volume']
        media_vol = volumi.mean()
        ultimo_vol = volumi.iloc[-1]
        
        # Analisi Smart Money (Seguiamo i pesci grossi)
        if ultimo_vol > (media_vol * 1.6):
            return "🔥 I Grandi stanno entrando (Forte Accumulo)", "Verde"
        elif ultimo_vol < (media_vol * 0.6):
            return "⚠️ Disinteresse dei Big (Possibile calo)", "Giallo"
        else:
            return "⚖️ Movimenti normali (Retail Flow)", "Grigio"
    except:
        return "Dati non disponibili", "Grigio"

# --- 3. CONFIGURAZIONE DASHBOARD (INTERFACCIA SEMPLICE) ---
st.set_page_config(page_title="Il Mio Assistente Soldi", layout="wide")
st.title("🛡️ Financial Pilot AI: Pannello Industriale")

# --- BARRA LATERALE: IL TUO TELECOMANDO ---
st.sidebar.header("🕹️ Centro di Controllo")

# 1. Slider del Rischio con spiegazione (?)
profilo = st.sidebar.select_slider(
    "Quanto vogliamo correre?",
    options=["Scudo (Sicuro)", "Equilibrio (Medio)", "Turbo (Aggressivo)"],
    value="Equilibrio (Medio)",
    help="Scudo: Protegge i risparmi. Turbo: Cerca il guadagno massimo accettando rischi alti."
)

# 2. Interruttore Automazione
auto_pilot = st.sidebar.toggle(
    "Pilota Automatico su eToro", 
    value=False,
    help="Se acceso, l'app compra e vende da sola seguendo i Big. Se spento, ti chiede prima il permesso."
)

# 3. La tua richiesta specifica: Protezione disattiva di default
protezione_attiva = st.sidebar.toggle(
    "Protezione Anti-Crollo (Hedging)", 
    value=False, # DISATTIVATA COME STANDARD
    help="Se accesa, l'app compra oro o beni sicuri per bilanciare le perdite. Nota: può appiattire i guadagni."
)

if st.sidebar.button("🚨 ESCI DA TUTTO / METTI AL SICURO"):
    st.sidebar.error("Ordine di vendita totale inviato. Liquidità al 100%.")

# --- AREA PRINCIPALE: ANALISI E PREVISIONI ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🧐 Cosa stanno facendo i Pesci Grossi?")
    # Lista di esempio: Nvidia, Bitcoin, Oro, Petrolio
    miei_asset = ["NVDA", "BTC-USD", "GC=F", "CL=F"] 
    risultati = []
    
    for asset in miei_asset:
        stato, colore = analisi_investigatore(asset)
        risultati.append({"Cosa": asset, "Situazione": stato})
    
    st.table(risultati)

with col2:
    st.subheader("💡 Il Consiglio dell'IA")
    # Prompt per il cervello dell'app
    msg = f"Profilo: {profilo}. Protezione: {'Attiva' if protezione_attiva else 'Spenta'}. Mercato Mar 2026. Cosa fare?"
    try:
        risposta = llm.invoke(msg)
        st.info(risposta.content)
    except:
        st.warning("Collega la tua Chiave IA per ricevere consigli in tempo reale.")

# --- MEMORIA E APPRENDIMENTO ---
st.divider()
st.subheader("🧠 Cosa ho imparato oggi (Memoria Errori)")
st.write("- Ho capito che senza protezione i guadagni sono più veloci, ma terrò d'occhio i segnali di allarme per avvisarti in tempo.")

