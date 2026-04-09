# 🍬 Nassau Candy — Profitability Intelligence Dashboard

Big-4 grade Streamlit analytics dashboard for Nassau Candy Distributor.

## Quick Start

### 1. Install dependencies
```bash
pip install streamlit plotly pandas numpy
```

### 2. Place your data file
Make sure `NassauCandy.csv` is in the **same folder** as `nassau_candy_dashboard.py`.

### 3. Run the dashboard
```bash
streamlit run nassau_candy_dashboard.py
```

The app will open automatically at **http://localhost:8501**

---

## Dashboard Modules

| Tab | Content |
|-----|---------|
| 📊 Executive Overview | KPI cards, revenue/margin trend, division profit mix, product leaderboard, regional scorecard |
| 🏷️ Product Deep Dive | Full product matrix, Sales vs GP scatter, quadrant chart, margin volatility over time |
| 🏢 Division & Region | Division KPI cards, margin distribution boxplots, state-level GP bars, heatmap |
| 🎯 Pareto & Cost Diagnostics | Revenue & profit Pareto charts, cost diagnostics, risk flags, profitability waterfall bridge |

## Sidebar Controls

- **Date Range** — filter orders by order date
- **Division** — filter by Chocolate / Sugar / Other
- **Region** — filter by Atlantic / Gulf / Interior / Pacific
- **Ship Mode** — filter by shipping method
- **Margin Risk Threshold** — set the % below which products are flagged as "at risk"
- **Product Search** — search for specific product names

---

*Powered by Streamlit · Plotly · Pandas*
