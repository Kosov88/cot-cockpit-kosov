import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from io import StringIO

# Configuration de la page Streamlit
st.set_page_config(page_title="COT Cockpit - Kosov", layout="wide")

st.title("📊 Cockpit Macro — Rapport COT (CFTC)")
st.caption("Données hebdomadaires de la CFTC actualisées pour l'analyse institutionnelle")

# Menu latéral (Sidebar)
st.sidebar.header("Configuration")
asset_choice = st.sidebar.selectbox(
    "Choisir un actif",
    ["EURO FX", "JAPANESE YEN", "BRITISH POUND", "GOLD", "CORN", "CRUDE OIL"]
)

@st.cache_data(ttl=86400)
def get_cot_data():
    # Récupération des données brutes CFTC (Financial Futures / Disaggregated)
    url = "https://www.cftc.gov/files/dea/history/fut_fin_txt_2026.txt"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        return None
    except Exception:
        return None

raw_data = get_cot_data()

if raw_data:
    st.success("✅ Données CFTC synchronisées avec succès.")
    
    # Structure de démonstration pour le Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric(label=f"Actif Sélectionné", value=asset_choice)
    col2.metric(label="Statut Large Speculators", value="Net Long", delta="+12.4%")
    col3.metric(label="Statut Commercials", value="Net Short", delta="-5.2%")

    st.markdown("---")
    st.subheader(f"📈 Analyse des Positions Nettes sur {asset_choice}")

    # Exemple de graphique interactif Plotly
    df_example = pd.DataFrame({
        "Semaine": ["S1", "S2", "S3", "S4"],
        "Large Specs Net": [15000, 18000, 22000, 24925],
        "Commercials Net": [-12000, -15000, -19000, -24925]
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_example["Semaine"], y=df_example["Large Specs Net"], mode='lines+markers', name='Large Speculators (Net)', line=dict(color='green', width=3)))
    fig.add_trace(go.Scatter(x=df_example["Semaine"], y=df_example["Commercials Net"], mode='lines+markers', name='Commercials (Net)', line=dict(color='red', width=3)))
    fig.update_layout(template="plotly_dark", height=450, margin=dict(l=20, r=20, t=30, b=20))
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Chargement des données brutes en cours ou serveur CFTC momentanément indisponible.")
