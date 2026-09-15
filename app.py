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
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #0e1117; color: #e0e0e0; padding: 10px; }
        
        .header { display: flex; justify-content: space-between; align-items: center; background-color: #161b22; padding: 15px 20px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #30363d; }
        .title { font-size: 20px; font-weight: bold; color: #ffffff; }
        .title span { color: #58a6ff; }
        .date { font-size: 14px; color: #8b949e; }
        
        /* Bloc résumé en 3 colonnes */
        .alerts-container { background-color: #161b22; border-radius: 6px; border: 1px solid #30363d; padding: 15px; margin-bottom: 15px; }
        .alerts-title { font-size: 14px; font-weight: bold; color: #f2994a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
        
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

<!-- RÉSUMÉ EN LISTE : 3 COLONNES -->
<div class="alerts-container">
    <div class="alerts-title">⚠️ Mouvements Inhabituels (Changements Longs/Shorts ≥ ±20%)</div>
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
            <tr><td class="asset-name">ETH</td><td>11,200</td><td class="pos" data-nc-l="+4.2%">+4.2%</td><td>9,800</td><td class="pos" data-nc-s="+31.5%">+31.5%</td><td>24,100</td><td class="neg" data-c-l="-14.2%">-14.2%</td><td>25,400</td><td class="neg" data-c-s="-2.1%">-2.1%</td><td>54,000</td></tr>
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
        let alertsCount = 0;
        const THRESHOLD = 20;

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

            const hasNcAlert = Math.abs(valNcL) >= THRESHOLD || Math.abs(valNcS) >= THRESHOLD;
            const hasCAlert = Math.abs(valCL) >= THRESHOLD || Math.abs(valCS) >= THRESHOLD;

            if (hasNcAlert || hasCAlert) {
                alertsCount++;

                const formatBadge = (val, type) => {
                    if (Math.abs(val) < THRESHOLD) return "";
                    const isLong = type === "L";
                    const badgeClass = isLong ? "badge-long" : "badge-short";
                    const sign = val > 0 ? "+" : "";
                    return `<span class="badge ${badgeClass}">${type}: ${sign}${val}%</span>`;
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
            alertsList.innerHTML = "<div style='color: #8b949e; font-size: 12px; padding: 10px; background-color: #0d1117; text-align: center;'>Aucun mouvement supérieur à ±20% cette semaine.</div>";
        }
    });
</script>

</body>
</html>
"""

components.html(html_code, height=2200, scrolling=True)
