import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="COT Report Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
            <tr class="category-header"><td colspan="10">▼ MAJOR CURRENCIES</td></tr>
            <tr>
                <td class="asset-name">NEW ZEALAND DOLLAR</td>
                <td>26,110</td><td class="pos" data-nc-l="+131.1%">+131.1%</td>
                <td>19,878</td><td class="pos" data-nc-s="+2.9%">+2.9%</td>
                <td>87,479</td><td class="neg" data-c-l="-2.8%">-2.8%</td>
                <td>93,114</td><td class="pos" data-c-s="+14.3%">+14.3%</td>
                <td>125,978</td>
            </tr>
            <tr>
                <td class="asset-name">BRITISH POUND STERLING</td>
                <td>73,520</td><td class="neg" data-nc-l="-13.9%">-13.9%</td>
                <td>132,356</td><td class="neg" data-nc-s="-1.9%">-1.9%</td>
                <td>205,647</td><td class="pos" data-c-l="+5.2%">+5.2%</td>
                <td>148,545</td><td class="neg" data-c-s="-0.7%">-0.7%</td>
                <td>318,608</td>
            </tr>
            <tr>
                <td class="asset-name">SWISS FRANC</td>
                <td>17,273</td><td class="neg" data-nc-l="-13.3%">-13.3%</td>
                <td>47,258</td><td class="pos" data-nc-s="+10.4%">+10.4%</td>
                <td>112,612</td><td class="pos" data-c-l="+27.6%">+27.6%</td>
                <td>71,108</td><td class="pos" data-c-s="+36.3%">+36.3%</td>
                <td>153,683</td>
            </tr>
            <tr>
                <td class="asset-name">JAPANESE YEN</td>
                <td>178,791</td><td class="pos" data-nc-l="+52.6%">+52.6%</td>
                <td>167,995</td><td class="neg" data-nc-s="-19.8%">-19.8%</td>
                <td>249,469</td><td class="pos" data-c-l="+10.8%">+10.8%</td>
                <td>263,510</td><td class="pos" data-c-s="+106.5%">+106.5%</td>
                <td>499,635</td>
            </tr>
            <tr>
                <td class="asset-name">CANADIAN DOLLAR</td>
                <td>54,444</td><td class="pos" data-nc-l="+50.1%">+50.1%</td>
                <td>124,943</td><td class="neg" data-nc-s="-13.5%">-13.5%</td>
                <td>244,052</td><td class="neg" data-c-l="-8.6%">-8.6%</td>
                <td>169,623</td><td class="pos" data-c-s="+11.9%">+11.9%</td>
                <td>334,861</td>
            </tr>
            <tr>
                <td class="asset-name">AUSTRALIAN DOLLAR</td>
                <td>120,532</td><td class="pos" data-nc-l="+5.6%">+5.6%</td>
                <td>155,402</td><td class="pos" data-nc-s="+1.2%">+1.2%</td>
                <td>271,564</td><td class="pos" data-c-l="+15.5%">+15.5%</td>
                <td>255,880</td><td class="pos" data-c-s="+18.3%">+18.3%</td>
                <td>455,468</td>
            </tr>
            <tr>
                <td class="asset-name">EURO FX</td>
                <td>198,509</td><td class="neg" data-nc-l="-2.4%">-2.4%</td>
                <td>241,125</td><td class="pos" data-nc-s="+5.6%">+5.6%</td>
                <td>593,162</td><td class="pos" data-c-l="+11.1%">+11.1%</td>
                <td>586,432</td><td class="pos" data-c-s="+8.1%">+8.1%</td>
                <td>942,464</td>
            </tr>
            <tr>
                <td class="asset-name">U.S. DOLLAR INDEX</td>
                <td>28,407</td><td class="pos" data-nc-l="+0.6%">+0.6%</td>
                <td>10,803</td><td class="neg" data-nc-s="-3.7%">-3.7%</td>
                <td>18,620</td><td class="pos" data-c-l="+14.2%">+14.2%</td>
                <td>37,808</td><td class="pos" data-c-s="+7.9%">+7.9%</td>
                <td>57,858</td>
            </tr>

            <!-- INDICES -->
            <tr class="category-header"><td colspan="10">▼ INDICES</td></tr>
            <tr>
                <td class="asset-name">S&P 500 E-MINI</td>
                <td>215,400</td><td class="pos" data-nc-l="+18.2%">+18.2%</td>
                <td>180,100</td><td class="neg" data-nc-s="-4.1%">-4.1%</td>
                <td>920,500</td><td class="neg" data-c-l="-2.0%">-2.0%</td>
                <td>980,100</td><td class="pos" data-c-s="+16.4%">+16.4%</td>
                <td>2,150,000</td>
            </tr>
            <tr>
                <td class="asset-name">NASDAQ 100 E-MINI</td>
                <td>62,100</td><td class="pos" data-nc-l="+3.5%">+3.5%</td>
                <td>45,200</td><td class="pos" data-nc-s="+21.0%">+21.0%</td>
                <td>145,000</td><td class="neg" data-c-l="-12.1%">-12.1%</td>
                <td>162,000</td><td class="neg" data-c-s="-1.5%">-1.5%</td>
                <td>320,000</td>
            </tr>

            <!-- MÉTAUX -->
            <tr class="category-header"><td colspan="10">▼ MÉTAUX</td></tr>
            <tr>
                <td class="asset-name">GOLD</td>
                <td>310,400</td><td class="pos" data-nc-l="+2.1%">+2.1%</td>
                <td>65,280</td><td class="neg" data-nc-s="-18.4%">-18.4%</td>
                <td>82,100</td><td class="neg" data-c-l="-16.2%">-16.2%</td>
                <td>362,200</td><td class="pos" data-c-s="+4.1%">+4.1%</td>
                <td>512,300</td>
            </tr>
            <tr>
                <td class="asset-name">SILVER</td>
                <td>68,200</td><td class="pos" data-nc-l="+22.5%">+22.5%</td>
                <td>26,100</td><td class="pos" data-nc-s="+17.3%">+17.3%</td>
                <td>31,000</td><td class="neg" data-c-l="-5.0%">-5.0%</td>
                <td>78,000</td><td class="pos" data-c-s="+19.1%">+19.1%</td>
                <td>145,200</td>
            </tr>

            <!-- ÉNERGIE -->
            <tr class="category-header"><td colspan="10">▼ ÉNERGIE</td></tr>
            <tr>
                <td class="asset-name">CRUDE OIL (WTI)</td>
                <td>245,100</td><td class="neg" data-nc-l="-16.8%">-16.8%</td>
                <td>95,400</td><td class="pos" data-nc-s="+8.2%">+8.2%</td>
                <td>320,100</td><td class="pos" data-c-l="+3.1%">+3.1%</td>
                <td>480,200</td><td class="neg" data-c-s="-15.5%">-15.5%</td>
                <td>980,000</td>
            </tr>
            <tr>
                <td class="asset-name">CORN</td>
                <td>180,200</td><td class="pos" data-nc-l="+0.5%">+0.5%</td>
                <td>120,400</td><td class="neg" data-nc-s="-2.1%">-2.1%</td>
                <td>210,000</td><td class="pos" data-c-l="+1.1%">+1.1%</td>
                <td>270,000</td><td class="neg" data-c-s="-0.8%">-0.8%</td>
                <td>650,000</td>
            </tr>
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

components.html(html_code, height=1400, scrolling=True)
