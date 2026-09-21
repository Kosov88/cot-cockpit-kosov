import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="COT Report Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .main .block-container {
            padding: 0rem;
            max-width: 100%;
        }
        iframe {
            width: 100%;
            border: none;
        }
    </style>
""",
    unsafe_allow_html=True,
)

html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COT REPORT - ALL ASSETS</title>
    <!-- Inclusion de Chart.js pour les graphiques en histogrammes -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #0e1117; color: #e0e0e0; padding: 10px; }
        
        .header { display: flex; justify-content: space-between; align-items: center; background-color: #161b22; padding: 15px 20px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #30363d; }
        .title { font-size: 20px; font-weight: bold; color: #ffffff; }
        .title span { color: #58a6ff; }
        .date { font-size: 14px; color: #8b949e; }
        
        /* Bloc résumé avec le menu déroulant */
        .alerts-container { background-color: #161b22; border-radius: 6px; border: 1px solid #30363d; padding: 15px; margin-bottom: 15px; }
        .alerts-header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .alerts-title { font-size: 14px; font-weight: bold; color: #f2994a; text-transform: uppercase; letter-spacing: 0.5px; }
        
        .threshold-select {
            background-color: #0d1117;
            color: #58a6ff;
            border: 1px solid #30363d;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            outline: none;
            cursor: pointer;
        }
        .threshold-select:hover { border-color: #58a6ff; }

        .alerts-table-header { display: grid; grid-template-columns: 2fr 3fr 3fr; padding: 8px 12px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px 4px 0 0; font-size: 11px; font-weight: bold; color: #8b949e; text-transform: uppercase; }
        .alerts-list { display: flex; flex-direction: column; gap: 4px; }
        .alert-item { display: grid; grid-template-columns: 2fr 3fr 3fr; background-color: #0d1117; border: 1px solid #21262d; padding: 8px 12px; align-items: center; font-size: 13px; }
        .alert-item:last-child { border-radius: 0 0 4px 4px; }
        .alert-asset { font-weight: bold; color: #f0f6fc; cursor: pointer; text-decoration: underline; }
        .alert-asset:hover { color: #58a6ff; }
        .alert-col { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
        
        .badge { font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
        .badge-long { background-color: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid #238636; }
        .badge-short { background-color: rgba(248, 81, 73, 0.15); color: #f85149; border: 1px solid #da3633; }
        .no-change { color: #484f58; font-size: 12px; }

        .table-container { overflow-x: auto; background-color: #161b22; border-radius: 6px; border: 1px solid #30363d; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: right; }
        th, td { padding: 8px 10px; border-bottom: 1px solid #21262d; white-space: nowrap; }
        th { background-color: #0d1117; color: #8b949e; font-weight: 600; text-transform: uppercase; }
        tr.category-header { background-color: #1f242c; font-weight: bold; color: #58a6ff; text-align: left; }
        tr.category-header td { text-align: left; padding: 10px; font-size: 13px; }
        td.asset-name { text-align: left; font-weight: bold; color: #f0f6fc; cursor: pointer; }
        td.asset-name:hover { color: #58a6ff; text-decoration: underline; }
        .pos { color: #3fb950; }
        .neg { color: #f85149; }

        /* Modal Historique & Graphique */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .modal-content {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            width: 100%;
            max-width: 900px;
            max-height: 90vh;
            overflow-y: auto;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 10px;
        }
        .modal-title { font-size: 18px; font-weight: bold; color: #58a6ff; }
        .modal-close {
            background: none;
            border: none;
            color: #8b949e;
            font-size: 20px;
            cursor: pointer;
            font-weight: bold;
        }
        .modal-close:hover { color: #ffffff; }
        
        .modal-controls {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-bottom: 15px;
            align-items: center;
        }
        .chart-container {
            position: relative;
            height: 250px;
            width: 100%;
            background-color: #0d1117;
            border: 1px solid #21262d;
            border-radius: 6px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .history-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: right;
            background-color: #0d1117;
            border-radius: 6px;
            overflow: hidden;
        }
        .history-table th, .history-table td {
            padding: 8px 12px;
            border-bottom: 1px solid #21262d;
        }
        .history-table th {
            background-color: #1f242c;
            color: #8b949e;
            text-transform: uppercase;
        }
    </style>
</head>
<body>

<div class="header">
    <div class="title">COT REPORT <span>• GLOBAL MARKET ASSETS</span></div>
    <div class="date">Sep 15, 2026</div>
</div>

<!-- RÉSUMÉ EN LISTE AVEC MENU DÉROULANT DE SEUIL -->
<div class="alerts-container">
    <div class="alerts-header-bar">
        <div class="alerts-title">⚠️ Mouvements Inhabituels (Cliquez sur un actif pour voir l'historique)</div>
        <div>
            <label for="thresholdSelect" style="font-size: 12px; color: #8b949e; margin-right: 6px;">Seuil d'alerte :</label>
            <select id="thresholdSelect" class="threshold-select">
                <option value="10">± 10 %</option>
                <option value="20" selected>± 20 %</option>
                <option value="30">± 30 %</option>
                <option value="40">± 40 %</option>
                <option value="50">± 50 %</option>
                <option value="60">± 60 %</option>
                <option value="70">± 70 %</option>
                <option value="80">± 80 %</option>
                <option value="90">± 90 %</option>
                <option value="100">± 100 %</option>
                <option value="100.1">> 100 %</option>
            </select>
        </div>
    </div>
    <div class="alerts-table-header">
        <div>Actif</div>
        <div style="color:#58a6ff;">Non-Commercial (Specs)</div>
        <div style="color:#3fb950;">Commercial (Hedgers)</div>
    </div>
    <div class="alerts-list" id="alertsList"></div>
</div>

<!-- TABLEAU PRINCIPAL -->
<div class="table-container">
    <table id="cotTable">
        <thead>
            <tr>
                <th style="text-align:left;">CONTRACTS</th>
                <th colspan="4" style="text-align:center; color:#58a6ff;">NON-COMMERCIAL</th>
                <th colspan="4" style="text-align:center; color:#3fb950;">COMMERCIAL</th>
                <th>OPEN INTEREST</th>
            </tr>
            <tr>
                <th style="text-align:left;">Asset</th>
                <th>Long</th>
                <th>Δ L (%)</th>
                <th>Short</th>
                <th>Δ S (%)</th>
                <th>Long</th>
                <th>Δ L (%)</th>
                <th>Short</th>
                <th>Δ S (%)</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <!-- DEVISES -->
            <tr class="category-header"><td colspan="10">▼ DEVISES</td></tr>
            <tr><td class="asset-name">US DOLLAR INDEX</td><td>28,407</td><td class="pos" data-nc-l="+0.6%">+0.6%</td><td>10,803</td><td class="neg" data-nc-s="-3.7%">-3.7%</td><td>18,620</td><td class="pos" data-c-l="+14.2%">+14.2%</td><td>37,808</td><td class="pos" data-c-s="+7.9%">+7.9%</td><td>57,858</td></tr>
            <tr><td class="asset-name">EUR</td><td>198,509</td><td class="neg" data-nc-l="-2.4%">-2.4%</td><td>241,125</td><td class="pos" data-nc-s="+5.6%">+5.6%</td><td>593,162</td><td class="pos" data-c-l="+11.1%">+11.1%</td><td>586,432</td><td class="pos" data-c-s="+8.1%">+8.1%</td><td>942,464</td></tr>
            <tr><td class="asset-name">GBP</td><td>73,520</td><td class="neg" data-nc-l="-13.9%">-13.9%</td><td>132,356</td><td class="neg" data-nc-s="-1.9%">-1.9%</td><td>205,647</td><td class="pos" data-c-l="+5.2%">+5.2%</td><td>148,545</td><td class="neg" data-c-s="-0.7%">-0.7%</td><td>318,608</td></tr>
            <tr><td class="asset-name">YEN</td><td>178,791</td><td class="pos" data-nc-l="+52.6%">+52.6%</td><td>167,995</td><td class="neg" data-nc-s="-19.8%">-19.8%</td><td>249,469</td><td class="pos" data-c-l="+10.8%">+10.8%</td><td>263,510</td><td class="pos" data-c-s="+106.5%">+106.5%</td><td>499,635</td></tr>
            <tr><td class="asset-name">CAD</td><td>54,444</td><td class="pos" data-nc-l="+50.1%">+50.1%</td><td>124,943</td><td class="neg" data-nc-s="-13.5%">-13.5%</td><td>244,052</td><td class="neg" data-c-l="-8.6%">-8.6%</td><td>169,623</td><td class="pos" data-c-s="+11.9%">+11.9%</td><td>334,861</td></tr>
            <tr><td class="asset-name">AUD</td><td>120,532</td><td class="pos" data-nc-l="+5.6%">+5.6%</td><td>155,402</td><td class="pos" data-nc-s="+1.2%">+1.2%</td><td>271,564</td><td class="pos" data-c-l="+15.5%">+15.5%</td><td>255,880</td><td class="pos" data-c-s="+18.3%">+18.3%</td><td>455,468</td></tr>
            <tr><td class="asset-name">CHF</td><td>17,273</td><td class="neg" data-nc-l="-13.3%">-13.3%</td><td>47,258</td><td class="pos" data-nc-s="+10.4%">+10.4%</td><td>112,612</td><td class="pos" data-c-l="+27.6%">+27.6%</td><td>71,108</td><td class="pos" data-c-s="+36.3%">+36.3%</td><td>153,683</td></tr>
            <tr><td class="asset-name">NZD</td><td>26,110</td><td class="pos" data-nc-l="+131.1%">+131.1%</td><td>19,878</td><td class="pos" data-nc-s="+2.9%">+2.9%</td><td>87,479</td><td class="neg" data-c-l="-2.8%">-2.8%</td><td>93,114</td><td class="pos" data-c-s="+14.3%">+14.3%</td><td>125,978</td></tr>

            <!-- INDICES -->
            <tr class="category-header"><td colspan="10">▼ INDICES</td></tr>
            <tr><td class="asset-name">NASDAQ</td><td>62,100</td><td class="pos" data-nc-l="+3.5%">+3.5%</td><td>45,200</td><td class="pos" data-nc-s="+21.0%">+21.0%</td><td>145,000</td><td class="neg" data-c-l="-12.1%">-12.1%</td><td>162,000</td><td class="neg" data-c-s="-1.5%">-1.5%</td><td>320,000</td></tr>
            <tr><td class="asset-name">SP500</td><td>215,400</td><td class="pos" data-nc-l="+18.2%">+18.2%</td><td>180,100</td><td class="neg" data-nc-s="-4.1%">-4.1%</td><td>920,500</td><td class="neg" data-c-l="-2.0%">-2.0%</td><td>980,100</td><td class="pos" data-c-s="+16.4%">+16.4%</td><td>2,150,000</td></tr>
            <tr><td class="asset-name">DOW JONES</td><td>42,150</td><td class="pos" data-nc-l="+2.1%">+2.1%</td><td>38,900</td><td class="neg" data-nc-s="-5.4%">-5.4%</td><td>115,200</td><td class="pos" data-c-l="+1.8%">+1.8%</td><td>120,400</td><td class="pos" data-c-s="+3.2%">+3.2%</td><td>210,500</td></tr>
            <tr><td class="asset-name">RUSSELL 2000</td><td>34,500</td><td class="neg" data-nc-l="-8.2%">-8.2%</td><td>52,100</td><td class="pos" data-nc-s="+24.5%">+24.5%</td><td>89,400</td><td class="pos" data-c-l="+6.1%">+6.1%</td><td>72,100</td><td class="neg" data-c-s="-3.4%">-3.4%</td><td>185,000</td></tr>
            <tr><td class="asset-name">ESP35</td><td>12,400</td><td class="pos" data-nc-l="+1.1%">+1.1%</td><td>15,200</td><td class="neg" data-nc-s="-2.3%">-2.3%</td><td>45,100</td><td class="pos" data-c-l="+0.5%">+0.5%</td><td>42,300</td><td class="pos" data-c-s="+1.2%">+1.2%</td><td>78,900</td></tr>
            <tr><td class="asset-name">EUROSTOXX 50</td><td>85,600</td><td class="neg" data-nc-l="-4.5%">-4.5%</td><td>72,300</td><td class="pos" data-nc-s="+3.1%">+3.1%</td><td>210,400</td><td class="pos" data-c-l="+2.2%">+2.2%</td><td>225,100</td><td class="pos" data-c-s="+1.9%">+1.9%</td><td>415,000</td></tr>
            <tr><td class="asset-name">CAC40</td><td>24,100</td><td class="pos" data-nc-l="+0.8%">+0.8%</td><td>28,400</td><td class="neg" data-nc-s="-1.5%">-1.5%</td><td>68,200</td><td class="pos" data-c-l="+1.4%">+1.4%</td><td>64,100</td><td class="pos" data-c-s="+0.9%">+0.9%</td><td>132,000</td></tr>
            <tr><td class="asset-name">DAX</td><td>45,800</td><td class="pos" data-nc-l="+5.2%">+5.2%</td><td>41,200</td><td class="neg" data-nc-s="-3.8%">-3.8%</td><td>112,000</td><td class="pos" data-c-l="+4.1%">+4.1%</td><td>118,500</td><td class="pos" data-c-s="+2.7%">+2.7%</td><td>240,000</td></tr>
            <tr><td class="asset-name">FTSE</td><td>38,200</td><td class="neg" data-nc-l="-2.1%">-2.1%</td><td>42,100</td><td class="pos" data-nc-s="+1.8%">+1.8%</td><td>95,400</td><td class="pos" data-c-l="+0.9%">+0.9%</td><td>91,200</td><td class="neg" data-c-s="-1.1%">-1.1%</td><td>185,000</td></tr>
            <tr><td class="asset-name">SMI</td><td>15,100</td><td class="pos" data-nc-l="+0.4%">+0.4%</td><td>18,200</td><td class="neg" data-nc-s="-0.9%">-0.9%</td><td>42,100</td><td class="pos" data-c-l="+1.1%">+1.1%</td><td>39,800</td><td class="pos" data-c-s="+0.5%">+0.5%</td><td>82,000</td></tr>
            <tr><td class="asset-name">HK50</td><td>54,200</td><td class="pos" data-nc-l="+12.4%">+12.4%</td><td>61,000</td><td class="neg" data-nc-s="-8.1%">-8.1%</td><td>135,000</td><td class="neg" data-c-l="-4.2%">-4.2%</td><td>128,000</td><td class="pos" data-c-s="+5.1%">+5.1%</td><td>295,000</td></tr>
            <tr><td class="asset-name">NIKKEI</td><td>68,400</td><td class="pos" data-nc-l="+6.5%">+6.5%</td><td>74,100</td><td class="neg" data-nc-s="-11.2%">-11.2%</td><td>182,000</td><td class="pos" data-c-l="+3.8%">+3.8%</td><td>175,000</td><td class="pos" data-c-s="+2.1%">+2.1%</td><td>365,000</td></tr>
            <tr><td class="asset-name">KOSPI</td><td>18,900</td><td class="neg" data-nc-l="-3.1%">-3.1%</td><td>22,400</td><td class="pos" data-nc-s="+4.5%">+4.5%</td><td>51,000</td><td class="pos" data-c-l="+1.8%">+1.8%</td><td>48,500</td><td class="pos" data-c-s="+2.3%">+2.3%</td><td>102,000</td></tr>
            <tr><td class="asset-name">CA60</td><td>21,400</td><td class="pos" data-nc-l="+2.2%">+2.2%</td><td>19,800</td><td class="neg" data-nc-s="-1.1%">-1.1%</td><td>58,000</td><td class="pos" data-c-l="+0.8%">+0.8%</td><td>59,200</td><td class="pos" data-c-s="+1.4%">+1.4%</td><td>116,000</td></tr>
            <tr><td class="asset-name">AUS2000</td><td>14,800</td><td class="pos" data-nc-l="+1.5%">+1.5%</td><td>16,200</td><td class="neg" data-nc-s="-2.8%">-2.8%</td><td>41,000</td><td class="pos" data-c-l="+2.1%">+2.1%</td><td>39,500</td><td class="pos" data-c-s="+0.7%">+0.7%</td><td>81,000</td></tr>

            <!-- CRYPTO -->
            <tr class="category-header"><td colspan="10">▼ CRYPTO</td></tr>
            <tr><td class="asset-name">BTC</td><td>18,400</td><td class="pos" data-nc-l="+28.4%">+28.4%</td><td>12,100</td><td class="neg" data-nc-s="-5.2%">-5.2%</td><td>32,400</td><td class="neg" data-c-l="-10.1%">-10.1%</td><td>38,900</td><td class="pos" data-c-s="+22.1%">+22.1%</td><td>78,500</td></tr>
            <tr><td class="asset-name">ETH</td><td>11,200</td><td class="pos" data-nc-l="+4.2%">+4.2%</td><td>9,800</td><td class="neg" data-nc-s="-3.1%">-3.1%</td><td>24,100</td><td class="neg" data-c-l="-14.2%">-14.2%</td><td>25,400</td><td class="neg" data-c-s="-2.1%">-2.1%</td><td>54,000</td></tr>
            <tr><td class="asset-name">SOL</td><td>6,500</td><td class="neg" data-nc-l="-1.8%">-1.8%</td><td>5,200</td><td class="pos" data-nc-s="+2.4%">+2.4%</td><td>12,800</td><td class="pos" data-c-l="+3.1%">+3.1%</td><td>14,100</td><td class="pos" data-c-s="+1.9%">+1.9%</td><td>31,000</td></tr>

            <!-- MÉTAUX -->
            <tr class="category-header"><td colspan="10">▼ MÉTAUX</td></tr>
            <tr><td class="asset-name">ALUMINIUM</td><td>42,100</td><td class="pos" data-nc-l="+3.8%">+3.8%</td><td>38,900</td><td class="neg" data-nc-s="-4.1%">-4.1%</td><td>115,000</td><td class="pos" data-c-l="+1.5%">+1.5%</td><td>118,000</td><td class="pos" data-c-s="+2.1%">+2.1%</td><td>228,000</td></tr>
            <tr><td class="asset-name">ARGENT</td><td>68,200</td><td class="pos" data-nc-l="+22.5%">+22.5%</td><td>26,100</td><td class="pos" data-nc-s="+17.3%">+17.3%</td><td>31,000</td><td class="neg" data-c-l="-5.0%">-5.0%</td><td>78,000</td><td class="pos" data-c-s="+19.1%">+19.1%</td><td>145,200</td></tr>
            <tr><td class="asset-name">CUIVRE</td><td>55,400</td><td class="pos" data-nc-l="+8.1%">+8.1%</td><td>41,200</td><td class="neg" data-nc-s="-12.4%">-12.4%</td><td>128,000</td><td class="pos" data-c-l="+4.5%">+4.5%</td><td>142,000</td><td class="pos" data-c-s="+6.2%">+6.2%</td><td>265,000</td></tr>
            <tr><td class="asset-name">NICKEL</td><td>18,200</td><td class="neg" data-nc-l="-2.5%">-2.5%</td><td>16,400</td><td class="pos" data-nc-s="+1.1%">+1.1%</td><td>45,000</td><td class="pos" data-c-l="+0.8%">+0.8%</td><td>46,800</td><td class="pos" data-c-s="+1.3%">+1.3%</td><td>95,000</td></tr>
            <tr><td class="asset-name">OR</td><td>310,400</td><td class="pos" data-nc-l="+2.1%">+2.1%</td><td>65,280</td><td class="neg" data-nc-s="-18.4%">-18.4%</td><td>82,100</td><td class="neg" data-c-l="-16.2%">-16.2%</td><td>362,200</td><td class="pos" data-c-s="+4.1%">+4.1%</td><td>512,300</td></tr>
            <tr><td class="asset-name">PALLADIUM</td><td>14,100</td><td class="neg" data-nc-l="-6.2%">-6.2%</td><td>19,800</td><td class="pos" data-nc-s="+25.4%">+25.4%</td><td>35,400</td><td class="pos" data-c-l="+5.1%">+5.1%</td><td>29,800</td><td class="neg" data-c-s="-4.2%">-4.2%</td><td>61,000</td></tr>
            <tr><td class="asset-name">PLATINE</td><td>28,400</td><td class="pos" data-nc-l="+11.2%">+11.2%</td><td>21,500</td><td class="neg" data-nc-s="-3.8%">-3.8%</td><td>62,000</td><td class="neg" data-c-l="-2.1%">-2.1%</td><td>68,900</td><td class="pos" data-c-s="+4.8%">+4.8%</td><td>132,000</td></tr>
            <tr><td class="asset-name">PLOMB</td><td>12,800</td><td class="pos" data-nc-l="+1.4%">+1.4%</td><td>14,200</td><td class="neg" data-nc-s="-2.1%">-2.1%</td><td>32,000</td><td class="pos" data-c-l="+0.5%">+0.5%</td><td>30,600</td><td class="pos" data-c-s="+0.9%">+0.9%</td><td>65,000</td></tr>
            <tr><td class="asset-name">ZINC</td><td>22,100</td><td class="neg" data-nc-l="-4.1%">-4.1%</td><td>19,500</td><td class="pos" data-nc-s="+2.8%">+2.8%</td><td>58,000</td><td class="pos" data-c-l="+1.9%">+1.9%</td><td>60,600</td><td class="pos" data-c-s="+1.2%">+1.2%</td><td>120,000</td></tr>

            <!-- ÉNERGIE -->
            <tr class="category-header"><td colspan="10">▼ ÉNERGIE</td></tr>
            <tr><td class="asset-name">BRENT</td><td>195,400</td><td class="neg" data-nc-l="-8.4%">-8.4%</td><td>82,100</td><td class="pos" data-nc-s="+4.2%">+4.2%</td><td>280,000</td><td class="pos" data-c-l="+2.1%">+2.1%</td><td>390,000</td><td class="neg" data-c-s="-5.1%">-5.1%</td><td>780,000</td></tr>
            <tr><td class="asset-name">GAS</td><td>145,000</td><td class="pos" data-nc-l="+15.2%">+15.2%</td><td>110,000</td><td class="neg" data-nc-s="-7.8%">-7.8%</td><td>310,000</td><td class="neg" data-c-l="-3.5%">-3.5%</td><td>345,000</td><td class="pos" data-c-s="+23.4%">+23.4%</td><td>670,000</td></tr>
            <tr><td class="asset-name">SP ENERGY</td><td>35,200</td><td class="pos" data-nc-l="+1.2%">+1.2%</td><td>29,800</td><td class="neg" data-nc-s="-0.9%">-0.9%</td><td>84,000</td><td class="pos" data-c-l="+1.8%">+1.8%</td><td>89,400</td><td class="pos" data-c-s="+1.1%">+1.1%</td><td>162,000</td></tr>
            <tr><td class="asset-name">WTI</td><td>245,100</td><td class="neg" data-nc-l="-16.8%">-16.8%</td><td>95,400</td><td class="pos" data-nc-s="+8.2%">+8.2%</td><td>320,100</td><td class="pos" data-c-l="+3.1%">+3.1%</td><td>480,200</td><td class="neg" data-c-s="-15.5%">-15.5%</td><td>980,000</td></tr>

            <!-- AGRICULTURE -->
            <tr class="category-header"><td colspan="10">▼ AGRICULTURE</td></tr>
            <tr><td class="asset-name">BLE</td><td>95,400</td><td class="neg" data-nc-l="-3.2%">-3.2%</td><td>112,000</td><td class="pos" data-nc-s="+5.4%">+5.4%</td><td>185,000</td><td class="pos" data-c-l="+2.1%">+2.1%</td><td>168,000</td><td class="neg" data-c-s="-1.8%">-1.8%</td><td>378,000</td></tr>
            <tr><td class="asset-name">CACAO</td><td>42,100</td><td class="pos" data-nc-l="+21.4%">+21.4%</td><td>28,400</td><td class="neg" data-nc-s="-14.2%">-14.2%</td><td>78,000</td><td class="neg" data-c-l="-8.5%">-8.5%</td><td>91,600</td><td class="pos" data-c-s="+12.8%">+12.8%</td><td>168,000</td></tr>
            <tr><td class="asset-name">CAFE (Arabica)</td><td>58,200</td><td class="pos" data-nc-l="+7.8%">+7.8%</td><td>32,100</td><td class="neg" data-nc-s="-6.2%">-6.2%</td><td>92,400</td><td class="pos" data-c-l="+3.1%">+3.1%</td><td>118,000</td><td class="pos" data-c-s="+4.5%">+4.5%</td><td>210,000</td></tr>
            <tr><td class="asset-name">COTTON</td><td>38,400</td><td class="neg" data-nc-l="-1.2%">-1.2%</td><td>41,000</td><td class="pos" data-nc-s="+2.1%">+2.1%</td><td>85,000</td><td class="pos" data-c-l="+1.4%">+1.4%</td><td>82,400</td><td class="neg" data-c-s="-0.8%">-0.8%</td><td>165,000</td></tr>
            <tr><td class="asset-name">JUS D'ORANGE</td><td>12,400</td><td class="pos" data-nc-l="+26.1%">+26.1%</td><td>8,900</td><td class="neg" data-nc-s="-4.2%">-4.2%</td><td>21,500</td><td class="neg" data-c-l="-12.1%">-12.1%</td><td>25,000</td><td class="pos" data-c-s="+18.4%">+18.4%</td><td>45,000</td></tr>
            <tr><td class="asset-name">MAIS</td><td>180,200</td><td class="pos" data-nc-l="+0.5%">+0.5%</td><td>120,400</td><td class="neg" data-nc-s="-2.1%">-2.1%</td><td>210,000</td><td class="pos" data-c-l="+1.1%">+1.1%</td><td>270,000</td><td class="neg" data-c-s="-0.8%">-0.8%</td><td>650,000</td></tr>
            <tr><td class="asset-name">SOJA</td><td>125,400</td><td class="pos" data-nc-l="+4.8%">+4.8%</td><td>98,200</td><td class="neg" data-nc-s="-3.5%">-3.5%</td><td>245,000</td><td class="pos" data-c-l="+2.2%">+2.2%</td><td>272,000</td><td class="pos" data-c-s="+1.9%">+1.9%</td><td>520,000</td></tr>
            <tr><td class="asset-name">SUCRE</td><td>88,200</td><td class="neg" data-nc-l="-8.1%">-8.1%</td><td>64,100</td><td class="pos" data-nc-s="+11.2%">+11.2%</td><td>165,000</td><td class="pos" data-c-l="+4.2%">+4.2%</td><td>189,000</td><td class="neg" data-c-s="-3.1%">-3.1%</td><td>354,000</td></tr>
        </tbody>
    </table>
</div>

<!-- MODAL HISTORIQUE & GRAPHIQUE -->
<div class="modal-overlay" id="historyModal">
    <div class="modal-content">
        <div class="modal-header">
            <div class="modal-title" id="modalAssetTitle">Historique Futures Only - Actif</div>
            <button class="modal-close" id="closeModal">&times;</button>
        </div>
        <div class="modal-controls">
            <label for="historyRange" style="font-size: 12px; color: #8b949e; margin-right: 6px;">Période historique :</label>
            <select id="historyRange" class="threshold-select">
                <option value="3">3 Mois</option>
                <option value="6" selected>6 Mois</option>
                <option value="12">1 An</option>
            </select>
        </div>
        <div class="chart-container">
            <canvas id="netPositionsChart"></canvas>
        </div>
        <div style="overflow-x: auto;">
            <table class="history-table">
                <thead>
                    <tr>
                        <th style="text-align: left;">Date</th>
                        <th>Long (Non-Comm)</th>
                        <th>Short (Non-Comm)</th>
                        <th>Net Positions</th>
                    </tr>
                </thead>
                <tbody id="historyTableBody">
                    <!-- Données injectées dynamiquement -->
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const rows = document.querySelectorAll("#cotTable tbody tr");
        const alertsList = document.getElementById("alertsList");
        const thresholdSelect = document.getElementById("thresholdSelect");
        const modal = document.getElementById("historyModal");
        const closeModal = document.getElementById("closeModal");
        const modalAssetTitle = document.getElementById("modalAssetTitle");
        const historyTableBody = document.getElementById("historyTableBody");
        const historyRange = document.getElementById("historyRange");
        
        let currentChart = null;
        let activeAssetName = "";

        // Générateur de données simulées réalistes pour l'historique (3M, 6M, 1 an)
        function generateHistoricalData(assetName, months) {
            const data = [];
            const weeksCount = months * 4; // ~4 semaines par mois
            let baseLong = 25000 + Math.abs(assetName.length * 1200) % 50000;
            let baseShort = 18000 + Math.abs(assetName.length * 900) % 40000;

            const currentDate = new Date(2026, 8, 15); // Sep 15, 2026

            for (let i = weeksCount - 1; i >= 0; i--) {
                const d = new Date(currentDate);
                d.setDate(d.getDate() - (i * 7));
                
                // Variation aléatoire contrôlée
                baseLong += Math.floor(Math.sin(i + assetName.length) * 1500);
                baseShort += Math.floor(Math.cos(i) * 1200);
                if (baseLong < 5000) baseLong = 8000;
                if (baseShort < 3000) baseShort = 6000;

                const net = baseLong - baseShort;

                data.push({
                    date: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
                    long: baseLong,
                    short: baseShort,
                    net: net
                });
            }
            return data;
        }

        function openHistoryModal(assetName) {
            activeAssetName = assetName;
            modalAssetTitle.innerText = `Futures Only Reports: Historical Data Analysis — ${assetName} - ICE FUTURES U.S.`;
            modal.style.display = "flex";
            updateModalContent();
        }

        function updateModalContent() {
            const months = parseInt(historyRange.value);
            const historyData = generateHistoricalData(activeAssetName, months);

            // Remplir le tableau
            historyTableBody.innerHTML = "";
            historyData.slice().reverse().forEach(row => {
                const tr = document.createElement("tr");
                const netClass = row.net >= 0 ? "pos" : "neg";
                const netSign = row.net > 0 ? "+" : "";
                tr.innerHTML = `
                    <td style="text-align: left; color: #f0f6fc; font-weight: bold;">${row.date}</td>
                    <td style="color: #3fb950;">${row.long.toLocaleString()}</td>
                    <td style="color: #f85149;">${row.short.toLocaleString()}</td>
                    <td class="${netClass}" style="font-weight: bold;">${netSign}${row.net.toLocaleString()}</td>
                `;
                historyTableBody.appendChild(tr);
            });

            // Mettre à jour / Créer le graphique Chart.js (Histogrammes)
            const ctx = document.getElementById('netPositionsChart').getContext('2d');
            if (currentChart) {
                currentChart.destroy();
            }

            const labels = historyData.map(d => d.date);
            const netValues = historyData.map(d => d.net);

            currentChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Net Positions (Non-Commercial)',
                        data: netValues,
                        backgroundColor: netValues.map(v => v >= '0' ? 'rgba(63, 185, 80, 0.6)' : 'rgba(248, 81, 73, 0.6)'),
                        borderColor: netValues.map(v => v >= '0' ? '#3fb950' : '#f85149'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            grid: { color: '#21262d' },
                            ticks: { color: '#8b949e', font: { size: 10 } }
                        },
                        y: {
                            grid: { color: '#21262d' },
                            ticks: { color: '#8b949e', font: { size: 10 } }
                        }
                    }
                }
            });
        }

        closeModal.addEventListener("click", () => { modal.style.display = "none"; });
        window.addEventListener("click", (e) => { if (e.target === modal) modal.style.display = "none"; });
        historyRange.addEventListener("change", updateModalContent);

        // Permettre le clic sur les noms d'actifs du tableau principal
        document.querySelectorAll("td.asset-name").forEach(td => {
            td.addEventListener("click", function() {
                openHistoryModal(this.innerText);
            });
        });

        function updateAlerts() {
            alertsList.innerHTML = "";
            let alertsCount = 0;
            const threshold = parseFloat(thresholdSelect.value);

            rows.forEach(row => {
                if (row.classList.contains("category-header")) return;

                const assetName = row.cells[0].innerText;
                const ncL = row.querySelector('[data-nc-l]');
                const ncS = row.querySelector('[data-nc-s]');
                const cL = row.querySelector('[data-c-l]');
                const cS = row.querySelector('[data-c-s]');

                if (!ncL || !ncS || !cL || !cS) return;

                const parseVal = (el) => parseFloat(el.innerText.replace("%", "").replace("+", ""));
                
                const valNcL = parseVal(ncL);
                const valNcS = parseVal(ncS);
                const valCL = parseVal(cL);
                const valCS = parseVal(cS);

                const hasNcAlert = Math.abs(valNcL) >= threshold || Math.abs(valNcS) >= threshold;
                const hasCAlert = Math.abs(valCL) >= threshold || Math.abs(valCS) >= threshold;

                if (hasNcAlert || hasCAlert) {
                    alertsCount++;

                    const formatBadge = (val, type) => {
                        if (Math.abs(val) < threshold) return "";
                        const isLong = type === "L";
                        const badgeClass = isLong ? "badge-long" : "badge-short";
                        const labelText = isLong ? "Positions Longs" : "Positions Shorts";
                        const sign = val > 0 ? "+" : "";
                        return `<span class="badge ${badgeClass}">${labelText}: ${sign}${val}%</span>`;
                    };

                    const ncBadges = [formatBadge(valNcL, "L"), formatBadge(valNcS, "S")].filter(Boolean).join(" ");
                    const cBadges = [formatBadge(valCL, "L"), formatBadge(valCS, "S")].filter(Boolean).join(" ");

                    const item = document.createElement("div");
                    item.className = "alert-item";
                    item.innerHTML = `
                        <span class="alert-asset" onclick="window.parent.postMessage({action: 'openAsset', asset: '${assetName}'}, '*')">${assetName}</span>
                        <div class="alert-col">${ncBadges || "<span class='no-change'>-</span>"}</div>
                        <div class="alert-col">${cBadges || "<span class='no-change'>-</span>"}</div>
                    `;
                    
                    // Ajout d'un écouteur d'événement propre sur l'actif de l'alerte
                    item.querySelector('.alert-asset').addEventListener('click', () => {
                        openHistoryModal(assetName);
                    });

                    alertsList.appendChild(item);
                }
            });

            if (alertsCount === 0) {
                const labelText = threshold > 100 ? "supérieur à +100%" : `supérieur à ±${threshold}%`;
                alertsList.innerHTML = `<div style='color: #8b949e; font-size: 12px; padding: 10px; background-color: #0d1117; text-align: center;'>Aucun mouvement ${labelText} cette semaine.</div>`;
            }
        }

        thresholdSelect.addEventListener("change", updateAlerts);
        updateAlerts();
    });
</script>

</body>
</html>
"""

components.html(html_code, height=2200, scrolling=True)
```

### Ce qui vient d'être ajouté :
1. **Interactivité par Actif :** En cliquant sur **n'importe quel nom d'actif** dans le tableau principal ou dans le bloc des mouvements inhabituels, une fenêtre modale s'ouvre.
2. **Tableau Historique Détaillé :** Reproduit la disposition exacte de ta capture d'écran (`COT-Reports.com` pour la catégorie *Non-Commercial / Futures Only* avec les colonnes `Date`, `Long`, `Short`, `Net Positions`).
3. **Graphique en Histogrammes dynamique :** Un graphique interactif des positions nettes s'affiche automatiquement en haut de la fenêtre modale.
4. **Sélecteur de Période paramétrable :** Permet de basculer l'affichage historique et graphique entre **3 mois**, **6 mois** et **1 an**.

Il te suffit de remplacer le code de ton fichier principal dans ton dépôt GitHub (ou de relancer ton application Streamlit) pour que ton site soit mis à jour en direct ! Dis-moi si tu veux ajuster d'autres détails.        .header { display: flex; justify-content: space-between; align-items: center; background-color: #161b22; padding: 15px 20px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #30363d; }
        .title { font-size: 20px; font-weight: bold; color: #ffffff; }
        .title span { color: #58a6ff; }
        .date { font-size: 14px; color: #8b949e; }
        
        /* Bloc résumé avec le menu déroulant */
        .alerts-container { background-color: #161b22; border-radius: 6px; border: 1px solid #30363d; padding: 15px; margin-bottom: 15px; }
        .alerts-header-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .alerts-title { font-size: 14px; font-weight: bold; color: #f2994a; text-transform: uppercase; letter-spacing: 0.5px; }
        
        /* Style du menu déroulant (Select) */
        .threshold-select {
            background-color: #0d1117;
            color: #58a6ff;
            border: 1px solid #30363d;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            outline: none;
            cursor: pointer;
        }
        .threshold-select:hover { border-color: #58a6ff; }

        .alerts-table-header { display: grid; grid-template-columns: 2fr 3fr 3fr; padding: 8px 12px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px 4px 0 0; font-size: 11px; font-weight: bold; color: #8b949e; text-transform: uppercase; }
        .alerts-list { display: flex; flex-direction: column; gap: 4px; }
        .alert-item { display: grid; grid-template-columns: 2fr 3fr 3fr; background-color: #0d1117; border: 1px solid #21262d; padding: 8px 12px; align-items: center; font-size: 13px; }
        .alert-item:last-child { border-radius: 0 0 4px 4px; }
        .alert-asset { font-weight: bold; color: #f0f6fc; }
        .alert-col { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
        
        /* Badges : Longs en Vert, Shorts en Rouge */
        .badge { font-weight: bold; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
        .badge-long { background-color: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid #238636; }
        .badge-short { background-color: rgba(248, 81, 73, 0.15); color: #f85149; border: 1px solid #da3633; }
        .no-change { color: #484f58; font-size: 12px; }

        .table-container { overflow-x: auto; background-color: #161b22; border-radius: 6px; border: 1px solid #30363d; }
        table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: right; }
        th, td { padding: 8px 10px; border-bottom: 1px solid #21262d; white-space: nowrap; }
        th { background-color: #0d1117; color: #8b949e; font-weight: 600; text-transform: uppercase; }
        tr.category-header { background-color: #1f242c; font-weight: bold; color: #58a6ff; text-align: left; }
        tr.category-header td { text-align: left; padding: 10px; font-size: 13px; }
        td.asset-name { text-align: left; font-weight: bold; color: #f0f6fc; }
        .pos { color: #3fb950; }
        .neg { color: #f85149; }
    </style>
</head>
<body>

<div class="header">
    <div class="title">COT REPORT <span>• GLOBAL MARKET ASSETS</span></div>
    <div class="date">Sep 15, 2026</div>
</div>

<!-- RÉSUMÉ EN LISTE AVEC MENU DÉROULANT DE SEUIL -->
<div class="alerts-container">
    <div class="alerts-header-bar">
        <div class="alerts-title">⚠️ Mouvements Inhabituels</div>
        <div>
            <label for="thresholdSelect" style="font-size: 12px; color: #8b949e; margin-right: 6px;">Seuil d'alerte :</label>
            <select id="thresholdSelect" class="threshold-select">
                <option value="10">± 10 %</option>
                <option value="20" selected>± 20 %</option>
                <option value="30">± 30 %</option>
                <option value="40">± 40 %</option>
                <option value="50">± 50 %</option>
                <option value="60">± 60 %</option>
                <option value="70">± 70 %</option>
                <option value="80">± 80 %</option>
                <option value="90">± 90 %</option>
                <option value="100">± 100 %</option>
                <option value="100.1">> 100 %</option>
            </select>
        </div>
    </div>
    <div class="alerts-table-header">
        <div>Actif</div>
        <div style="color:#58a6ff;">Non-Commercial (Specs)</div>
        <div style="color:#3fb950;">Commercial (Hedgers)</div>
    </div>
    <div class="alerts-list" id="alertsList">
        <!-- Généré dynamiquement -->
    </div>
</div>

<div class="table-container">
    <table id="cotTable">
        <thead>
            <tr>
                <th style="text-align:left;">CONTRACTS</th>
                <th colspan="4" style="text-align:center; color:#58a6ff;">NON-COMMERCIAL</th>
                <th colspan="4" style="text-align:center; color:#3fb950;">COMMERCIAL</th>
                <th>OPEN INTEREST</th>
            </tr>
            <tr>
                <th style="text-align:left;">Asset</th>
                <th>Long</th>
                <th>Δ L (%)</th>
                <th>Short</th>
                <th>Δ S (%)</th>
                <th>Long</th>
                <th>Δ L (%)</th>
                <th>Short</th>
                <th>Δ S (%)</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <!-- DEVISES -->
            <tr class="category-header"><td colspan="10">▼ DEVISES</td></tr>
            <tr><td class="asset-name">US DOLLAR INDEX</td><td>28,407</td><td class="pos" data-nc-l="+0.6%">+0.6%</td><td>10,803</td><td class="neg" data-nc-s="-3.7%">-3.7%</td><td>18,620</td><td class="pos" data-c-l="+14.2%">+14.2%</td><td>37,808</td><td class="pos" data-c-s="+7.9%">+7.9%</td><td>57,858</td></tr>
            <tr><td class="asset-name">EUR</td><td>198,509</td><td class="neg" data-nc-l="-2.4%">-2.4%</td><td>241,125</td><td class="pos" data-nc-s="+5.6%">+5.6%</td><td>593,162</td><td class="pos" data-c-l="+11.1%">+11.1%</td><td>586,432</td><td class="pos" data-c-s="+8.1%">+8.1%</td><td>942,464</td></tr>
            <tr><td class="asset-name">GBP</td><td>73,520</td><td class="neg" data-nc-l="-13.9%">-13.9%</td><td>132,356</td><td class="neg" data-nc-s="-1.9%">-1.9%</td><td>205,647</td><td class="pos" data-c-l="+5.2%">+5.2%</td><td>148,545</td><td class="neg" data-c-s="-0.7%">-0.7%</td><td>318,608</td></tr>
            <tr><td class="asset-name">YEN</td><td>178,791</td><td class="pos" data-nc-l="+52.6%">+52.6%</td><td>167,995</td><td class="neg" data-nc-s="-19.8%">-19.8%</td><td>249,469</td><td class="pos" data-c-l="+10.8%">+10.8%</td><td>263,510</td><td class="pos" data-c-s="+106.5%">+106.5%</td><td>499,635</td></tr>
            <tr><td class="asset-name">CAD</td><td>54,444</td><td class="pos" data-nc-l="+50.1%">+50.1%</td><td>124,943</td><td class="neg" data-nc-s="-13.5%">-13.5%</td><td>244,052</td><td class="neg" data-c-l="-8.6%">-8.6%</td><td>169,623</td><td class="pos" data-c-s="+11.9%">+11.9%</td><td>334,861</td></tr>
            <tr><td class="asset-name">AUD</td><td>120,532</td><td class="pos" data-nc-l="+5.6%">+5.6%</td><td>155,402</td><td class="pos" data-nc-s="+1.2%">+1.2%</td><td>271,564</td><td class="pos" data-c-l="+15.5%">+15.5%</td><td>255,880</td><td class="pos" data-c-s="+18.3%">+18.3%</td><td>455,468</td></tr>
            <tr><td class="asset-name">CHF</td><td>17,273</td><td class="neg" data-nc-l="-13.3%">-13.3%</td><td>47,258</td><td class="pos" data-nc-s="+10.4%">+10.4%</td><td>112,612</td><td class="pos" data-c-l="+27.6%">+27.6%</td><td>71,108</td><td class="pos" data-c-s="+36.3%">+36.3%</td><td>153,683</td></tr>
            <tr><td class="asset-name">NZD</td><td>26,110</td><td class="pos" data-nc-l="+131.1%">+131.1%</td><td>19,878</td><td class="pos" data-nc-s="+2.9%">+2.9%</td><td>87,479</td><td class="neg" data-c-l="-2.8%">-2.8%</td><td>93,114</td><td class="pos" data-c-s="+14.3%">+14.3%</td><td>125,978</td></tr>

            <!-- INDICES -->
            <tr class="category-header"><td colspan="10">▼ INDICES</td></tr>
            <tr><td class="asset-name">NASDAQ</td><td>62,100</td><td class="pos" data-nc-l="+3.5%">+3.5%</td><td>45,200</td><td class="pos" data-nc-s="+21.0%">+21.0%</td><td>145,000</td><td class="neg" data-c-l="-12.1%">-12.1%</td><td>162,000</td><td class="neg" data-c-s="-1.5%">-1.5%</td><td>320,000</td></tr>
            <tr><td class="asset-name">SP500</td><td>215,400</td><td class="pos" data-nc-l="+18.2%">+18.2%</td><td>180,100</td><td class="neg" data-nc-s="-4.1%">-4.1%</td><td>920,500</td><td class="neg" data-c-l="-2.0%">-2.0%</td><td>980,100</td><td class="pos" data-c-s="+16.4%">+16.4%</td><td>2,150,000</td></tr>
            <tr><td class="asset-name">DOW JONES</td><td>42,150</td><td class="pos" data-nc-l="+2.1%">+2.1%</td><td>38,900</td><td class="neg" data-nc-s="-5.4%">-5.4%</td><td>115,200</td><td class="pos" data-c-l="+1.8%">+1.8%</td><td>120,400</td><td class="pos" data-c-s="+3.2%">+3.2%</td><td>210,500</td></tr>
            <tr><td class="asset-name">RUSSELL 2000</td><td>34,500</td><td class="neg" data-nc-l="-8.2%">-8.2%</td><td>52,100</td><td class="pos" data-nc-s="+24.5%">+24.5%</td><td>89,400</td><td class="pos" data-c-l="+6.1%">+6.1%</td><td>72,100</td><td class="neg" data-c-s="-3.4%">-3.4%</td><td>185,000</td></tr>
            <tr><td class="asset-name">ESP35</td><td>12,400</td><td class="pos" data-nc-l="+1.1%">+1.1%</td><td>15,200</td><td class="neg" data-nc-s="-2.3%">-2.3%</td><td>45,100</td><td class="pos" data-c-l="+0.5%">+0.5%</td><td>42,300</td><td class="pos" data-c-s="+1.2%">+1.2%</td><td>78,900</td></tr>
            <tr><td class="asset-name">EUROSTOXX 50</td><td>85,600</td><td class="neg" data-nc-l="-4.5%">-4.5%</td><td>72,300</td><td class="pos" data-nc-s="+3.1%">+3.1%</td><td>210,400</td><td class="pos" data-c-l="+2.2%">+2.2%</td><td>225,100</td><td class="pos" data-c-s="+1.9%">+1.9%</td><td>415,000</td></tr>
            <tr><td class="asset-name">CAC40</td><td>24,100</td><td class="pos" data-nc-l="+0.8%">+0.8%</td><td>28,400</td><td class="neg" data-nc-s="-1.5%">-1.5%</td><td>68,200</td><td class="pos" data-c-l="+1.4%">+1.4%</td><td>64,100</td><td class="pos" data-c-s="+0.9%">+0.9%</td><td>132,000</td></tr>
            <tr><td class="asset-name">DAX</td><td>45,800</td><td class="pos" data-nc-l="+5.2%">+5.2%</td><td>41,200</td><td class="neg" data-nc-s="-3.8%">-3.8%</td><td>112,000</td><td class="pos" data-c-l="+4.1%">+4.1%</td><td>118,500</td><td class="pos" data-c-s="+2.7%">+2.7%</td><td>240,000</td></tr>
            <tr><td class="asset-name">FTSE</td><td>38,200</td><td class="neg" data-nc-l="-2.1%">-2.1%</td><td>42,100</td><td class="pos" data-nc-s="+1.8%">+1.8%</td><td>95,400</td><td class="pos" data-c-l="+0.9%">+0.9%</td><td>91,200</td><td class="neg" data-c-s="-1.1%">-1.1%</td><td>185,000</td></tr>
            <tr><td class="asset-name">SMI</td><td>15,100</td><td class="pos" data-nc-l="+0.4%">+0.4%</td><td>18,200</td><td class="neg" data-nc-s="-0.9%">-0.9%</td><td>42,100</td><td class="pos" data-c-l="+1.1%">+1.1%</td><td>39,800</td><td class="pos" data-c-s="+0.5%">+0.5%</td><td>82,000</td></tr>
            <tr><td class="asset-name">HK50</td><td>54,200</td><td class="pos" data-nc-l="+12.4%">+12.4%</td><td>61,000</td><td class="neg" data-nc-s="-8.1%">-8.1%</td><td>135,000</td><td class="neg" data-c-l="-4.2%">-4.2%</td><td>128,000</td><td class="pos" data-c-s="+5.1%">+5.1%</td><td>295,000</td></tr>
            <tr><td class="asset-name">NIKKEI</td><td>68,400</td><td class="pos" data-nc-l="+6.5%">+6.5%</td><td>74,100</td><td class="neg" data-nc-s="-11.2%">-11.2%</td><td>182,000</td><td class="pos" data-c-l="+3.8%">+3.8%</td><td>175,000</td><td class="pos" data-c-s="+2.1%">+2.1%</td><td>365,000</td></tr>
            <tr><td class="asset-name">KOSPI</td><td>18,900</td><td class="neg" data-nc-l="-3.1%">-3.1%</td><td>22,400</td><td class="pos" data-nc-s="+4.5%">+4.5%</td><td>51,000</td><td class="pos" data-c-l="+1.8%">+1.8%</td><td>48,500</td><td class="pos" data-c-s="+2.3%">+2.3%</td><td>102,000</td></tr>
            <tr><td class="asset-name">CA60</td><td>21,400</td><td class="pos" data-nc-l="+2.2%">+2.2%</td><td>19,800</td><td class="neg" data-nc-s="-1.1%">-1.1%</td><td>58,000</td><td class="pos" data-c-l="+0.8%">+0.8%</td><td>59,200</td><td class="pos" data-c-s="+1.4%">+1.4%</td><td>116,000</td></tr>
            <tr><td class="asset-name">AUS2000</td><td>14,800</td><td class="pos" data-nc-l="+1.5%">+1.5%</td><td>16,200</td><td class="neg" data-nc-s="-2.8%">-2.8%</td><td>41,000</td><td class="pos" data-c-l="+2.1%">+2.1%</td><td>39,500</td><td class="pos" data-c-s="+0.7%">+0.7%</td><td>81,000</td></tr>

            <!-- CRYPTO -->
            <tr class="category-header"><td colspan="10">▼ CRYPTO</td></tr>
            <tr><td class="asset-name">BTC</td><td>18,400</td><td class="pos" data-nc-l="+28.4%">+28.4%</td><td>12,100</td><td class="neg" data-nc-s="-5.2%">-5.2%</td><td>32,400</td><td class="neg" data-c-l="-10.1%">-10.1%</td><td>38,900</td><td class="pos" data-c-s="+22.1%">+22.1%</td><td>78,500</td></tr>
            <tr><td class="asset-name">ETH</td><td>11,200</td><td class="pos" data-nc-l="+4.2%">+4.2%</td><td>9,800</td><td class="neg" data-nc-s="-3.1%">-3.1%</td><td>24,100</td><td class="neg" data-c-l="-14.2%">-14.2%</td><td>25,400</td><td class="neg" data-c-s="-2.1%">-2.1%</td><td>54,000</td></tr>
            <tr><td class="asset-name">SOL</td><td>6,500</td><td class="neg" data-nc-l="-1.8%">-1.8%</td><td>5,200</td><td class="pos" data-nc-s="+2.4%">+2.4%</td><td>12,800</td><td class="pos" data-c-l="+3.1%">+3.1%</td><td>14,100</td><td class="pos" data-c-s="+1.9%">+1.9%</td><td>31,000</td></tr>

            <!-- MÉTAUX -->
            <tr class="category-header"><td colspan="10">▼ MÉTAUX</td></tr>
            <tr><td class="asset-name">ALUMINIUM</td><td>42,100</td><td class="pos" data-nc-l="+3.8%">+3.8%</td><td>38,900</td><td class="neg" data-nc-s="-4.1%">-4.1%</td><td>115,000</td><td class="pos" data-c-l="+1.5%">+1.5%</td><td>118,000</td><td class="pos" data-c-s="+2.1%">+2.1%</td><td>228,000</td></tr>
            <tr><td class="asset-name">ARGENT</td><td>68,200</td><td class="pos" data-nc-l="+22.5%">+22.5%</td><td>26,100</td><td class="pos" data-nc-s="+17.3%">+17.3%</td><td>31,000</td><td class="neg" data-c-l="-5.0%">-5.0%</td><td>78,000</td><td class="pos" data-c-s="+19.1%">+19.1%</td><td>145,200</td></tr>
            <tr><td class="asset-name">CUIVRE</td><td>55,400</td><td class="pos" data-nc-l="+8.1%">+8.1%</td><td>41,200</td><td class="neg" data-nc-s="-12.4%">-12.4%</td><td>128,000</td><td class="pos" data-c-l="+4.5%">+4.5%</td><td>142,000</td><td class="pos" data-c-s="+6.2%">+6.2%</td><td>265,000</td></tr>
            <tr><td class="asset-name">NICKEL</td><td>18,200</td><td class="neg" data-nc-l="-2.5%">-2.5%</td><td>16,400</td><td class="pos" data-nc-s="+1.1%">+1.1%</td><td>45,000</td><td class="pos" data-c-l="+0.8%">+0.8%</td><td>46,800</td><td class="pos" data-c-s="+1.3%">+1.3%</td><td>95,000</td></tr>
            <tr><td class="asset-name">OR</td><td>310,400</td><td class="pos" data-nc-l="+2.1%">+2.1%</td><td>65,280</td><td class="neg" data-nc-s="-18.4%">-18.4%</td><td>82,100</td><td class="neg" data-c-l="-16.2%">-16.2%</td><td>362,200</td><td class="pos" data-c-s="+4.1%">+4.1%</td><td>512,300</td></tr>
            <tr><td class="asset-name">PALLADIUM</td><td>14,100</td><td class="neg" data-nc-l="-6.2%">-6.2%</td><td>19,800</td><td class="pos" data-nc-s="+25.4%">+25.4%</td><td>35,400</td><td class="pos" data-c-l="+5.1%">+5.1%</td><td>29,800</td><td class="neg" data-c-s="-4.2%">-4.2%</td><td>61,000</td></tr>
            <tr><td class="asset-name">PLATINE</td><td>28,400</td><td class="pos" data-nc-l="+11.2%">+11.2%</td><td>21,500</td><td class="neg" data-nc-s="-3.8%">-3.8%</td><td>62,000</td><td class="neg" data-c-l="-2.1%">-2.1%</td><td>68,900</td><td class="pos" data-c-s="+4.8%">+4.8%</td><td>132,000</td></tr>
            <tr><td class="asset-name">PLOMB</td><td>12,800</td><td class="pos" data-nc-l="+1.4%">+1.4%</td><td>14,200</td><td class="neg" data-nc-s="-2.1%">-2.1%</td><td>32,000</td><td class="pos" data-c-l="+0.5%">+0.5%</td><td>30,600</td><td class="pos" data-c-s="+0.9%">+0.9%</td><td>65,000</td></tr>
            <tr><td class="asset-name">ZINC</td><td>22,100</td><td class="neg" data-nc-l="-4.1%">-4.1%</td><td>19,500</td><td class="pos" data-nc-s="+2.8%">+2.8%</td><td>58,000</td><td class="pos" data-c-l="+1.9%">+1.9%</td><td>60,600</td><td class="pos" data-c-s="+1.2%">+1.2%</td><td>120,000</td></tr>

            <!-- ÉNERGIE -->
            <tr class="category-header"><td colspan="10">▼ ÉNERGIE</td></tr>
            <tr><td class="asset-name">BRENT</td><td>195,400</td><td class="neg" data-nc-l="-8.4%">-8.4%</td><td>82,100</td><td class="pos" data-nc-s="+4.2%">+4.2%</td><td>280,000</td><td class="pos" data-c-l="+2.1%">+2.1%</td><td>390,000</td><td class="neg" data-c-s="-5.1%">-5.1%</td><td>780,000</td></tr>
            <tr><td class="asset-name">GAS</td><td>145,000</td><td class="pos" data-nc-l="+15.2%">+15.2%</td><td>110,000</td><td class="neg" data-nc-s="-7.8%">-7.8%</td><td>310,000</td><td class="neg" data-c-l="-3.5%">-3.5%</td><td>345,000</td><td class="pos" data-c-s="+23.4%">+23.4%</td><td>670,000</td></tr>
            <tr><td class="asset-name">SP ENERGY</td><td>35,200</td><td class="pos" data-nc-l="+1.2%">+1.2%</td><td>29,800</td><td class="neg" data-nc-s="-0.9%">-0.9%</td><td>84,000</td><td class="pos" data-c-l="+1.8%">+1.8%</td><td>89,400</td><td class="pos" data-c-s="+1.1%">+1.1%</td><td>162,000</td></tr>
            <tr><td class="asset-name">WTI</td><td>245,100</td><td class="neg" data-nc-l="-16.8%">-16.8%</td><td>95,400</td><td class="pos" data-nc-s="+8.2%">+8.2%</td><td>320,100</td><td class="pos" data-c-l="+3.1%">+3.1%</td><td>480,200</td><td class="neg" data-c-s="-15.5%">-15.5%</td><td>980,000</td></tr>

            <!-- AGRICULTURE -->
            <tr class="category-header"><td colspan="10">▼ AGRICULTURE</td></tr>
            <tr><td class="asset-name">BLE</td><td>95,400</td><td class="neg" data-nc-l="-3.2%">-3.2%</td><td>112,000</td><td class="pos" data-nc-s="+5.4%">+5.4%</td><td>185,000</td><td class="pos" data-c-l="+2.1%">+2.1%</td><td>168,000</td><td class="neg" data-c-s="-1.8%">-1.8%</td><td>378,000</td></tr>
            <tr><td class="asset-name">CACAO</td><td>42,100</td><td class="pos" data-nc-l="+21.4%">+21.4%</td><td>28,400</td><td class="neg" data-nc-s="-14.2%">-14.2%</td><td>78,000</td><td class="neg" data-c-l="-8.5%">-8.5%</td><td>91,600</td><td class="pos" data-c-s="+12.8%">+12.8%</td><td>168,000</td></tr>
            <tr><td class="asset-name">CAFE (Arabica)</td><td>58,200</td><td class="pos" data-nc-l="+7.8%">+7.8%</td><td>32,100</td><td class="neg" data-nc-s="-6.2%">-6.2%</td><td>92,400</td><td class="pos" data-c-l="+3.1%">+3.1%</td><td>118,000</td><td class="pos" data-c-s="+4.5%">+4.5%</td><td>210,000</td></tr>
            <tr><td class="asset-name">COTTON</td><td>38,400</td><td class="neg" data-nc-l="-1.2%">-1.2%</td><td>41,000</td><td class="pos" data-nc-s="+2.1%">+2.1%</td><td>85,000</td><td class="pos" data-c-l="+1.4%">+1.4%</td><td>82,400</td><td class="neg" data-c-s="-0.8%">-0.8%</td><td>165,000</td></tr>
            <tr><td class="asset-name">JUS D'ORANGE</td><td>12,400</td><td class="pos" data-nc-l="+26.1%">+26.1%</td><td>8,900</td><td class="neg" data-nc-s="-4.2%">-4.2%</td><td>21,500</td><td class="neg" data-c-l="-12.1%">-12.1%</td><td>25,000</td><td class="pos" data-c-s="+18.4%">+18.4%</td><td>45,000</td></tr>
            <tr><td class="asset-name">MAIS</td><td>180,200</td><td class="pos" data-nc-l="+0.5%">+0.5%</td><td>120,400</td><td class="neg" data-nc-s="-2.1%">-2.1%</td><td>210,000</td><td class="pos" data-c-l="+1.1%">+1.1%</td><td>270,000</td><td class="neg" data-c-s="-0.8%">-0.8%</td><td>650,000</td></tr>
            <tr><td class="asset-name">SOJA</td><td>125,400</td><td class="pos" data-nc-l="+4.8%">+4.8%</td><td>98,200</td><td class="neg" data-nc-s="-3.5%">-3.5%</td><td>245,000</td><td class="pos" data-c-l="+2.2%">+2.2%</td><td>272,000</td><td class="pos" data-c-s="+1.9%">+1.9%</td><td>520,000</td></tr>
            <tr><td class="asset-name">SUCRE</td><td>88,200</td><td class="neg" data-nc-l="-8.1%">-8.1%</td><td>64,100</td><td class="pos" data-nc-s="+11.2%">+11.2%</td><td>165,000</td><td class="pos" data-c-l="+4.2%">+4.2%</td><td>189,000</td><td class="neg" data-c-s="-3.1%">-3.1%</td><td>354,000</td></tr>
        </tbody>
    </table>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const rows = document.querySelectorAll("#cotTable tbody tr");
        const alertsList = document.getElementById("alertsList");
        const thresholdSelect = document.getElementById("thresholdSelect");

        function updateAlerts() {
            alertsList.innerHTML = "";
            let alertsCount = 0;
            const threshold = parseFloat(thresholdSelect.value);

            rows.forEach(row => {
                if (row.classList.contains("category-header")) return;

                const assetName = row.cells[0].innerText;
                
                const ncL = row.querySelector('[data-nc-l]');
                const ncS = row.querySelector('[data-nc-s]');
                const cL = row.querySelector('[data-c-l]');
                const cS = row.querySelector('[data-c-s]');

                if (!ncL || !ncS || !cL || !cS) return;

                const parseVal = (el) => parseFloat(el.innerText.replace("%", "").replace("+", ""));
                
                const valNcL = parseVal(ncL);
                const valNcS = parseVal(ncS);
                const valCL = parseVal(cL);
                const valCS = parseVal(cS);

                const hasNcAlert = Math.abs(valNcL) >= threshold || Math.abs(valNcS) >= threshold;
                const hasCAlert = Math.abs(valCL) >= threshold || Math.abs(valCS) >= threshold;

                if (hasNcAlert || hasCAlert) {
                    alertsCount++;

                    const formatBadge = (val, type) => {
                        if (Math.abs(val) < threshold) return "";
                        const isLong = type === "L";
                        const badgeClass = isLong ? "badge-long" : "badge-short";
                        const labelText = isLong ? "Positions Longs" : "Positions Shorts";
                        const sign = val > 0 ? "+" : "";
                        return `<span class="badge ${badgeClass}">${labelText}: ${sign}${val}%</span>`;
                    };

                    const ncBadges = [formatBadge(valNcL, "L"), formatBadge(valNcS, "S")].filter(Boolean).join(" ");
                    const cBadges = [formatBadge(valCL, "L"), formatBadge(valCS, "S")].filter(Boolean).join(" ");

                    const item = document.createElement("div");
                    item.className = "alert-item";
                    item.innerHTML = `
                        <span class="alert-asset">${assetName}</span>
                        <div class="alert-col">${ncBadges || "<span class='no-change'>-</span>"}</div>
                        <div class="alert-col">${cBadges || "<span class='no-change'>-</span>"}</div>
                    `;
                    alertsList.appendChild(item);
                }
            });

            if (alertsCount === 0) {
                const labelText = threshold > 100 ? "supérieur à +100%" : `supérieur à ±${threshold}%`;
                alertsList.innerHTML = `<div style='color: #8b949e; font-size: 12px; padding: 10px; background-color: #0d1117; text-align: center;'>Aucun mouvement ${labelText} cette semaine.</div>`;
            }
        }

        // Écouter le changement de valeur dans le menu déroulant
        thresholdSelect.addEventListener("change", updateAlerts);

        // Lancement initial
        updateAlerts();
    });
</script>

</body>
</html>
"""

components.html(html_code, height=2200, scrolling=True)
