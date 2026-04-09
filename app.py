"""
Nassau Candy Distributor — Product Line Profitability & Margin Performance Dashboard
Big-4 Grade Analytics · Built with Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy | Profitability Intelligence",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL THEME  (inject CSS)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Font import ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700;900&display=swap');

/* ── Root palette ── */
:root {
    --bg:       #0D0F14;
    --surface:  #141720;
    --card:     #1A1E2B;
    --border:   #252A3A;
    --accent:   #F5A623;
    --accent2:  #E8547A;
    --accent3:  #4ECDC4;
    --accent4:  #A78BFA;
    --text:     #E8EAF0;
    --muted:    #7B82A0;
    --green:    #34D399;
    --red:      #F87171;
}

/* ── App shell ── */
.stApp { background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; }
.stApp > header { background: transparent !important; }
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    transition: border-color .2s;
}
div[data-testid="metric-container"]:hover { border-color: var(--accent); }
div[data-testid="metric-container"] label { color: var(--muted) !important; font-size: 11px !important; letter-spacing: .08em; text-transform: uppercase; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--text) !important; font-size: 26px !important; font-weight: 700 !important; }
div[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 12px !important; }

/* ── Section headers ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 900;
    color: var(--text);
    margin: 8px 0 4px;
    letter-spacing: -.01em;
}
.section-sub {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 18px;
}

/* ── Chart cards ── */
.chart-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
}

/* ── Pill badges ── */
.pill-green { background: #052e16; color: var(--green); border: 1px solid var(--green); border-radius: 99px; padding: 2px 10px; font-size: 11px; font-weight: 600; }
.pill-red   { background: #2d0a0a; color: var(--red);   border: 1px solid var(--red);   border-radius: 99px; padding: 2px 10px; font-size: 11px; font-weight: 600; }
.pill-amber { background: #2d1a00; color: var(--accent); border: 1px solid var(--accent); border-radius: 99px; padding: 2px 10px; font-size: 11px; font-weight: 600; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: var(--surface); border-radius: 10px; padding: 4px; gap: 2px; }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; color: var(--muted); font-weight: 500; padding: 8px 18px; }
.stTabs [aria-selected="true"] { background: var(--card) !important; color: var(--text) !important; }

/* ── Dataframe ── */
.stDataFrame { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }

/* ── Sidebar widgets ── */
.stSlider > div > div { background: var(--accent) !important; }
.stSelectbox > div > div { background: var(--card) !important; border-color: var(--border) !important; color: var(--text) !important; }
.stMultiSelect > div > div { background: var(--card) !important; border-color: var(--border) !important; }

/* ── Logo band ── */
.logo-band {
    display: flex; align-items: center; gap: 14px;
    background: linear-gradient(135deg, #1A1E2B 0%, #0D0F14 100%);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 24px;
}
.logo-icon { font-size: 40px; line-height:1; }
.logo-text { display: flex; flex-direction: column; }
.logo-name  { font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 900; color: var(--accent); }
.logo-tag   { font-size: 11px; color: var(--muted); letter-spacing: .12em; text-transform: uppercase; margin-top: 2px; }

/* ── Risk table cells ── */
.risk-high   { color: var(--red) !important; font-weight: 700; }
.risk-medium { color: var(--accent) !important; font-weight: 600; }
.risk-low    { color: var(--green) !important; font-weight: 600; }

/* ── KPI insight box ── */
.insight-box {
    background: linear-gradient(135deg, #1A1E2B, #141720);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 13px;
    color: var(--muted);
}
.insight-box b { color: var(--text); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("NassauCandy.csv")
    df.columns = df.columns.str.strip()
    df["Sales"]        = pd.to_numeric(df["Sales"], errors="coerce")
    df["Gross Profit"] = pd.to_numeric(df["Gross Profit"], errors="coerce")
    df["Cost"]         = pd.to_numeric(df["Cost"], errors="coerce")
    df["Units"]        = pd.to_numeric(df["Units"], errors="coerce")
    df = df.dropna(subset=["Sales", "Gross Profit", "Cost"])
    df = df[df["Sales"] > 0]
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True, errors="coerce")
    df["Gross Margin %"] = df["Gross Profit"] / df["Sales"] * 100
    df["Profit per Unit"] = df["Gross Profit"] / df["Units"].replace(0, np.nan)
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"]  = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df

df = load_data()

# ─────────────────────────────────────────────
#  CHART THEME  (shared Plotly layout)
# ─────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#7B82A0", size=11),
    title_font=dict(family="DM Sans", color="#E8EAF0", size=14),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#252A3A", borderwidth=1,
                font=dict(color="#E8EAF0")),
    margin=dict(t=40, b=20, l=10, r=10),
    xaxis=dict(gridcolor="#1D2030", zeroline=False, tickfont=dict(color="#7B82A0")),
    yaxis=dict(gridcolor="#1D2030", zeroline=False, tickfont=dict(color="#7B82A0")),
    colorway=["#F5A623", "#E8547A", "#4ECDC4", "#A78BFA", "#34D399", "#60A5FA"],
)

def apply_theme(fig, **kwargs):
    # Merge kwargs into a copy of CHART_LAYOUT so duplicate keys (e.g. 'legend',
    # 'xaxis', 'yaxis') are overridden rather than passed twice.
    layout = {**CHART_LAYOUT}
    for k, v in kwargs.items():
        if k in layout and isinstance(layout[k], dict) and isinstance(v, dict):
            layout[k] = {**layout[k], **v}   # deep-merge dicts
        else:
            layout[k] = v                     # scalar / new key: just override
    fig.update_layout(**layout)
    return fig

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:12px 0 18px;'>
      <div style='font-size:42px;'>🍬</div>
      <div style='font-family:"Playfair Display",serif;font-size:18px;color:#F5A623;font-weight:900;'>Nassau Candy</div>
      <div style='font-size:10px;color:#7B82A0;letter-spacing:.12em;text-transform:uppercase;margin-top:4px;'>Profitability Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📅 Date Range**")
    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    date_range = st.date_input("", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date,
                               label_visibility="collapsed")

    st.markdown("**🏷️ Division**")
    all_divisions = sorted(df["Division"].dropna().unique())
    sel_divisions = st.multiselect("", all_divisions, default=all_divisions,
                                   label_visibility="collapsed")

    st.markdown("**🗺️ Region**")
    all_regions = sorted(df["Region"].dropna().unique())
    sel_regions = st.multiselect("", all_regions, default=all_regions,
                                 label_visibility="collapsed")

    st.markdown("**📦 Ship Mode**")
    all_modes = sorted(df["Ship Mode"].dropna().unique())
    sel_modes = st.multiselect("", all_modes, default=all_modes,
                               label_visibility="collapsed")

    st.markdown("**⚠️ Margin Risk Threshold (%)**")
    margin_threshold = st.slider("", min_value=0, max_value=100, value=40,
                                 label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**🔍 Product Search**")
    product_search = st.text_input("", placeholder="e.g. Wonka Bar…",
                                   label_visibility="collapsed")

    st.markdown("---")
    st.caption("Nassau Candy Distributor · FY 2024–2025")

# ─────────────────────────────────────────────
#  FILTER DATA
# ─────────────────────────────────────────────
if len(date_range) == 2:
    start_d, end_d = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_d, end_d = df["Order Date"].min(), df["Order Date"].max()

mask = (
    df["Order Date"].between(start_d, end_d) &
    df["Division"].isin(sel_divisions) &
    df["Region"].isin(sel_regions) &
    df["Ship Mode"].isin(sel_modes)
)
if product_search:
    mask &= df["Product Name"].str.contains(product_search, case=False, na=False)

dff = df[mask].copy()

# ─────────────────────────────────────────────
#  AGGREGATIONS
# ─────────────────────────────────────────────
total_sales  = dff["Sales"].sum()
total_gp     = dff["Gross Profit"].sum()
total_cost   = dff["Cost"].sum()
total_units  = dff["Units"].sum()
overall_gm   = total_gp / total_sales * 100 if total_sales else 0
avg_ppu      = dff["Profit per Unit"].mean()

# Product level
prod_df = dff.groupby(["Product ID","Product Name","Division"]).agg(
    Sales=("Sales","sum"),
    GrossProfit=("Gross Profit","sum"),
    Cost=("Cost","sum"),
    Units=("Units","sum"),
    Orders=("Order ID","nunique"),
).reset_index()
prod_df["GM%"]         = prod_df["GrossProfit"] / prod_df["Sales"] * 100
prod_df["ProfitPerUnit"]= prod_df["GrossProfit"] / prod_df["Units"].replace(0,np.nan)
prod_df["RevShare%"]   = prod_df["Sales"]       / total_sales * 100
prod_df["ProfShare%"]  = prod_df["GrossProfit"] / total_gp   * 100
prod_df["MarginRisk"]  = np.where(prod_df["GM%"] < margin_threshold, "⚠️ At Risk", "✅ Healthy")

# Division level
div_df = dff.groupby("Division").agg(
    Sales=("Sales","sum"),
    GrossProfit=("Gross Profit","sum"),
    Cost=("Cost","sum"),
    Units=("Units","sum"),
).reset_index()
div_df["GM%"] = div_df["GrossProfit"] / div_df["Sales"] * 100

# Region level
reg_df = dff.groupby("Region").agg(
    Sales=("Sales","sum"),
    GrossProfit=("Gross Profit","sum"),
    Units=("Units","sum"),
).reset_index()
reg_df["GM%"] = reg_df["GrossProfit"] / reg_df["Sales"] * 100

# Monthly trend
month_df = dff.groupby("YearMonth").agg(
    Sales=("Sales","sum"),
    GrossProfit=("Gross Profit","sum"),
).reset_index().sort_values("YearMonth")
month_df["GM%"] = month_df["GrossProfit"] / month_df["Sales"] * 100

# State level (top 15)
state_df = dff.groupby("State/Province").agg(
    Sales=("Sales","sum"),
    GrossProfit=("Gross Profit","sum"),
    Units=("Units","sum"),
).reset_index().sort_values("GrossProfit", ascending=False).head(15)
state_df["GM%"] = state_df["GrossProfit"] / state_df["Sales"] * 100

# ─────────────────────────────────────────────
#  HEADER BAND
# ─────────────────────────────────────────────
st.markdown("""
<div class='logo-band'>
  <div class='logo-icon'>🍬</div>
  <div class='logo-text'>
    <div class='logo-name'>Nassau Candy Distributor</div>
    <div class='logo-tag'>Product Line Profitability &amp; Margin Performance · Executive Intelligence Dashboard</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Overview",
    "🏷️ Product Deep Dive",
    "🏢 Division & Region",
    "🎯 Pareto & Cost Diagnostics",
])

# ══════════════════════════════════════════════
#  TAB 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    # KPI row
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.metric("💰 Total Revenue",    f"${total_sales:,.0f}")
    with k2: st.metric("📈 Gross Profit",      f"${total_gp:,.0f}")
    with k3: st.metric("🎯 Overall Margin",    f"{overall_gm:.1f}%",
                        delta=f"{overall_gm - 60:.1f}pp vs 60% target")
    with k4: st.metric("📦 Total Units Sold",  f"{total_units:,.0f}")
    with k5: st.metric("💵 Profit / Unit",     f"${avg_ppu:.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Revenue trend + Division waterfall
    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("<div class='section-title'>Revenue & Margin Trend</div><div class='section-sub'>Monthly gross profit vs. revenue with rolling margin %</div>", unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=month_df["YearMonth"], y=month_df["Sales"],
            name="Revenue", marker_color="#252A3A", opacity=.9,
        ), secondary_y=False)
        fig.add_trace(go.Bar(
            x=month_df["YearMonth"], y=month_df["GrossProfit"],
            name="Gross Profit", marker_color="#F5A623", opacity=.9,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=month_df["YearMonth"], y=month_df["GM%"],
            name="Margin %", mode="lines+markers",
            line=dict(color="#4ECDC4", width=2.5),
            marker=dict(size=5),
        ), secondary_y=True)
        apply_theme(fig, barmode="overlay",
                    yaxis2=dict(gridcolor="rgba(0,0,0,0)", ticksuffix="%",
                                tickfont=dict(color="#4ECDC4")),
                    legend=dict(orientation="h", y=1.08))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Division Profit Mix</div><div class='section-sub'>Gross profit contribution by division</div>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=div_df["Division"],
            values=div_df["GrossProfit"],
            hole=.55,
            marker=dict(colors=["#F5A623","#E8547A","#4ECDC4","#A78BFA"],
                        line=dict(color="#0D0F14", width=2)),
            textinfo="label+percent",
            textfont=dict(color="#E8EAF0", size=12),
        ))
        apply_theme(fig2)
        fig2.update_layout(
            height=300,
            annotations=[dict(text=f"${total_gp/1000:.0f}K<br><span style='font-size:10px'>GP Total</span>",
                              x=.5, y=.5, showarrow=False, font=dict(size=16, color="#F5A623"))]
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Row 3: Margin by product (horizontal bar) + Region scorecard
    c3, c4 = st.columns([3, 2])

    with c3:
        st.markdown("<div class='section-title'>Product Margin Leaderboard</div><div class='section-sub'>Gross margin % ranked — red threshold = risk zone</div>", unsafe_allow_html=True)
        prod_sorted = prod_df.sort_values("GM%", ascending=True)
        colors = ["#F87171" if m < margin_threshold else "#34D399" for m in prod_sorted["GM%"]]
        fig3 = go.Figure(go.Bar(
            y=prod_sorted["Product Name"].str[:35],
            x=prod_sorted["GM%"],
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}%" for v in prod_sorted["GM%"]],
            textposition="outside",
            textfont=dict(color="#E8EAF0", size=10),
        ))
        fig3.add_vline(x=margin_threshold, line_dash="dash", line_color="#F5A623",
                       annotation_text=f"Risk threshold {margin_threshold}%",
                       annotation_font_color="#F5A623")
        apply_theme(fig3, xaxis=dict(ticksuffix="%", gridcolor="#1D2030", zeroline=False,
                                      tickfont=dict(color="#7B82A0")))
        fig3.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("<div class='section-title'>Regional Scorecard</div><div class='section-sub'>Revenue, GP and margin per region</div>", unsafe_allow_html=True)
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            name="Revenue", x=reg_df["Region"], y=reg_df["Sales"],
            marker_color="#252A3A",
        ))
        fig4.add_trace(go.Bar(
            name="Gross Profit", x=reg_df["Region"], y=reg_df["GrossProfit"],
            marker_color="#F5A623",
        ))
        apply_theme(fig4, barmode="group")
        fig4.update_layout(height=220, legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig4, use_container_width=True)

        # Margin table
        reg_tbl = reg_df[["Region","GM%"]].copy()
        reg_tbl["GM%"] = reg_tbl["GM%"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(reg_df[["Region","Sales","GrossProfit","GM%"]].assign(
            Sales=reg_df["Sales"].apply(lambda x: f"${x:,.0f}"),
            GrossProfit=reg_df["GrossProfit"].apply(lambda x: f"${x:,.0f}"),
            **{"GM%": reg_df["GM%"].apply(lambda x: f"{x:.1f}%")}
        ).rename(columns={"GrossProfit":"GP","GM%":"Margin"}),
            hide_index=True, use_container_width=True)

    # ── Insight bar
    at_risk = prod_df[prod_df["GM%"] < margin_threshold]
    top_prod = prod_df.nlargest(1,"GrossProfit").iloc[0]
    st.markdown(f"""
    <div class='insight-box'>
      💡 <b>Analyst Insight:</b> &nbsp;
      <b>{top_prod['Product Name']}</b> leads all SKUs with <b>${top_prod['GrossProfit']:,.0f}</b> gross profit at a
      <b>{top_prod['GM%']:.1f}%</b> margin. &nbsp;|&nbsp;
      <b>{len(at_risk)}</b> product(s) fall below the <b>{margin_threshold}%</b> margin risk threshold —
      consider repricing or discontinuation review.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 2 — PRODUCT DEEP DIVE
# ══════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>Product Intelligence Matrix</div><div class='section-sub'>All SKUs ranked by profitability — click column headers to sort</div>", unsafe_allow_html=True)

    # Full product table
    disp = prod_df[[
        "Product Name","Division","Sales","GrossProfit","Cost","Units","GM%","ProfitPerUnit","RevShare%","ProfShare%","MarginRisk"
    ]].copy()
    disp["Sales"]        = disp["Sales"].apply(lambda x: f"${x:,.0f}")
    disp["GrossProfit"]  = disp["GrossProfit"].apply(lambda x: f"${x:,.0f}")
    disp["Cost"]         = disp["Cost"].apply(lambda x: f"${x:,.0f}")
    disp["Units"]        = disp["Units"].apply(lambda x: f"{x:,.0f}")
    disp["GM%"]          = disp["GM%"].apply(lambda x: f"{x:.1f}%")
    disp["ProfitPerUnit"]= disp["ProfitPerUnit"].apply(lambda x: f"${x:.2f}" if not np.isnan(x) else "—")
    disp["RevShare%"]    = disp["RevShare%"].apply(lambda x: f"{x:.1f}%")
    disp["ProfShare%"]   = disp["ProfShare%"].apply(lambda x: f"{x:.1f}%")
    disp.columns = ["Product","Division","Revenue","Gross Profit","COGS","Units","Margin %","Profit/Unit","Rev Share","Profit Share","Risk Status"]
    st.dataframe(disp, hide_index=True, use_container_width=True, height=380)

    st.markdown("<br>", unsafe_allow_html=True)

    # Scatter: Sales vs GP (bubble = units)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Sales vs. Gross Profit Matrix</div><div class='section-sub'>Bubble size = units sold · Identify high-volume low-margin SKUs</div>", unsafe_allow_html=True)
        fig_s = px.scatter(
            prod_df, x="Sales", y="GrossProfit", size="Units",
            color="GM%", color_continuous_scale=["#F87171","#F5A623","#34D399"],
            hover_name="Product Name",
            hover_data={"Sales":":.0f","GrossProfit":":.0f","GM%":":.1f","Units":":.0f"},
            labels={"Sales":"Revenue ($)","GrossProfit":"Gross Profit ($)","GM%":"Margin %"},
        )
        apply_theme(fig_s, coloraxis_colorbar=dict(
            tickfont=dict(color="#7B82A0"), title=dict(text="GM %", font=dict(color="#7B82A0"))
        ))
        fig_s.update_layout(height=350)
        st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Margin vs. Profit/Unit Quadrant</div><div class='section-sub'>Upper-right = star performers · Lower-left = review candidates</div>", unsafe_allow_html=True)
        q_df = prod_df.dropna(subset=["ProfitPerUnit"])
        med_gm  = q_df["GM%"].median()
        med_ppu = q_df["ProfitPerUnit"].median()
        fig_q = px.scatter(
            q_df, x="GM%", y="ProfitPerUnit",
            color="Division", size="Sales",
            hover_name="Product Name",
            labels={"GM%":"Gross Margin %","ProfitPerUnit":"Profit per Unit ($)"},
            color_discrete_sequence=["#F5A623","#E8547A","#4ECDC4","#A78BFA"],
        )
        fig_q.add_vline(x=med_gm,  line_dash="dot", line_color="#7B82A0", opacity=.5)
        fig_q.add_hline(y=med_ppu, line_dash="dot", line_color="#7B82A0", opacity=.5)
        # Quadrant labels
        for txt, ax, ay in [
            ("⭐ Stars",      q_df["GM%"].max()*0.85, q_df["ProfitPerUnit"].max()*0.85),
            ("⬆ Price Up",   q_df["GM%"].min()*1.15,  q_df["ProfitPerUnit"].max()*0.85),
            ("📉 Review",    q_df["GM%"].min()*1.15,  med_ppu*0.3),
            ("📦 Volume",    q_df["GM%"].max()*0.85,  med_ppu*0.3),
        ]:
            fig_q.add_annotation(x=ax, y=ay, text=txt, showarrow=False,
                                  font=dict(color="#7B82A0", size=10))
        apply_theme(fig_q)
        fig_q.update_layout(height=350)
        st.plotly_chart(fig_q, use_container_width=True)

    # Margin variance over time per product
    st.markdown("<div class='section-title'>Product Margin Volatility (Monthly)</div><div class='section-sub'>Margin % over time — wide swings signal pricing or cost instability</div>", unsafe_allow_html=True)
    top_prods = prod_df.nlargest(6,"GrossProfit")["Product Name"].tolist()
    mv_df = dff[dff["Product Name"].isin(top_prods)].groupby(["YearMonth","Product Name"]).agg(
        Sales=("Sales","sum"), GP=("Gross Profit","sum")
    ).reset_index()
    mv_df["GM%"] = mv_df["GP"] / mv_df["Sales"] * 100
    fig_v = px.line(mv_df, x="YearMonth", y="GM%", color="Product Name",
                    labels={"YearMonth":"Month","GM%":"Gross Margin %"},
                    color_discrete_sequence=["#F5A623","#E8547A","#4ECDC4","#A78BFA","#34D399","#60A5FA"])
    apply_theme(fig_v, yaxis=dict(ticksuffix="%", gridcolor="#1D2030", zeroline=False,
                                   tickfont=dict(color="#7B82A0")))
    fig_v.update_layout(height=280)
    st.plotly_chart(fig_v, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 3 — DIVISION & REGION
# ══════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-title'>Division Performance Dashboard</div><div class='section-sub'>Revenue, profitability and efficiency metrics across divisions</div>", unsafe_allow_html=True)

    # Division KPI cards
    d_cols = st.columns(len(div_df))
    for i, (_, row) in enumerate(div_df.iterrows()):
        with d_cols[i]:
            color = "#34D399" if row["GM%"] >= 60 else ("#F5A623" if row["GM%"] >= 40 else "#F87171")
            st.markdown(f"""
            <div style='background:#1A1E2B;border:1px solid #252A3A;border-top:3px solid {color};
                        border-radius:12px;padding:18px;text-align:center;'>
              <div style='font-size:13px;color:#7B82A0;text-transform:uppercase;letter-spacing:.08em;'>{row['Division']}</div>
              <div style='font-size:28px;font-weight:700;color:#E8EAF0;margin:8px 0 4px;'>${row['GrossProfit']:,.0f}</div>
              <div style='font-size:20px;font-weight:600;color:{color};'>{row['GM%']:.1f}%</div>
              <div style='font-size:11px;color:#7B82A0;margin-top:4px;'>Revenue: ${row['Sales']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Revenue vs. Profit by Division</div>", unsafe_allow_html=True)
        fig_d = go.Figure()
        fig_d.add_trace(go.Bar(name="Revenue",      x=div_df["Division"], y=div_df["Sales"],
                               marker_color="#252A3A"))
        fig_d.add_trace(go.Bar(name="Gross Profit", x=div_df["Division"], y=div_df["GrossProfit"],
                               marker_color="#F5A623"))
        fig_d.add_trace(go.Bar(name="COGS",         x=div_df["Division"], y=div_df["Cost"],
                               marker_color="#E8547A"))
        apply_theme(fig_d, barmode="group")
        fig_d.update_layout(height=300)
        st.plotly_chart(fig_d, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Margin Distribution by Division</div>", unsafe_allow_html=True)
        fig_box = go.Figure()
        colors = ["#F5A623","#E8547A","#4ECDC4"]
        for idx, div in enumerate(div_df["Division"]):
            sub = dff[dff["Division"]==div]["Gross Margin %"]
            fig_box.add_trace(go.Box(
                y=sub, name=div, marker_color=colors[idx % len(colors)],
                line_color=colors[idx % len(colors)], fillcolor="rgba(0,0,0,0)",
                boxmean="sd",
            ))
        apply_theme(fig_box, yaxis=dict(ticksuffix="%", gridcolor="#1D2030",
                                         tickfont=dict(color="#7B82A0"), zeroline=False))
        fig_box.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>Regional Deep Dive</div><div class='section-sub'>State-level profit concentration and regional margin efficiency</div>", unsafe_allow_html=True)

    c3, c4 = st.columns([3, 2])
    with c3:
        fig_state = go.Figure(go.Bar(
            x=state_df["GrossProfit"],
            y=state_df["State/Province"],
            orientation="h",
            marker=dict(
                color=state_df["GM%"],
                colorscale=[[0,"#F87171"],[0.5,"#F5A623"],[1,"#34D399"]],
                showscale=True,
                colorbar=dict(tickfont=dict(color="#7B82A0"),
                              title=dict(text="GM %", font=dict(color="#7B82A0"))),
            ),
            text=[f"${v:,.0f}" for v in state_df["GrossProfit"]],
            textposition="outside",
            textfont=dict(color="#E8EAF0", size=10),
        ))
        apply_theme(fig_state, title="Top 15 States by Gross Profit (color = margin %)")
        fig_state.update_layout(height=450)
        st.plotly_chart(fig_state, use_container_width=True)

    with c4:
        st.markdown("<div class='section-title'>Region × Division Heatmap</div>", unsafe_allow_html=True)
        heat_df = dff.groupby(["Region","Division"])["Gross Margin %"].mean().reset_index()
        heat_pivot = heat_df.pivot(index="Division", columns="Region", values="Gross Margin %")
        fig_heat = go.Figure(go.Heatmap(
            z=heat_pivot.values,
            x=heat_pivot.columns.tolist(),
            y=heat_pivot.index.tolist(),
            colorscale=[[0,"#F87171"],[0.5,"#F5A623"],[1,"#34D399"]],
            text=[[f"{v:.1f}%" for v in row] for row in heat_pivot.values],
            texttemplate="%{text}",
            textfont=dict(color="white", size=12),
            showscale=True,
            colorbar=dict(tickfont=dict(color="#7B82A0"), title=dict(text="GM %", font=dict(color="#7B82A0"))),
        ))
        apply_theme(fig_heat)
        fig_heat.update_layout(height=320)
        st.plotly_chart(fig_heat, use_container_width=True)

        # Ship mode analysis
        sm_df = dff.groupby("Ship Mode").agg(
            Sales=("Sales","sum"), GP=("Gross Profit","sum"), Orders=("Order ID","nunique")
        ).reset_index()
        sm_df["GM%"] = sm_df["GP"] / sm_df["Sales"] * 100
        st.markdown("**Ship Mode Margin Summary**")
        st.dataframe(sm_df.assign(
            Sales=sm_df["Sales"].apply(lambda x: f"${x:,.0f}"),
            GP=sm_df["GP"].apply(lambda x: f"${x:,.0f}"),
            **{"GM%": sm_df["GM%"].apply(lambda x: f"{x:.1f}%")}
        )[["Ship Mode","Sales","GP","GM%","Orders"]].rename(columns={"GP":"Gross Profit","GM%":"Margin"}),
            hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 4 — PARETO & COST DIAGNOSTICS
# ══════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-title'>Profit Concentration (Pareto) Analysis</div><div class='section-sub'>Which products drive 80% of profit? Identify dependency risks</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        # Pareto — Revenue
        pareto_rev = prod_df.sort_values("Sales", ascending=False).copy()
        pareto_rev["CumRev%"] = pareto_rev["Sales"].cumsum() / total_sales * 100
        pareto_rev["ProdIdx"] = range(1, len(pareto_rev)+1)

        fig_par_r = make_subplots(specs=[[{"secondary_y": True}]])
        fig_par_r.add_trace(go.Bar(
            x=pareto_rev["Product Name"].str[:20],
            y=pareto_rev["Sales"],
            marker_color="#A78BFA", name="Revenue",
        ), secondary_y=False)
        fig_par_r.add_trace(go.Scatter(
            x=pareto_rev["Product Name"].str[:20],
            y=pareto_rev["CumRev%"],
            mode="lines+markers", name="Cumulative %",
            line=dict(color="#F5A623", width=2.5),
        ), secondary_y=True)
        fig_par_r.add_hline(y=80, secondary_y=True, line_dash="dash", line_color="#E8547A",
                            annotation_text="80% threshold",
                            annotation_font_color="#E8547A",
                            annotation_xanchor="left", annotation_xshift=6)
        apply_theme(fig_par_r,
                    title="Revenue Pareto",
                    yaxis2=dict(range=[0,105], ticksuffix="%",
                                gridcolor="rgba(0,0,0,0)",
                                tickfont=dict(color="#F5A623")))
        fig_par_r.update_layout(height=320, xaxis_tickangle=-35, showlegend=False)
        st.plotly_chart(fig_par_r, use_container_width=True)

    with c2:
        # Pareto — Profit
        pareto_gp = prod_df.sort_values("GrossProfit", ascending=False).copy()
        pareto_gp["CumGP%"] = pareto_gp["GrossProfit"].cumsum() / total_gp * 100

        fig_par_g = make_subplots(specs=[[{"secondary_y": True}]])
        fig_par_g.add_trace(go.Bar(
            x=pareto_gp["Product Name"].str[:20],
            y=pareto_gp["GrossProfit"],
            marker_color="#4ECDC4", name="Gross Profit",
        ), secondary_y=False)
        fig_par_g.add_trace(go.Scatter(
            x=pareto_gp["Product Name"].str[:20],
            y=pareto_gp["CumGP%"],
            mode="lines+markers", name="Cumulative %",
            line=dict(color="#F5A623", width=2.5),
        ), secondary_y=True)
        fig_par_g.add_hline(y=80, secondary_y=True, line_dash="dash", line_color="#E8547A",
                            annotation_text="80% threshold",
                            annotation_font_color="#E8547A",
                            annotation_xanchor="left", annotation_xshift=6)
        apply_theme(fig_par_g,
                    title="Gross Profit Pareto",
                    yaxis2=dict(range=[0,105], ticksuffix="%",
                                gridcolor="rgba(0,0,0,0)",
                                tickfont=dict(color="#F5A623")))
        fig_par_g.update_layout(height=320, xaxis_tickangle=-35, showlegend=False)
        st.plotly_chart(fig_par_g, use_container_width=True)

    # 80% lines annotation
    n_rev_80 = int((pareto_rev["CumRev%"] <= 80).sum()) + 1
    n_gp_80  = int((pareto_gp["CumGP%"]  <= 80).sum()) + 1
    st.markdown(f"""
    <div class='insight-box'>
      📊 <b>Pareto Finding:</b> &nbsp;
      <b>{n_rev_80}</b> out of <b>{len(prod_df)}</b> SKUs generate <b>≥80%</b> of total revenue. &nbsp;|&nbsp;
      <b>{n_gp_80}</b> SKUs drive <b>≥80%</b> of gross profit — signaling high concentration risk
      if these products face supply disruption or pricing pressure.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>Cost Structure Diagnostics</div><div class='section-sub'>Cost vs. sales scatter — flag margin-poor, cost-heavy products</div>", unsafe_allow_html=True)

    c3, c4 = st.columns([3,2])
    with c3:
        # Cost vs Sales scatter with margin color
        fig_cs = px.scatter(
            prod_df, x="Cost", y="Sales",
            size="Units", color="GM%",
            color_continuous_scale=["#F87171","#F5A623","#34D399"],
            hover_name="Product Name",
            text="Product Name",
            labels={"Cost":"Total COGS ($)","Sales":"Total Revenue ($)","GM%":"Margin %"},
        )
        # 45-degree breakeven line
        max_val = max(prod_df["Sales"].max(), prod_df["Cost"].max())
        fig_cs.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val],
            mode="lines", name="Break-even (0% GP)",
            line=dict(color="#F87171", dash="dash", width=1.5),
        ))
        fig_cs.update_traces(textposition="top center", textfont_size=9,
                              selector=dict(mode="markers+text"))
        apply_theme(fig_cs, coloraxis_colorbar=dict(
            tickfont=dict(color="#7B82A0"), title=dict(text="GM %", font=dict(color="#7B82A0"))
        ))
        fig_cs.update_layout(height=380)
        st.plotly_chart(fig_cs, use_container_width=True)

    with c4:
        # Risk flag table
        st.markdown("<div class='section-title'>⚠️ Margin Risk Flags</div>", unsafe_allow_html=True)
        risk_prods = prod_df[prod_df["GM%"] < margin_threshold].sort_values("GM%")[
            ["Product Name","Division","GM%","Sales","GrossProfit"]
        ].copy()

        if len(risk_prods):
            risk_prods["Action"] = risk_prods["GM%"].apply(
                lambda m: "🔴 Discontinue Review" if m < 15 else
                          ("🟡 Reprice" if m < 30 else "🟠 Monitor")
            )
            risk_prods["GM%"]         = risk_prods["GM%"].apply(lambda x: f"{x:.1f}%")
            risk_prods["Sales"]       = risk_prods["Sales"].apply(lambda x: f"${x:,.0f}")
            risk_prods["GrossProfit"] = risk_prods["GrossProfit"].apply(lambda x: f"${x:,.0f}")
            risk_prods.columns = ["Product","Division","Margin","Revenue","GP","Recommendation"]
            st.dataframe(risk_prods, hide_index=True, use_container_width=True, height=220)
        else:
            st.success(f"✅ All products are above the {margin_threshold}% margin threshold!")

        # Cost efficiency summary
        st.markdown("<br>", unsafe_allow_html=True)
        prod_df["CostRatio"] = prod_df["Cost"] / prod_df["Sales"]
        hi_cost = prod_df.nlargest(5,"CostRatio")[["Product Name","CostRatio","GM%"]]
        hi_cost.columns = ["Product","Cost/Rev Ratio","GM %"]
        hi_cost["Cost/Rev Ratio"] = hi_cost["Cost/Rev Ratio"].apply(lambda x: f"{x:.1%}")
        hi_cost["GM %"]           = hi_cost["GM %"].apply(lambda x: f"{x:.1f}%")
        st.markdown("**Highest Cost-to-Revenue Products**")
        st.dataframe(hi_cost, hide_index=True, use_container_width=True)

    # Waterfall: contribution bridge
    st.markdown("---")
    st.markdown("<div class='section-title'>Profitability Contribution Bridge</div><div class='section-sub'>How each product builds up total gross profit</div>", unsafe_allow_html=True)

    bridge_df = prod_df.sort_values("GrossProfit", ascending=False)
    measures  = ["relative"] * len(bridge_df) + ["total"]
    x_vals    = list(bridge_df["Product Name"].str[:22]) + ["TOTAL"]
    y_vals    = list(bridge_df["GrossProfit"])  + [total_gp]

    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=measures,
        x=x_vals,
        y=y_vals,
        connector=dict(line=dict(color="#252A3A", dash="dot")),
        increasing=dict(marker=dict(color="#34D399")),
        decreasing=dict(marker=dict(color="#F87171")),
        totals=dict(marker=dict(color="#F5A623")),
        text=[f"${v:,.0f}" for v in y_vals],
        textposition="outside",
        textfont=dict(color="#E8EAF0", size=9),
    ))
    apply_theme(fig_wf)
    fig_wf.update_layout(height=340, xaxis_tickangle=-30)
    st.plotly_chart(fig_wf, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='display:flex;justify-content:space-between;align-items:center;
            padding:10px 0;color:#7B82A0;font-size:11px;'>
  <div>🍬 <b style='color:#F5A623;'>Nassau Candy Distributor</b> · Product Line Profitability & Margin Performance Intelligence Platform</div>
  <div>Data: FY 2024–2025 · Built with Streamlit + Plotly</div>
</div>
""", unsafe_allow_html=True)