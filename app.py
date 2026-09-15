import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import cot_reports as cot

# Configuration de la page
st.set_page_config(page_title="COT Cockpit - Kosov", layout="wide")

st.title("📊 Cockpit Macro — Rapport COT (CFTC)")
st.caption("Données hebdomadaires de la CFTC actualisées pour l'analyse institutionnelle")

# Menu latéral
st.sidebar.header("Configuration")
asset_choice = st.sidebar.selectbox(
    "Choisir un actif",
    ["EURO FX", "JAPANESE YEN", "BRITISH POUND", "GOLD", "CORN", "CRUDE OIL"]
)

@st.cache_data(ttl=86400)
def load_data():
    try:
        # Récupération automatique du rapport de l'année en cours
        df = cot.cot_year(year=2026, cot_report_type='traders_in_financial_futures_futures_only')
        return df
    except Exception as e:
        # Fallback si le format financier varie
        try:
            df = cot.cot_year(year=2026, cot_report_type='legacy_futures_only')
            return df
        except Exception:
            return None

with st.spinner("Extraction et traitement des données CFTC..."):
    df_cot = load_data()

if df_cot is not None and not df_cot.empty:
    st.success("✅ Données CFTC synchronisées avec succès.")
    
    # Filtrage sur l'actif sélectionné
    df_asset = df_cot[df_cot['Market_and_Exchange_Names'].str.contains(asset_choice, case=False, na=False)]
    
    if not df_asset.empty:
        # Tri chronologique
        df_asset = df_asset.sort_values(by='As_of_Date_In_YYYY-MM-DD', ascending=True)
        
        # Récupération de la dernière ligne
        latest = df_asset.iloc[-1]
        date_str = str(latest['As_of_Date_In_YYYY-MM-DD'])[:10]
        
        st.info(f"Dernier rapport disponible du : **{date_str}**")
        
        # Calcul des positions nettes
        if 'Lev_Money_Positions_Long_All' in df_asset.columns:
            # Format Financial Futures (Leveraged / Asset Mgr)
            df_asset['Leveraged_Net'] = df_asset['Lev_Money_Positions_Long_All'] - df_asset['Lev_Money_Positions_Short_All']
            df_asset['AssetMgr_Net'] = df_asset['Asset_Mgr_Positions_Long_All'] - df_asset['Asset_Mgr_Positions_Short_All']
            
            col1, col2 = st.columns(2)
            col1.metric("Leveraged Funds (Net)", f"{int(df_asset['Leveraged_Net'].iloc[-1]):,}")
            col2.metric("Asset Managers (Net)", f"{int(df_asset['AssetMgr_Net'].iloc[-1]):,}")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_asset['As_of_Date_In_YYYY-MM-DD'], y=df_asset['Leveraged_Net'], name='Leveraged Funds (Net)', line=dict(color='orange', width=2)))
            fig.add_trace(go.Scatter(x=df_asset['As_of_Date_In_YYYY-MM-DD'], y=df_asset['AssetMgr_Net'], name='Asset Managers (Net)', line=dict(color='cyan', width=2)))
            fig.update_layout(template="plotly_dark", height=500, title=f"Évolution des positions sur {asset_choice}")
            st.plotly_chart(fig, use_container_width=True)

        else:
            # Format Legacy (Non-Commercials / Commercials)
            df_asset['NonComm_Net'] = df_asset['NonComm_Positions_Long_All'] - df_asset['NonComm_Positions_Short_All']
            df_asset['Comm_Net'] = df_asset['Comm_Positions_Long_All'] - df_asset['Comm_Positions_Short_All']
            
            col1, col2 = st.columns(2)
            col1.metric("Large Speculators / NonComm (Net)", f"{int(df_asset['NonComm_Net'].iloc[-1]):,}")
            col2.metric("Commercials (Net)", f"{int(df_asset['Comm_Net'].iloc[-1]):,}")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_asset['As_of_Date_In_YYYY-MM-DD'], y=df_asset['NonComm_Net'], name='Non-Commercials (Net)', line=dict(color='green', width=2)))
            fig.add_trace(go.Scatter(x=df_asset['As_of_Date_In_YYYY-MM-DD'], y=df_asset['Comm_Net'], name='Commercials (Net)', line=dict(color='red', width=2)))
            fig.update_layout(template="plotly_dark", height=500, title=f"Évolution des positions sur {asset_choice}")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Aucune donnée trouvée pour {asset_choice}. Essaie un autre actif.")
else:
    st.error("Impossible de récupérer les rapports. Le serveur de la CFTC est en maintenance.")
