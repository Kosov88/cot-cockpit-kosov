import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Configuration de la page
st.set_page_config(page_title="COT Cockpit - Kosov", layout="wide")

st.title("📊 Cockpit Macro — Rapport COT (CFTC)")
st.caption("Données hebdomadaires de la CFTC actualisées pour l'analyse institutionnelle")

# Dictionnaire de correspondance des actifs avec l'API CFTC (Code CFTC & Noms)
ASSETS = {
    "EURO FX": "EURO FX - CHICAGO MERCANTILE EXCHANGE",
    "JAPANESE YEN": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
    "BRITISH POUND": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
    "GOLD": "GOLD - COMMODITY EXCHANGE INC.",
    "CORN": "CORN - CHICAGO BOARD OF TRADE",
    "CRUDE OIL": "CRUDE OIL LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE"
}

st.sidebar.header("Configuration")
asset_choice = st.sidebar.selectbox("Choisir un actif", list(ASSETS.keys()))

@st.cache_data(ttl=3600)
def fetch_cot_data_api(market_name):
    # API publique Socrata de la CFTC (Futures Only Legacy / Disaggregated)
    url = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"
    
    # Paramètres de la requête API : On filtre par marché et on trie par date
    params = {
        "$where": f"market_and_exchange_names like '%{market_name}%'",
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": 100
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        res = requests.get(url, params=params, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data)
                return df
    except Exception as e:
        return None
    return None

with st.spinner(f"Récupération des données API pour {asset_choice}..."):
    cftc_name = ASSETS[asset_choice]
    df_asset = fetch_cot_data_api(asset_choice)

if df_asset is not None and not df_asset.empty:
    st.success("✅ Données CFTC récupérées via l'API avec succès.")
    
    # Tri chronologique (du plus ancien au plus récent pour le graphique)
    df_asset = df_asset.sort_values(by='report_date_as_yyyy_mm_dd', ascending=True)
    
    # Conversion des colonnes numériques
    num_cols = [
        'noncomm_positions_long_all', 'noncomm_positions_short_all',
        'comm_positions_long_all', 'comm_positions_short_all'
    ]
    for col in num_cols:
        if col in df_asset.columns:
            df_asset[col] = pd.to_numeric(df_asset[col], errors='coerce').fillna(0)
            
    # Calcul des positions nettes
    df_asset['NonComm_Net'] = df_asset['noncomm_positions_long_all'] - df_asset['noncomm_positions_short_all']
    df_asset['Comm_Net'] = df_asset['comm_positions_long_all'] - df_asset['comm_positions_short_all']
    
    latest_date = df_asset['report_date_as_yyyy_mm_dd'].iloc[-1][:10]
    st.info(f"Dernier rapport disponible : **{latest_date}**")
    
    # Métriques principales
    col1, col2 = st.columns(2)
    last_noncomm = int(df_asset['NonComm_Net'].iloc[-1])
    last_comm = int(df_asset['Comm_Net'].iloc[-1])
    
    col1.metric("Large Speculators / Non-Comm (Net)", f"{last_noncomm:,}")
    col2.metric("Commercials / Hedgers (Net)", f"{last_comm:,}")
    
    # Graphique Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_asset['report_date_as_yyyy_mm_dd'], 
        y=df_asset['NonComm_Net'], 
        name='Large Speculators (Net)', 
        line=dict(color='limegreen', width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=df_asset['report_date_as_yyyy_mm_dd'], 
        y=df_asset['Comm_Net'], 
        name='Commercials (Net)', 
        line=dict(color='crimson', width=2.5)
    ))
    
    fig.update_layout(
        template="plotly_dark",
        height=500,
        title=f"Évolution des positions nettes — {asset_choice}",
        xaxis_title="Date",
        yaxis_title="Nombre de contrats (Net)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("⚠️ Impossible de contacter l'API de la CFTC ou aucun résultat trouvé pour cet actif.")
    
