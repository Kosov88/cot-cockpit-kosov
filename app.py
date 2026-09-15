import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page Streamlit
st.set_page_config(
    page_title="COT Report Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style pour afficher le composant en plein écran sans marges
st.markdown("""
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
""", unsafe_allow_html=True)

# Code HTML / CSS / JS du Dashboard
html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COT REPORT - WEEKLY SUMMARY</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            background-color: #0e1117;
            color: #e0e0e0;
            padding: 10px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #161b22;
            padding: 15px 20px;
            border-radius: 6px;
            margin-bottom: 15px;
            border: 1px solid #30363d;
        }
        .title {
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 1px;
            color: #ffffff;
        }
        .title span {
            color: #58a6ff;
        }
        .date {
            font-size: 14px;
            color: #8b949e;
        }
        .table-container {
            overflow-x: auto;
            background-color: #161b22;
            border-radius: 6px;
            border: 1px solid #30363d;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: right;
        }
        th, td {
            padding: 10px 12px;
            border-bottom: 1px solid #21262d;
            white-space: nowrap;
        }
        th {
            background-color: #0d1117;
            color: #8b949e;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        tr.category-header {
            background-color: #1f242c;
            font-weight: bold;
            color: #58a6ff;
            text-align: left;
        }
        tr.category-header td {
            text-align: left;
            padding: 12px;
            font-size: 13px;
        }
        td.asset-name {
            text-align: left;
            font-weight: bold;
            color: #f0f6fc;
        }
        .pos { color: #3fb950; }
        .neg { color: #f85149; }
        .bar-container {
            display: flex;
            align-items: center;
            gap: 6px;
            justify-content: flex-end;
        }
        .bar {
            height: 8px;
            border-radius: 4px;
            display: flex;
            overflow: hidden;
            width: 80px;
            background-color: #21262d;
        }
        .bar-long { background-color: #238636; }
        .bar-short { background-color: #da3633; }
    </style>
</head>
<body>

<div class="header">
    <div class="title">COT REPORT <span>• WEEKLY SUMMARY</span></div>
    <div class="date">Sep 15, 2026</div>
</div>

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th style="text-align:left;">CONTRACTS</th>
                <th colspan="4" style="text-align:center; background-color:#161b22; color:#58a6ff;">NON-COMMERCIAL (Large Speculators)</th>
                <th colspan="4" style="text-align:center; background-color:#161b22; color:#3fb950;">COMMERCIAL (Hedgers)</th>
                <th colspan="4" style="text-align:center; background-color:#161b22; color:#f85149;">NON-REPORTABLE (Small Speculators)</th>
                <th>OPEN INTEREST</th>
            </tr>
            <tr>
                <th style="text-align:left;">Asset</th>
                <th>Net Pos</th>
                <th>Long</th>
                <th>Short</th>
                <th>L vs S</th>
                <th>Net Pos</th>
                <th>Long</th>
                <th>Short</th>
                <th>L vs S</th>
                <th>Net Pos</th>
                <th>Long</th>
                <th>Short</th>
                <th>L vs S</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <!-- MAJOR CURRENCIES -->
            <tr class="category-header">
                <td colspan="14">▼ MAJOR CURRENCIES</td>
            </tr>
            <tr>
                <td class="asset-name">NEW ZEALAND DOLLAR</td>
                <td class="pos">+6,232</td>
                <td>26,110</td>
                <td>19,878</td>
                <td><div class="bar-container"><span>57%</span><div class="bar"><div class="bar-long" style="width:57%"></div><div class="bar-short" style="width:43%"></div></div></div></td>
                <td class="neg">-5,635</td>
                <td>87,479</td>
                <td>93,114</td>
                <td><div class="bar-container"><span>48%</span><div class="bar"><div class="bar-long" style="width:48%"></div><div class="bar-short" style="width:52%"></div></div></div></td>
                <td class="neg">-597</td>
                <td>4,520</td>
                <td>5,117</td>
                <td><div class="bar-container"><span>47%</span><div class="bar"><div class="bar-long" style="width:47%"></div><div class="bar-short" style="width:53%"></div></div></div></td>
                <td>125,978</td>
            </tr>
            <tr>
                <td class="asset-name">BRITISH POUND STERLING</td>
                <td class="neg">-58,836</td>
                <td>73,520</td>
                <td>132,356</td>
                <td><div class="bar-container"><span>36%</span><div class="bar"><div class="bar-long" style="width:36%"></div><div class="bar-short" style="width:64%"></div></div></div></td>
                <td class="pos">+57,102</td>
                <td>205,647</td>
                <td>148,545</td>
                <td><div class="bar-container"><span>58%</span><div class="bar"><div class="bar-long" style="width:58%"></div><div class="bar-short" style="width:42%"></div></div></div></td>
                <td class="pos">+1,734</td>
                <td>31,683</td>
                <td>29,949</td>
                <td><div class="bar-container"><span>51%</span><div class="bar"><div class="bar-long" style="width:51%"></div><div class="bar-short" style="width:49%"></div></div></div></td>
                <td>318,608</td>
            </tr>
            <tr>
                <td class="asset-name">JAPANESE YEN</td>
                <td class="pos">+10,796</td>
                <td>178,791</td>
                <td>167,995</td>
                <td><div class="bar-container"><span>52%</span><div class="bar"><div class="bar-long" style="width:52%"></div><div class="bar-short" style="width:48%"></div></div></div></td>
                <td class="neg">-14,041</td>
                <td>249,469</td>
                <td>263,510</td>
                <td><div class="bar-container"><span>49%</span><div class="bar"><div class="bar-long" style="width:49%"></div><div class="bar-short" style="width:51%"></div></div></div></td>
                <td class="pos">+3,245</td>
                <td>42,640</td>
                <td>39,395</td>
                <td><div class="bar-container"><span>52%</span><div class="bar"><div class="bar-long" style="width:52%"></div><div class="bar-short" style="width:48%"></div></div></div></td>
                <td>499,635</td>
            </tr>
            <tr>
                <td class="asset-name">EURO FX</td>
                <td class="neg">-42,616</td>
                <td>198,509</td>
                <td>241,125</td>
                <td><div class="bar-container"><span>45%</span><div class="bar"><div class="bar-long" style="width:45%"></div><div class="bar-short" style="width:55%"></div></div></div></td>
                <td class="pos">+6,730</td>
                <td>593,162</td>
                <td>586,432</td>
                <td><div class="bar-container"><span>50%</span><div class="bar"><div class="bar-long" style="width:50%"></div><div class="bar-short" style="width:50%"></div></div></div></td>
                <td class="pos">+35,886</td>
                <td>92,781</td>
                <td>56,895</td>
                <td><div class="bar-container"><span>62%</span><div class="bar"><div class="bar-long" style="width:62%"></div><div class="bar-short" style="width:38%"></div></div></div></td>
                <td>942,464</td>
            </tr>
            <tr>
                <td class="asset-name">U.S. DOLLAR INDEX</td>
                <td class="pos">+17,604</td>
                <td>28,407</td>
                <td>10,803</td>
                <td><div class="bar-container"><span>72%</span><div class="bar"><div class="bar-long" style="width:72%"></div><div class="bar-short" style="width:28%"></div></div></div></td>
                <td class="neg">-19,188</td>
                <td>18,620</td>
                <td>37,808</td>
                <td><div class="bar-container"><span>33%</span><div class="bar"><div class="bar-long" style="width:33%"></div><div class="bar-short" style="width:67%"></div></div></div></td>
                <td class="pos">+1,584</td>
                <td>3,246</td>
                <td>1,662</td>
                <td><div class="bar-container"><span>66%</span><div class="bar"><div class="bar-long" style="width:66%"></div><div class="bar-short" style="width:34%"></div></div></div></td>
                <td>57,858</td>
            </tr>

            <!-- CRYPTOCURRENCIES -->
            <tr class="category-header">
                <td colspan="14">▼ CRYPTOCURRENCIES</td>
            </tr>
            <tr>
                <td class="asset-name">BITCOIN</td>
                <td class="pos">+1,524</td>
                <td>17,600</td>
                <td>16,076</td>
                <td><div class="bar-container"><span>52%</span><div class="bar"><div class="bar-long" style="width:52%"></div><div class="bar-short" style="width:48%"></div></div></div></td>
                <td class="neg">-2,061</td>
                <td>64</td>
                <td>2,125</td>
                <td><div class="bar-container"><span>3%</span><div class="bar"><div class="bar-long" style="width:3%"></div><div class="bar-short" style="width:97%"></div></div></div></td>
                <td class="pos">+537</td>
                <td>1,273</td>
                <td>736</td>
                <td><div class="bar-container"><span>63%</span><div class="bar"><div class="bar-long" style="width:63%"></div><div class="bar-short" style="width:37%"></div></div></div></td>
                <td>21,083</td>
            </tr>
            <tr>
                <td class="asset-name">ETHEREUM</td>
                <td class="neg">-3,103,337</td>
                <td>1,262,856</td>
                <td>4,366,193</td>
                <td><div class="bar-container"><span>22%</span><div class="bar"><div class="bar-long" style="width:22%"></div><div class="bar-short" style="width:78%"></div></div></div></td>
                <td class="pos">+3,101,838</td>
                <td>9,345,044</td>
                <td>6,243,206</td>
                <td><div class="bar-container"><span>60%</span><div class="bar"><div class="bar-long" style="width:60%"></div><div class="bar-short" style="width:40%"></div></div></div></td>
                <td class="pos">+1,499</td>
                <td>78,805</td>
                <td>77,306</td>
                <td><div class="bar-container"><span>50%</span><div class="bar"><div class="bar-long" style="width:50%"></div><div class="bar-short" style="width:50%"></div></div></div></td>
                <td>13,294,407</td>
            </tr>
        </tbody>
    </table>
</div>

</body>
</html>
"""

# Affichage du HTML dans Streamlit avec hauteur dynamique
components.html(html_code, height=900, scrolling=True)
