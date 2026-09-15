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
    <title>COT REPORT - WEEKLY SUMMARY</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #0e1117; color: #e0e0e0; padding: 10px; }
        
        .header { display: flex; justify-content: space-between; align-items: center; background-color: #161b22; padding: 15px 20px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #30363d; }
        .title { font-size: 20px; font-weight: bold; color: #ffffff; }
        .title span { color: #58a6ff; }
        .date { font-size: 14px; color: #8b949e; }
        
        /* Bloc résumé en liste verticale */
        .alerts-container { background-color: #161b22; border-radius: 6px; border: 1px solid #30363d; padding: 15px; margin-bottom: 15px; }
        .alerts-title { font-size: 14px; font-weight: bold; color: #f2994a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
        
        .alerts-list { display: flex; flex-direction: column; gap: 8px; }
        .alert-item { background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px; padding: 8px 12px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; }
        .alert-asset { font-weight: bold; color: #f0f6fc; }
        .alert-details { display: flex; gap: 10px; align-items: center; }
        
        .badge { font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
        .badge-up { background-color: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid #238636; }
        .badge-down { background-color: rgba(248, 81, 73, 0.15); color: #f85149; border: 1px solid #da3633; }

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
    <div class="title">COT REPORT <span>• FUSION MARKETS ASSETS</span></div>
    <div class="date">Sep 15, 2026</div>
</div>

<!-- RÉSUMÉ EN LISTE DES MOUVEMENTS INHABITUELS -->
<div class="alerts-container">
    <div class="alerts-title">⚠️ Mouvements Inhabituels (Change in Longs/Shorts ≥ ±20%)</div>
    <div class="alerts-list" id="alertsList">
        <!-- Généré dynamiquement en liste -->
    </div>
</div>

<div class="table-container">
    <table id="cotTable">
        <thead>
            <tr>
                <th style="text-align:left;">CONTRACTS</th>
                <th colspan="5" style="text-align:center; color:#58a6ff;">NON-COMMERCIAL (Large Specs)</th>
                <th>OPEN INTEREST</th>
            </tr>
            <tr>
                <th style="text-align:left;">Asset</th>
                <th>Net Pos</th>
                <th>Long</th>
                <th>Δ Long (%)</th>
                <th>Short</th>
                <th>Δ Short (%)</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <tr class="category-header"><td colspan="7">▼ DEVISES</td></tr>
            <tr>
                <td class="asset-name">US Dollar Index (DXY)</td>
                <td class="pos">+17,604</td>
                <td>28,407</td>
                <td class="pos" data-change="long">+24%</td>
                <td>10,803</td>
                <td class="neg" data-change="short">-5%</td>
                <td>57,858</td>
            </tr>
            <tr>
                <td class="asset-name">EUR</td>
                <td class="neg">-42,616</td>
                <td>198,509</td>
                <td class="neg" data-change="long">-3%</td>
                <td>241,125</td>
                <td class="pos" data-change="short">+28%</td>
                <td>942,464</td>
            </tr>
            <tr>
                <td class="asset-name">GBP</td>
                <td class="neg">-58,836</td>
                <td>73,520</td>
                <td class="neg" data-change="long">-22%</td>
                <td>132,356</td>
                <td class="pos" data-change="short">+12%</td>
                <td>318,608</td>
            </tr>

            <tr class="category-header"><td colspan="7">▼ MÉTAUX</td></tr>
            <tr>
                <td class="asset-name">OR (Gold)</td>
                <td class="pos">+245,120</td>
                <td>310,400</td>
                <td class="pos" data-change="long">+5%</td>
                <td>65,280</td>
                <td class="neg" data-change="short">-31%</td>
                <td>512,300</td>
            </tr>
            <tr>
                <td class="asset-name">ARGENT (Silver)</td>
                <td class="pos">+42,100</td>
                <td>68,200</td>
                <td class="pos" data-change="long">+35%</td>
                <td>26,100</td>
                <td class="pos" data-change="short">+21%</td>
                <td>145,200</td>
            </tr>
        </tbody>
    </table>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const rows = document.querySelectorAll("#cotTable tbody tr");
        const alertsList = document.getElementById("alertsList");
        let alertsCount = 0;

        rows.forEach(row => {
            if (row.classList.contains("category-header")) return;

            const assetName = row.cells[0].innerText;
            const longChangeCell = row.querySelector('[data-change="long"]');
            const shortChangeCell = row.querySelector('[data-change="short"]');

            if (!longChangeCell || !shortChangeCell) return;

            const longChange = parseFloat(longChangeCell.innerText.replace("%", "").replace("+", ""));
            const shortChange = parseFloat(shortChangeCell.innerText.replace("%", "").replace("+", ""));

            let details = [];

            if (Math.abs(longChange) >= 20) {
                const badgeClass = longChange > 0 ? "badge-up" : "badge-down";
                const sign = longChange > 0 ? "+" : "";
                details.push(`<span class="badge ${badgeClass}">Longs: ${sign}${longChange}%</span>`);
            }

            if (Math.abs(shortChange) >= 20) {
                const badgeClass = shortChange > 0 ? "badge-up" : "badge-down";
                const sign = shortChange > 0 ? "+" : "";
                details.push(`<span class="badge ${badgeClass}">Shorts: ${sign}${shortChange}%</span>`);
            }

            if (details.length > 0) {
                alertsCount++;
                const item = document.createElement("div");
                item.className = "alert-item";
                item.innerHTML = `
                    <span class="alert-asset">${assetName}</span>
                    <div class="alert-details">${details.join(" ")}</div>
                `;
                alertsList.appendChild(item);
            }
        });

        if (alertsCount === 0) {
            alertsList.innerHTML = "<div style='color: #8b949e; font-size: 12px;'>Aucun mouvement supérieur à ±20% sur les Longs ou Shorts cette semaine.</div>";
        }
    });
</script>

</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
