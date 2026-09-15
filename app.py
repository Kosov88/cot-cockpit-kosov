<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>COT REPORT • WEEKLY SUMMARY • ALL TRADERS TYPES</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- FontAwesome Icons CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Plotly.js for Detailed Charts -->
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
          },
          colors: {
            cotBg: '#0b0d11',
            cotCard: '#131720',
            cotHeader: '#1a1f2c',
            cotBorder: '#232938',
            cotGreen: '#00e676',
            cotGreenBg: 'rgba(0, 230, 118, 0.12)',
            cotRed: '#ff4d4d',
            cotRedBg: 'rgba(255, 77, 77, 0.12)',
            cotBlue: '#3b82f6',
            cotYellow: '#eab308',
            cotText: '#e2e8f0',
            cotMuted: '#94a3b8'
          }
        }
      }
    }
  </script>

  <style>
    /* Custom scrollbars for clean table layout */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #0b0d11;
    }
    ::-webkit-scrollbar-thumb {
      background: #232938;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #3b82f6;
    }

    /* Fixed table styling for tight alignment */
    .cot-table {
      border-collapse: separate;
      border-spacing: 0;
    }
    
    .sticky-col {
      position: sticky;
      left: 0;
      z-index: 20;
      background-color: #131720;
    }

    .sticky-header {
      position: sticky;
      top: 0;
      z-index: 30;
      background-color: #1a1f2c;
    }

    /* Ratio bar styling */
    .ratio-bar {
      height: 6px;
      border-radius: 3px;
      display: flex;
      overflow: hidden;
      background-color: #232938;
    }

    .badge-up {
      color: #00e676;
    }

    .badge-down {
      color: #ff4d4d;
    }
  </style>
</head>
<body class="bg-cotBg text-cotText font-sans min-h-screen flex flex-col antialiased selection:bg-cotBlue selection:text-white">

  <!-- Top Navigation / Branding Header -->
  <header class="bg-cotCard border-b border-cotBorder px-4 py-3 sticky top-0 z-40 shadow-xl">
    <div class="max-w-[1920px] mx-auto flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      
      <!-- Brand Title & Date -->
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-lg bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400 font-bold text-lg shadow-inner">
          <i class="fa-solid font-bold fa-chart-line"></i>
        </div>
        <div>
          <h1 class="text-base sm:text-lg font-extrabold tracking-wide text-white uppercase flex items-center gap-2">
            COT REPORT <span class="text-cotMuted font-normal">•</span> <span class="text-blue-400">WEEKLY SUMMARY</span>
          </h1>
          <p class="text-xs text-cotMuted flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-cotGreen animate-pulse"></span>
            CFTC Disaggregated & Legacy Futures • Latest: <span id="reportDate" class="font-semibold text-cotText">Sep 08, 2026</span>
          </p>
        </div>
      </div>

      <!-- Quick Action Controls & Presets -->
      <div class="flex flex-wrap items-center gap-2 sm:gap-3 text-xs">
        <!-- Search Input -->
        <div class="relative flex-grow sm:flex-grow-0 min-w-[180px]">
          <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-cotMuted"></i>
          <input type="text" id="searchInput" placeholder="Search contract (EUR, Gold, BTC)..." 
                 class="w-full bg-cotBg border border-cotBorder rounded-lg pl-9 pr-3 py-1.5 text-xs text-cotText focus:outline-none focus:border-cotBlue transition-colors" />
        </div>

        <!-- Presets Buttons -->
        <div class="flex items-center bg-cotBg border border-cotBorder rounded-lg p-0.5">
          <button onclick="setPreset('full')" id="preset-full" class="px-2.5 py-1 rounded-md text-cotText font-medium bg-cotCard transition-all">Full View</button>
          <button onclick="setPreset('spec')" id="preset-spec" class="px-2.5 py-1 rounded-md text-cotMuted hover:text-cotText transition-all">Speculators Only</button>
          <button onclick="setPreset('hedger')" id="preset-hedger" class="px-2.5 py-1 rounded-md text-cotMuted hover:text-cotText transition-all">Hedgers Only</button>
        </div>

        <!-- Category Filter Dropdown -->
        <select id="categoryFilter" class="bg-cotBg border border-cotBorder text-cotText rounded-lg px-3 py-1.5 focus:outline-none focus:border-cotBlue cursor-pointer">
          <option value="ALL">All Categories</option>
          <option value="CURRENCIES">Major Currencies</option>
          <option value="CRYPTO">Cryptocurrencies</option>
          <option value="COMMODITIES">Commodities</option>
          <option value="INDICES">Equity Indices</option>
        </select>

        <!-- Customizer Drawer Toggle -->
        <button onclick="toggleSettingsModal()" class="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-3 py-1.5 rounded-lg transition-colors flex items-center gap-2 shadow-lg shadow-blue-600/20">
          <i class="fa-solid fa-sliders"></i>
          <span>Customize View</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Main Content Area -->
  <main class="flex-1 max-w-[1920px] w-full mx-auto p-2 sm:p-4 space-y-4">
    
    <!-- Top Stats / Highlight Bar -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
      <div class="bg-cotCard border border-cotBorder rounded-xl p-3 flex items-center justify-between">
        <div>
          <div class="text-cotMuted uppercase font-semibold text-[10px] tracking-wider">Most Bullish Speculators</div>
          <div class="text-sm font-bold text-cotGreen flex items-center gap-1 mt-0.5">
            <i class="fa-solid fa-arrow-trend-up"></i> Japanese Yen (6J)
          </div>
        </div>
        <span class="px-2 py-1 rounded-md bg-cotGreenBg text-cotGreen font-bold">+103,023 Net</span>
      </div>

      <div class="bg-cotCard border border-cotBorder rounded-xl p-3 flex items-center justify-between">
        <div>
          <div class="text-cotMuted uppercase font-semibold text-[10px] tracking-wider">Most Bearish Speculators</div>
          <div class="text-sm font-bold text-cotRed flex items-center gap-1 mt-0.5">
            <i class="fa-solid fa-arrow-trend-down"></i> Ethereum (ETH)
          </div>
        </div>
        <span class="px-2 py-1 rounded-md bg-cotRedBg text-cotRed font-bold">-164,704 Net</span>
      </div>

      <div class="bg-cotCard border border-cotBorder rounded-xl p-3 flex items-center justify-between">
        <div>
          <div class="text-cotMuted uppercase font-semibold text-[10px] tracking-wider">Highest Open Interest</div>
          <div class="text-sm font-bold text-cotText mt-0.5">Ethereum (ETH)</div>
        </div>
        <span class="px-2 py-1 rounded-md bg-cotBorder text-cotText font-bold">13,294,407</span>
      </div>

      <div class="bg-cotCard border border-cotBorder rounded-xl p-3 flex items-center justify-between">
        <div>
          <div class="text-cotMuted uppercase font-semibold text-[10px] tracking-wider">Total Active Contracts</div>
          <div class="text-sm font-bold text-blue-400 mt-0.5" id="contractCount">14 Contracts</div>
        </div>
        <div class="text-cotMuted text-xs"><i class="fa-solid fa-database"></i> Live CFTC Data</div>
      </div>
    </div>

    <!-- Main Dynamic COT Table -->
    <div class="bg-cotCard border border-cotBorder rounded-xl shadow-2xl overflow-hidden">
      <div class="overflow-x-auto max-h-[calc(100vh-220px)]">
        <table class="w-full text-left text-xs cot-table" id="cotMainTable">
          
          <!-- TABLE HEADER -->
          <thead>
            <!-- Group Header Tier 1 -->
            <tr class="sticky-header text-[11px] uppercase tracking-wider text-cotText font-bold border-b border-cotBorder">
              
              <!-- Sticky Left Header -->
              <th scope="col" class="sticky-col py-3 px-4 bg-cotHeader min-w-[200px] border-r border-cotBorder">
                CONTRACTS
              </th>

              <!-- Non-Commercial Header -->
              <th scope="col" id="th-group-noncomm" colspan="4" class="py-2.5 px-3 bg-[#131b2e] text-blue-400 border-r border-cotBorder text-center">
                <div class="flex items-center justify-center gap-2">
                  <i class="fa-solid fa-users"></i>
                  <span>NON-COMMERCIAL • LARGE SPECULATORS</span>
                </div>
              </th>

              <!-- Commercial Header -->
              <th scope="col" id="th-group-comm" colspan="4" class="py-2.5 px-3 bg-[#11241c] text-cotGreen border-r border-cotBorder text-center">
                <div class="flex items-center justify-center gap-2">
                  <i class="fa-solid fa-building-columns"></i>
                  <span>COMMERCIAL • HEDGERS / INSTITUTIONAL</span>
                </div>
              </th>

              <!-- Non-Reportable Header -->
              <th scope="col" id="th-group-nonrep" colspan="4" class="py-2.5 px-3 bg-[#2b171a] text-cotRed border-r border-cotBorder text-center">
                <div class="flex items-center justify-center gap-2">
                  <i class="fa-solid fa-user-group"></i>
                  <span>NON-REPORTABLE • SMALL SPECULATORS</span>
                </div>
              </th>

              <!-- Open Interest Header -->
              <th scope="col" id="th-group-oi" class="py-2.5 px-4 bg-[#1e2330] text-cotMuted text-right min-w-[120px]">
                OPEN INTEREST
              </th>
            </tr>

            <!-- Sub Columns Tier 2 -->
            <tr class="bg-cotHeader text-[10px] uppercase tracking-wider text-cotMuted font-semibold border-b border-cotBorder text-center select-none">
              
              <th scope="col" class="sticky-col py-2 px-4 text-left bg-cotHeader border-r border-cotBorder">
                Asset Name / Ticker
              </th>

              <!-- Non-Comm Columns -->
              <th scope="col" class="col-nc-net py-2 px-3 border-r border-cotBorder/50 w-[110px]">Net Positions</th>
              <th scope="col" class="col-nc-long py-2 px-3 border-r border-cotBorder/50 w-[90px] text-cotGreen">Long</th>
              <th scope="col" class="col-nc-short py-2 px-3 border-r border-cotBorder/50 w-[90px] text-cotRed">Short</th>
              <th scope="col" class="col-nc-ratio py-2 px-3 border-r border-cotBorder w-[120px]">Long vs Short</th>

              <!-- Comm Columns -->
              <th scope="col" class="col-c-net py-2 px-3 border-r border-cotBorder/50 w-[110px]">Net Positions</th>
              <th scope="col" class="col-c-long py-2 px-3 border-r border-cotBorder/50 w-[90px] text-cotGreen">Long</th>
              <th scope="col" class="col-c-short py-2 px-3 border-r border-cotBorder/50 w-[90px] text-cotRed">Short</th>
              <th scope="col" class="col-c-ratio py-2 px-3 border-r border-cotBorder w-[120px]">Long vs Short</th>

              <!-- Non-Rep Columns -->
              <th scope="col" class="col-nr-net py-2 px-3 border-r border-cotBorder/50 w-[110px]">Net Positions</th>
              <th scope="col" class="col-nr-long py-2 px-3 border-r border-cotBorder/50 w-[90px] text-cotGreen">Long</th>
              <th scope="col" class="col-nr-short py-2 px-3 border-r border-cotBorder/50 w-[90px] text-cotRed">Short</th>
              <th scope="col" class="col-nr-ratio py-2 px-3 border-r border-cotBorder w-[120px]">Long vs Short</th>

              <!-- Open Interest -->
              <th scope="col" class="col-oi py-2 px-4 text-right">Total Contracts</th>
            </tr>
          </thead>

          <!-- TABLE BODY (DYNAMICALLY POPULATED) -->
          <tbody id="cotTableBody" class="divide-y divide-cotBorder/40">
            <!-- Data Rows inserted via JavaScript -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- CUSTOMIZATION SETTINGS MODAL -->
  <div id="settingsModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-cotCard border border-cotBorder rounded-2xl w-full max-w-lg p-6 shadow-2xl space-y-5">
      
      <div class="flex items-center justify-between border-b border-cotBorder pb-3">
        <h3 class="text-lg font-bold text-white flex items-center gap-2">
          <i class="fa-solid fa-sliders text-blue-400"></i>
          <span>Customize Dashboard Columns</span>
        </h3>
        <button onclick="toggleSettingsModal()" class="text-cotMuted hover:text-white text-lg px-2">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Visibility Toggles -->
      <div class="space-y-4 text-xs">
        <div>
          <label class="block font-semibold text-cotText mb-2 uppercase text-[11px] text-blue-400">Trader Groups to Show</label>
          <div class="grid grid-cols-2 gap-2">
            <label class="flex items-center space-x-2 bg-cotBg p-2.5 rounded-lg border border-cotBorder cursor-pointer">
              <input type="checkbox" id="toggle-noncomm" checked onchange="updateColumnVisibility()" class="rounded border-cotBorder text-blue-600 focus:ring-0">
              <span>Non-Commercial (Large Spec)</span>
            </label>

            <label class="flex items-center space-x-2 bg-cotBg p-2.5 rounded-lg border border-cotBorder cursor-pointer">
              <input type="checkbox" id="toggle-comm" checked onchange="updateColumnVisibility()" class="rounded border-cotBorder text-cotGreen focus:ring-0">
              <span>Commercial (Hedgers)</span>
            </label>

            <label class="flex items-center space-x-2 bg-cotBg p-2.5 rounded-lg border border-cotBorder cursor-pointer">
              <input type="checkbox" id="toggle-nonrep" checked onchange="updateColumnVisibility()" class="rounded border-cotBorder text-cotRed focus:ring-0">
              <span>Non-Reportable (Small Spec)</span>
            </label>

            <label class="flex items-center space-x-2 bg-cotBg p-2.5 rounded-lg border border-cotBorder cursor-pointer">
              <input type="checkbox" id="toggle-oi" checked onchange="updateColumnVisibility()" class="rounded border-cotBorder text-cotMuted focus:ring-0">
              <span>Open Interest Column</span>
            </label>
          </div>
        </div>

        <div>
          <label class="block font-semibold text-cotText mb-2 uppercase text-[11px] text-blue-400">Data Metrics</label>
          <div class="grid grid-cols-2 gap-2">
            <label class="flex items-center space-x-2 bg-cotBg p-2.5 rounded-lg border border-cotBorder cursor-pointer">
              <input type="checkbox" id="toggle-ratio" checked onchange="updateColumnVisibility()" class="rounded border-cotBorder text-blue-600 focus:ring-0">
              <span>Visual Ratio Bars (L vs S)</span>
            </label>

            <label class="flex items-center space-x-2 bg-cotBg p-2.5 rounded-lg border border-cotBorder cursor-pointer">
              <input type="checkbox" id="toggle-deltas" checked onchange="renderTable()" class="rounded border-cotBorder text-blue-600 focus:ring-0">
              <span>Show Weekly Changes (+/-)</span>
            </label>
          </div>
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-3 border-t border-cotBorder">
        <button onclick="toggleSettingsModal()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition-colors">
          Apply Preferences
        </button>
      </div>

    </div>
  </div>

  <!-- HISTORICAL CHART MODAL -->
  <div id="chartModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-cotCard border border-cotBorder rounded-2xl w-full max-w-4xl p-6 shadow-2xl space-y-4">
      
      <div class="flex items-center justify-between border-b border-cotBorder pb-3">
        <div>
          <h3 id="chartModalTitle" class="text-lg font-bold text-white flex items-center gap-2">
            <!-- Dynamic Asset Title -->
          </h3>
          <p class="text-xs text-cotMuted">Historical COT Net Positions Trend (Multi-Week)</p>
        </div>
        <button onclick="closeChartModal()" class="text-cotMuted hover:text-white text-lg px-2">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Plotly Container -->
      <div id="plotlyChartContainer" class="w-full h-[400px] bg-cotBg rounded-xl p-2"></div>

    </div>
  </div>

  <script>
    // --- MOCK DATA DATASET (REALISTIC COT VALUES MATCHING USER REFERENCE IMAGE) ---
    const cotDataset = [
      {
        category: "CURRENCIES",
        categoryName: "MAJOR CURRENCIES",
        items: [
          {
            name: "NEW ZEALAND DOLLAR",
            code: "6N",
            pinned: false,
            ncNet: 6232, ncNetChange: 14253, ncNetChangePct: 177.7, ncLong: 26110, ncLongChange: 14810, ncLongChangePct: 131.1, ncShort: 19878, ncShortChange: 557, ncShortChangePct: 2.9,
            cNet: -5635, cNetChange: -14211, cNetChangePct: -165.7, cLong: 87479, cLongChange: -2538, cLongChangePct: -2.8, cShort: 93114, cShortChange: 11673, cShortChangePct: 14.3,
            nrNet: -597, nrNetChange: -42, nrNetChangePct: -7.6, nrLong: 4520, nrLongChange: 181, nrLongChangePct: 4.2, nrShort: 5117, nrShortChange: 223, nrShortChangePct: 4.6,
            oi: 125978, oiChange: 18704
          },
          {
            name: "BRITISH POUND STERLING",
            code: "6B",
            pinned: false,
            ncNet: -58836, ncNetChange: -9261, ncNetChangePct: -18.7, ncLong: 73520, ncLongChange: -11866, ncLongChangePct: -13.9, ncShort: 132356, ncShortChange: -2605, ncShortChangePct: -1.9,
            cNet: 57102, cNetChange: 11299, cNetChangePct: 24.7, cLong: 205647, cLongChange: 10184, cLongChangePct: 5.2, cShort: 148545, cShortChange: -1115, cShortChangePct: -0.7,
            nrNet: 1734, nrNetChange: -2038, nrNetChangePct: -54.0, nrLong: 31683, nrLongChange: -106, nrLongChangePct: -0.3, nrShort: 29949, nrShortChange: 1932, nrShortChangePct: 6.9,
            oi: 318608, oiChange: 647
          },
          {
            name: "SWISS FRANC",
            code: "6S",
            pinned: false,
            ncNet: -29985, ncNetChange: -7109, ncNetChangePct: -31.1, ncLong: 17273, ncLongChange: -2639, ncLongChangePct: -13.3, ncShort: 47258, ncShortChange: 4470, ncShortChangePct: 10.4,
            cNet: 41504, cNetChange: 5416, cNetChangePct: 15.0, cLong: 112612, cLongChange: 24372, cLongChangePct: 27.6, cShort: 71108, cShortChange: 18956, cShortChangePct: 36.3,
            nrNet: -11519, nrNetChange: 1693, nrNetChangePct: 12.8, nrLong: 12822, nrLongChange: 1687, nrLongChangePct: 15.2, nrShort: 24341, nrShortChange: -6, nrShortChangePct: 0.0,
            oi: 153683, oiChange: 16721
          },
          {
            name: "JAPANESE YEN",
            code: "6J",
            pinned: true,
            ncNet: 10796, ncNetChange: 103023, ncNetChangePct: 111.7, ncLong: 178791, ncLongChange: 61622, ncLongChangePct: 52.6, ncShort: 167995, ncShortChange: -41401, ncShortChangePct: -19.8,
            cNet: -14041, cNetChange: -111602, cNetChangePct: -114.4, cLong: 249469, cLongChange: 24280, cLongChangePct: 10.8, cShort: 263510, cShortChange: 135882, cShortChangePct: 106.5,
            nrNet: 3245, nrNetChange: 8579, nrNetChangePct: 160.8, nrLong: 42640, nrLongChange: 9417, nrLongChangePct: 28.3, nrShort: 39395, nrShortChange: 838, nrShortChangePct: 2.2,
            oi: 499635, oiChange: 87753
          },
          {
            name: "CANADIAN DOLLAR",
            code: "6C",
            pinned: false,
            ncNet: -70499, ncNetChange: 37644, ncNetChangePct: 34.8, ncLong: 54444, ncLongChange: 18182, ncLongChangePct: 50.1, ncShort: 124943, ncShortChange: -19462, ncShortChangePct: -13.5,
            cNet: 74429, cNetChange: -40853, cNetChangePct: -35.4, cLong: 244052, cLongChange: -22829, cLongChangePct: -8.6, cShort: 169623, cShortChange: 18024, cShortChangePct: 11.9,
            nrNet: -3930, nrNetChange: 3209, nrNetChangePct: 45.0, nrLong: 29559, nrLongChange: 3211, nrLongChangePct: 12.2, nrShort: 33489, nrShortChange: 2, nrShortChangePct: 0.0,
            oi: 334861, oiChange: 61
          },
          {
            name: "AUSTRALIAN DOLLAR",
            code: "6A",
            pinned: false,
            ncNet: -34870, ncNetChange: 4536, ncNetChangePct: 11.5, ncLong: 120532, ncLongChange: 6427, ncLongChangePct: 5.6, ncShort: 155402, ncShortChange: 1891, ncShortChangePct: 1.2,
            cNet: 15684, cNetChange: -3126, cNetChangePct: -16.6, cLong: 271564, cLongChange: 36412, cLongChangePct: 15.5, cShort: 255880, cShortChange: 39538, cShortChangePct: 18.3,
            nrNet: 19186, nrNetChange: -1410, nrNetChangePct: -6.8, nrLong: 37079, nrLongChange: 839, nrLongChangePct: 2.3, nrShort: 17893, nrShortChange: 2249, nrShortChangePct: 14.4,
            oi: 455468, oiChange: 63790
          },
          {
            name: "EURO FX",
            code: "6E",
            pinned: true,
            ncNet: -42616, ncNetChange: -17691, ncNetChangePct: -71.0, ncLong: 198509, ncLongChange: -4968, ncLongChangePct: -2.4, ncShort: 241125, ncShortChange: 12723, ncShortChangePct: 5.6,
            cNet: 6730, cNetChange: 15457, cNetChangePct: 177.1, cLong: 593162, cLongChange: 59242, cLongChangePct: 11.1, cShort: 586432, cShortChange: 43785, cShortChangePct: 8.1,
            nrNet: 35886, nrNetChange: 2234, nrNetChangePct: 6.6, nrLong: 92781, nrLongChange: 7111, nrLongChangePct: 8.3, nrShort: 56895, nrShortChange: 4877, nrShortChangePct: 9.4,
            oi: 942464, oiChange: 77032
          },
          {
            name: "U.S. DOLLAR INDEX",
            code: "DX",
            pinned: false,
            ncNet: 17604, ncNetChange: 579, ncNetChangePct: 3.4, ncLong: 28407, ncLongChange: 167, ncLongChangePct: 0.6, ncShort: 10803, ncShortChange: -412, ncShortChangePct: -3.7,
            cNet: -19188, cNetChange: -464, cNetChangePct: -2.5, cLong: 18620, cLongChange: 1850, cLongChangePct: 11.0, cShort: 37808, cShortChange: 2317, cShortChangePct: 6.5,
            nrNet: 1584, nrNetChange: -115, nrNetChangePct: -6.8, nrLong: 3246, nrLongChange: -179, nrLongChangePct: -5.2, nrShort: 1662, nrShortChange: -64, nrShortChangePct: -3.7,
            oi: 57858, oiChange: 7838
          }
        ]
      },
      {
        category: "CRYPTO",
        categoryName: "CRYPTOCURRENCIES",
        items: [
          {
            name: "BITCOIN",
            code: "BTC",
            pinned: true,
            ncNet: 1524, ncNetChange: 821, ncNetChangePct: 116.8, ncLong: 17600, ncLongChange: 1070, ncLongChangePct: 6.5, ncShort: 16076, ncShortChange: 249, ncShortChangePct: 1.6,
            cNet: -2061, cNetChange: -984, cNetChangePct: -91.4, cLong: 64, cLongChange: -359, cLongChangePct: -84.9, cShort: 2125, cShortChange: 625, cShortChangePct: 41.7,
            nrNet: 537, nrNetChange: 163, nrNetChangePct: 43.6, nrLong: 1273, nrLongChange: 86, nrLongChangePct: 7.2, nrShort: 736, nrShortChange: -77, nrShortChangePct: -9.5,
            oi: 21083, oiChange: 1386
          },
          {
            name: "ETHEREUM",
            code: "ETH",
            pinned: false,
            ncNet: -3103337, ncNetChange: -164704, ncNetChangePct: -5.6, ncLong: 1262856, ncLongChange: -31968, ncLongChangePct: -2.5, ncShort: 4366193, ncShortChange: 132736, ncShortChangePct: 3.1,
            cNet: 3101838, cNetChange: 163939, cNetChangePct: 5.6, cLong: 9345044, cLongChange: 188436, cLongChangePct: 2.1, cShort: 6243206, cShortChange: 24497, cShortChangePct: 0.4,
            nrNet: 1499, nrNetChange: 765, nrNetChangePct: 104.2, nrLong: 78805, nrLongChange: 11899, nrLongChangePct: 17.8, nrShort: 77306, nrShortChange: 11134, nrShortChangePct: 16.8,
            oi: 13294407, oiChange: 218718
          }
        ]
      },
      {
        category: "COMMODITIES",
        categoryName: "COMMODITIES & METALS",
        items: [
          {
            name: "GOLD",
            code: "GC",
            pinned: true,
            ncNet: 245100, ncNetChange: 12500, ncNetChangePct: 5.4, ncLong: 298400, ncLongChange: 9800, ncLongChangePct: 3.4, ncShort: 53300, ncShortChange: -2700, ncShortChangePct: -4.8,
            cNet: -278500, cNetChange: -14100, cNetChangePct: -5.3, cLong: 112000, cLongChange: 3100, cLongChangePct: 2.8, cShort: 390500, cShortChange: 17200, cShortChangePct: 4.6,
            nrNet: 33400, nrNetChange: 1600, nrNetChangePct: 5.0, nrLong: 51200, nrLongChange: 2100, nrLongChangePct: 4.3, nrShort: 17800, nrShortChange: 500, nrShortChangePct: 2.9,
            oi: 512300, oiChange: 24100
          },
          {
            name: "CRUDE OIL",
            code: "CL",
            pinned: false,
            ncNet: 182400, ncNetChange: -8400, ncNetChangePct: -4.4, ncLong: 265100, ncLongChange: -5200, ncLongChangePct: -1.9, ncShort: 82700, ncShortChange: 3200, ncShortChangePct: 4.0,
            cNet: -198200, cNetChange: 9100, cNetChangePct: 4.4, cLong: 310500, cLongChange: 12400, cLongChangePct: 4.2, cShort: 508700, cShortChange: 3300, cShortChangePct: 0.7,
            nrNet: 15800, nrNetChange: -700, nrNetChangePct: -4.2, nrLong: 32100, nrLongChange: 400, nrLongChangePct: 1.3, nrShort: 16300, nrShortChange: 1100, nrShortChangePct: 7.2,
            oi: 1420800, oiChange: -12500
          }
        ]
      }
    ];

    // --- STATE MANAGEMENT ---
    let collapsedCategories = {};

    // --- HELPER FUNCTIONS FOR FORMATTING ---
    function formatNum(num) {
      if (num === undefined || num === null) return '0';
      return num.toLocaleString('en-US');
    }

    function formatDelta(change, changePct) {
      if (!change && change === 0) return '';
      const isPos = change > 0;
      const sign = isPos ? '+' : '';
      const colorClass = isPos ? 'badge-up' : 'badge-down';
      const arrow = isPos ? '↑' : '↓';
      return `<div class="text-[10px] font-medium ${colorClass} mt-0.5">
                ${arrow} ${sign}${formatNum(change)} (${sign}${changePct}%)
              </div>`;
    }

    function renderRatioBar(long, short) {
      const total = long + short;
      if (total === 0) return '<div class="ratio-bar"></div>';
      const longPct = ((long / total) * 100).toFixed(1);
      const shortPct = (100 - longPct).toFixed(1);

      return `
        <div class="space-y-1">
          <div class="ratio-bar">
            <div style="width: ${longPct}%" class="bg-cotGreen h-full"></div>
            <div style="width: ${shortPct}%" class="bg-cotRed h-full"></div>
          </div>
          <div class="flex justify-between text-[9px] font-semibold text-cotMuted">
            <span class="text-cotGreen">${longPct}%</span>
            <span class="text-cotRed">${shortPct}%</span>
          </div>
        </div>
      `;
    }

    // --- MAIN RENDER TABLE FUNCTION ---
    function renderTable() {
      const tbody = document.getElementById('cotTableBody');
      const searchVal = document.getElementById('searchInput').value.toLowerCase().trim();
      const catVal = document.getElementById('categoryFilter').value;
      const showDeltas = document.getElementById('toggle-deltas').checked;

      let html = '';
      let totalCount = 0;

      cotDataset.forEach((catGroup) => {
        // Filter by Category Dropdown
        if (catVal !== 'ALL' && catGroup.category !== catVal) return;

        // Filter items by search
        const filteredItems = catGroup.items.filter(item => 
          item.name.toLowerCase().includes(searchVal) || 
          item.code.toLowerCase().includes(searchVal)
        );

        if (filteredItems.length === 0) return;

        totalCount += filteredItems.length;
        const isCollapsed = collapsedCategories[catGroup.category] || false;
        const chevronIcon = isCollapsed ? 'fa-chevron-right' : 'fa-chevron-down';

        // Render Category Header Row
        html += `
          <tr class="bg-cotHeader/80 text-cotMuted font-bold text-[11px] border-y border-cotBorder hover:bg-cotHeader cursor-pointer select-none"
              onclick="toggleCategory('${catGroup.category}')">
            <td colspan="14" class="py-2 px-4 sticky-col bg-cotHeader">
              <div class="flex items-center gap-2">
                <i class="fa-solid ${chevronIcon} text-cotMuted text-[10px]"></i>
                <span class="text-cotText tracking-wider">${catGroup.categoryName}</span>
                <span class="px-2 py-0.5 rounded-full bg-cotBg text-[10px] text-cotMuted font-normal border border-cotBorder">
                  ${filteredItems.length} contracts
                </span>
              </div>
            </td>
          </tr>
        `;

        if (isCollapsed) return;

        // Render Items inside Category
        filteredItems.forEach((item) => {
          const pinClass = item.pinned ? 'text-cotYellow' : 'text-cotMuted hover:text-white';
          const netNcClass = item.ncNet >= 0 ? 'text-cotGreen' : 'text-cotRed';
          const netCClass = item.cNet >= 0 ? 'text-cotGreen' : 'text-cotRed';
          const netNrClass = item.nrNet >= 0 ? 'text-cotGreen' : 'text-cotRed';

          html += `
            <tr class="hover:bg-cotHeader/40 transition-colors border-b border-cotBorder/30 text-center cursor-pointer" onclick="openChartModal('${item.name}', '${item.code}')">
              
              <!-- Sticky Contract Name Cell -->
              <td class="sticky-col py-3 px-4 text-left font-bold text-white border-r border-cotBorder bg-cotCard">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <button onclick="event.stopPropagation(); togglePin('${item.code}')" class="${pinClass} transition-colors">
                      <i class="fa-solid fa-star text-xs"></i>
                    </button>
                    <div>
                      <div class="text-xs font-bold text-white tracking-wide">${item.name}</div>
                      <div class="text-[10px] text-cotMuted font-mono italic">${item.code}</div>
                    </div>
                  </div>
                  <i class="fa-solid fa-chart-line text-cotMuted/40 hover:text-blue-400 text-xs transition-colors"></i>
                </div>
              </td>

              <!-- NON-COMMERCIAL -->
              <td class="col-nc-net py-2.5 px-3 border-r border-cotBorder/50 font-bold ${netNcClass}">
                ${formatNum(item.ncNet)}
                ${showDeltas ? formatDelta(item.ncNetChange, item.ncNetChangePct) : ''}
              </td>
              <td class="col-nc-long py-2.5 px-3 border-r border-cotBorder/50 font-mono text-cotText">
                ${formatNum(item.ncLong)}
                ${showDeltas ? formatDelta(item.ncLongChange, item.ncLongChangePct) : ''}
              </td>
              <td class="col-nc-short py-2.5 px-3 border-r border-cotBorder/50 font-mono text-cotText">
                ${formatNum(item.ncShort)}
                ${showDeltas ? formatDelta(item.ncShortChange, item.ncShortChangePct) : ''}
              </td>
              <td class="col-nc-ratio py-2.5 px-3 border-r border-cotBorder">
                ${renderRatioBar(item.ncLong, item.ncShort)}
              </td>

              <!-- COMMERCIAL -->
              <td class="col-c-net py-2.5 px-3 border-r border-cotBorder/50 font-bold ${netCClass}">
                ${formatNum(item.cNet)}
                ${showDeltas ? formatDelta(item.cNetChange, item.cNetChangePct) : ''}
              </td>
              <td class="col-c-long py-2.5 px-3 border-r border-cotBorder/50 font-mono text-cotText">
                ${formatNum(item.cLong)}
                ${showDeltas ? formatDelta(item.cLongChange, item.cLongChangePct) : ''}
              </td>
              <td class="col-c-short py-2.5 px-3 border-r border-cotBorder/50 font-mono text-cotText">
                ${formatNum(item.cShort)}
                ${showDeltas ? formatDelta(item.cShortChange, item.cShortChangePct) : ''}
              </td>
              <td class="col-c-ratio py-2.5 px-3 border-r border-cotBorder">
                ${renderRatioBar(item.cLong, item.cShort)}
              </td>

              <!-- NON-REPORTABLE -->
              <td class="col-nr-net py-2.5 px-3 border-r border-cotBorder/50 font-bold ${netNrClass}">
                ${formatNum(item.nrNet)}
                ${showDeltas ? formatDelta(item.nrNetChange, item.nrNetChangePct) : ''}
              </td>
              <td class="col-nr-long py-2.5 px-3 border-r border-cotBorder/50 font-mono text-cotText">
                ${formatNum(item.nrLong)}
                ${showDeltas ? formatDelta(item.nrLongChange, item.nrLongChangePct) : ''}
              </td>
              <td class="col-nr-short py-2.5 px-3 border-r border-cotBorder/50 font-mono text-cotText">
                ${formatNum(item.nrShort)}
                ${showDeltas ? formatDelta(item.nrShortChange, item.nrShortChangePct) : ''}
              </td>
              <td class="col-nr-ratio py-2.5 px-3 border-r border-cotBorder">
                ${renderRatioBar(item.nrLong, item.nrShort)}
              </td>

              <!-- OPEN INTEREST -->
              <td class="col-oi py-2.5 px-4 text-right font-bold text-white font-mono">
                ${formatNum(item.oi)}
                ${showDeltas ? formatDelta(item.oiChange, ((item.oiChange/item.oi)*100).toFixed(1)) : ''}
              </td>
            </tr>
          `;
        });
      });

      tbody.innerHTML = html;
      document.getElementById('contractCount').innerText = `${totalCount} Contracts`;
      updateColumnVisibility();
    }

    // --- INTERACTION HANDLERS ---
    function toggleCategory(catKey) {
      collapsedCategories[catKey] = !collapsedCategories[catKey];
      renderTable();
    }

    function togglePin(code) {
      cotDataset.forEach(cat => {
        cat.items.forEach(item => {
          if (item.code === code) item.pinned = !item.pinned;
        });
      });
      renderTable();
    }

    function toggleSettingsModal() {
      const modal = document.getElementById('settingsModal');
      modal.classList.toggle('hidden');
    }

    // --- COLUMN VISIBILITY & PRESETS ---
    function updateColumnVisibility() {
      const showNC = document.getElementById('toggle-noncomm').checked;
      const showC = document.getElementById('toggle-comm').checked;
      const showNR = document.getElementById('toggle-nonrep').checked;
      const showOI = document.getElementById('toggle-oi').checked;
      const showRatio = document.getElementById('toggle-ratio').checked;

      // Group headers
      document.getElementById('th-group-noncomm').style.display = showNC ? '' : 'none';
      document.getElementById('th-group-comm').style.display = showC ? '' : 'none';
      document.getElementById('th-group-nonrep').style.display = showNR ? '' : 'none';
      document.getElementById('th-group-oi').style.display = showOI ? '' : 'none';

      // Specific columns
      const toggleClasses = (className, displayCondition) => {
        document.querySelectorAll('.' + className).forEach(el => {
          el.style.display = displayCondition ? '' : 'none';
        });
      };

      toggleClasses('col-nc-net', showNC);
      toggleClasses('col-nc-long', showNC);
      toggleClasses('col-nc-short', showNC);
      toggleClasses('col-nc-ratio', showNC && showRatio);

      toggleClasses('col-c-net', showC);
      toggleClasses('col-c-long', showC);
      toggleClasses('col-c-short', showC);
      toggleClasses('col-c-ratio', showC && showRatio);

      toggleClasses('col-nr-net', showNR);
      toggleClasses('col-nr-long', showNR);
      toggleClasses('col-nr-short', showNR);
      toggleClasses('col-nr-ratio', showNR && showRatio);

      toggleClasses('col-oi', showOI);
    }

    function setPreset(type) {
      document.querySelectorAll('[id^="preset-"]').forEach(btn => {
        btn.className = "px-2.5 py-1 rounded-md text-cotMuted hover:text-cotText transition-all";
      });

      document.getElementById(`preset-${type}`).className = "px-2.5 py-1 rounded-md text-cotText font-medium bg-cotCard transition-all";

      if (type === 'full') {
        document.getElementById('toggle-noncomm').checked = true;
        document.getElementById('toggle-comm').checked = true;
        document.getElementById('toggle-nonrep').checked = true;
        document.getElementById('toggle-oi').checked = true;
      } else if (type === 'spec') {
        document.getElementById('toggle-noncomm').checked = true;
        document.getElementById('toggle-comm').checked = false;
        document.getElementById('toggle-nonrep').checked = true;
        document.getElementById('toggle-oi').checked = true;
      } else if (type === 'hedger') {
        document.getElementById('toggle-noncomm').checked = false;
        document.getElementById('toggle-comm').checked = true;
        document.getElementById('toggle-nonrep').checked = false;
        document.getElementById('toggle-oi').checked = true;
      }
      updateColumnVisibility();
    }

    // --- HISTORICAL PLOTLY CHART MODAL ---
    function openChartModal(name, code) {
      document.getElementById('chartModalTitle').innerHTML = `
        <span class="text-blue-400 font-bold">${name} (${code})</span>
      `;

      document.getElementById('chartModal').classList.remove('hidden');

      // Generate 12 weeks mock trend historical data
      const weeks = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'Latest'];
      const nonCommTrend = [-30000, -25000, -18000, -12000, -5000, 2000, 10000, 18000, 25000, 15000, -10000, -42616];
      const commTrend = [35000, 28000, 20000, 15000, 8000, -1000, -8000, -16000, -22000, -12000, 12000, 6730];

      const trace1 = {
        x: weeks,
        y: nonCommTrend,
        mode: 'lines+markers',
        name: 'Large Speculators (Net)',
        line: { color: '#00e676', width: 3 }
      };

      const trace2 = {
        x: weeks,
        y: commTrend,
        mode: 'lines+markers',
        name: 'Commercial Hedgers (Net)',
        line: { color: '#ff4d4d', width: 3 }
      };

      const layout = {
        paper_bgcolor: '#0b0d11',
        plot_bgcolor: '#0b0d11',
        margin: { l: 50, r: 30, t: 30, b: 40 },
        xaxis: { gridcolor: '#232938', color: '#94a3b8' },
        yaxis: { gridcolor: '#232938', color: '#94a3b8' },
        legend: { font: { color: '#e2e8f0' }, orientation: 'h', y: 1.1 },
        hovermode: 'x unified'
      };

      Plotly.newPlot('plotlyChartContainer', [trace1, trace2], layout, { responsive: true });
    }

    function closeChartModal() {
      document.getElementById('chartModal').classList.add('hidden');
    }

    // --- EVENT LISTENERS INITIALIZATION ---
    document.getElementById('searchInput').addEventListener('input', renderTable);
    document.getElementById('categoryFilter').addEventListener('change', renderTable);

    // Initial render call on page load
    window.addEventListener('DOMContentLoaded', () => {
      renderTable();
    });
  </script>
</body>
</html>
