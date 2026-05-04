import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


st.set_page_config(
    page_title="SupplyChain·AI | Favorita Grocery",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root & Body ── */
:root {
    --bg:      #080c18;
    --surface: #0f1623;
    --card:    #131a28;
    --border:  #1a2840;
    --navy:    #055475;
    --teal:    #0f6b8a;
    --cyan:    #00C896;
    --red:     #F5606A;
    --amber:   #F4A118;
    --text:    #dce8f8;
    --muted:   #5f7a96;
    --light:   #9ab8cf;
}
html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    background-image:
        linear-gradient(rgba(5,84,117,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(5,84,117,0.06) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Main Content ── */
.main .block-container {
    padding: 1.5rem 2rem 2rem 2rem;
    max-width: 1500px;
}

/* ── KPI Cards ── */
.kpi-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
    margin-bottom: 0;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #055475, #00C896);
}
.kpi-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
    font-family: 'Space Mono', monospace;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 4px;
    line-height: 1;
}
.kpi-sub {
    font-size: 11px;
    color: var(--muted);
    margin-top: 6px;
}
.kpi-glow {
    position: absolute;
    bottom: -15px;
    right: -5px;
    font-size: 58px;
    opacity: 0.07;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--cyan);
    margin: 20px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1a2840, transparent);
}

/* ── Insight Box ── */
.insight-box {
    background: linear-gradient(135deg, rgba(5,84,117,0.18), rgba(0,200,150,0.08));
    border: 1px solid rgba(0,200,150,0.22);
    border-radius: 13px;
    padding: 20px 24px;
    margin-bottom: 20px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
}
.insight-icon { font-size: 26px; flex-shrink: 0; margin-top: 2px; }
.insight-title { font-size: 13px; font-weight: 700; color: var(--cyan); margin-bottom: 6px; font-family: 'Syne', sans-serif; }
.insight-body { font-size: 12px; color: var(--light); line-height: 1.7; }

/* ── Rec Cards ── */
.rec-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    height: 100%;
}
.rec-icon { font-size: 26px; margin-bottom: 10px; }
.rec-title { font-size: 13px; font-weight: 700; color: var(--text); margin-bottom: 6px; font-family: 'Syne', sans-serif; }
.rec-body { font-size: 12px; color: var(--muted); line-height: 1.65; margin-bottom: 10px; }
.rec-tag {
    display: inline-block;
    font-size: 9px;
    padding: 3px 9px;
    border-radius: 4px;
    background: rgba(15,107,138,0.25);
    color: #0f9dc2;
    border: 1px solid rgba(15,107,138,0.35);
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Pipeline Step ── */
.pipeline-step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.step-num {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    color: var(--cyan);
    background: rgba(0,200,150,0.1);
    border: 1px solid rgba(0,200,150,0.2);
    width: 30px;
    height: 30px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.step-title { font-size: 13px; font-weight: 700; color: var(--text); margin-bottom: 3px; font-family: 'Syne', sans-serif; }
.step-desc { font-size: 12px; color: var(--muted); }

/* ── Stat Pill ── */
.stat-pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 13px 18px;
    text-align: center;
}
.stat-pill-label { font-size: 9px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--muted); margin-bottom: 5px; font-family: 'Space Mono', monospace; }
.stat-pill-val { font-family: 'Space Mono', monospace; font-size: 20px; font-weight: 700; }

/* ── Header ── */
.dash-header {
    background: rgba(8,12,24,0.92);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 26px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(12px);
}
.header-logo { display: flex; align-items: center; gap: 14px; }
.logo-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #055475, #00C896);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.logo-text { font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; color: var(--text); letter-spacing: 1px; }
.logo-sub { font-size: 10px; color: var(--muted); letter-spacing: 2.5px; text-transform: uppercase; margin-top: 2px; }
.badge-group { display: flex; gap: 10px; align-items: center; }
.badge {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    padding: 5px 12px;
    border: 1px solid var(--cyan);
    border-radius: 20px;
    color: var(--cyan);
    letter-spacing: 0.8px;
}
.live-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 12px var(--cyan);
    animation: pulse 2s infinite;
    display: inline-block;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.35); }
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stToolbar"] { display: none; }

/* ── Sidebar nav buttons ── */
.stRadio > div { gap: 8px !important; }
.stRadio > div > label {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 12px 18px !important;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    width: 100%;
    transition: all 0.2s;
    color: var(--light) !important;
}
.stRadio > div > label:hover { border-color: var(--teal) !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* Plotly chart background */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA ───────────────────────────────────────────────────────────────
MONTHS = ['Sep 15','Oct 15','Nov 15','Dec 15','Jan 16','Feb 16','Mar 16','Apr 16',
          'May 16','Jun 16','Jul 16','Aug 16','Sep 16','Oct 16','Nov 16','Dec 16',
          'Jan 17','Feb 17','Mar 17','Apr 17','May 17','Jun 17','Jul 17','Aug 17']

MONTHLY_SALES = [434.7,432.2,426.6,509.6,434.1,424.7,418.7,485.7,448.6,415.4,424.7,406.4,
                 419.3,435.0,461.0,554.4,476.6,466.0,483.4,484.4,487.2,480.4,489.0,465.1]

OIL = [45.5,46.2,42.4,37.2,31.7,30.3,37.5,40.8,46.7,48.8,44.7,44.7,
       45.2,49.8,45.7,52.0,52.5,53.5,49.3,51.1,48.5,45.2,46.6,48.9]

TOTAL_SALES_M = [14.45,14.80,13.72,19.10,12.91,13.98,15.08,16.35,15.14,14.66,13.21,15.83,
                 13.77,13.92,15.87,19.49,15.32,14.46,17.90,14.35,17.64,16.81,14.47,8.76]

DOW_LABELS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
DOW_DATA   = [346.5, 319.8, 332.9, 283.5, 325.2, 433.3, 463.1]

PLOT_BG    = "rgba(0,0,0,0)"
PAPER_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(26,40,64,0.9)"
FONT_COLOR = "#6b8199"

def base_layout(**kwargs):
    return dict(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, family="DM Sans"),
        margin=dict(l=10, r=10, t=10, b=10),
        **kwargs
    )

def xax(extra=None):
    d = dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickcolor=GRID_COLOR)
    if extra:
        d.update(extra)
    return d

def yax(extra=None):
    d = dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickcolor=GRID_COLOR)
    if extra:
        d.update(extra)
    return d


# ── SIDEBAR ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 20px 0;'>
        <div style='font-family:Space Mono,monospace;font-size:12px;letter-spacing:2px;color:#00C896;margin-bottom:4px;'>SUPPLYCHAIN·AI</div>
        <div style='font-size:10px;color:#5f7a96;letter-spacing:2px;text-transform:uppercase;'>Favorita Grocery · Ecuador</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📊  Overview", "📈  Demand Patterns", "🛒  Products & Stores", "🤖  Forecasting Model", "💡  ERP Insights"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:Space Mono,monospace;font-size:9px;letter-spacing:1.5px;color:#5f7a96;text-transform:uppercase;padding:12px 0 6px 0;border-top:1px solid #1a2840;'>
        Model Info
    </div>
    """, unsafe_allow_html=True)

    for label, val, color in [
        ("Algorithm", "LightGBM", "#00C896"),
        ("RMSLE Score", "0.43", "#00C896"),
        ("Boost Rounds", "1,000", "#F4A118"),
        ("Features", "24", "#0f9dc2"),
        ("Training Rows", "3.0M+", "#dce8f8"),
    ]:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid rgba(26,40,64,0.5);'>
            <span style='font-size:11px;color:#5f7a96;'>{label}</span>
            <span style='font-family:Space Mono,monospace;font-size:12px;font-weight:700;color:{color};'>{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:28px;font-size:10px;color:#3a5269;font-family:Space Mono,monospace;text-align:center;letter-spacing:0.5px;'>
        MS (AI & Data Science)<br>SAD Project · Anish Yadav<br>April 2026
    </div>
    """, unsafe_allow_html=True)


# ── HEADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="header-logo">
    <div class="logo-icon">🏪</div>
    <div>
      <div class="logo-text">SUPPLYCHAIN·AI</div>
      <div class="logo-sub">Favorita Grocery · Ecuador · 2013–2017</div>
    </div>
  </div>
  <div class="badge-group">
    <span class="badge">LightGBM · RMSLE 0.43</span>
    <span class="badge">3.0M+ Records</span>
    <span class="live-dot"></span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════
if "Overview" in page:

    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        ("Total Training Records", "3.0M+", "Daily sales rows · 2013–2017", "📦", "#00C896"),
        ("Stores Analyzed", "54", "5 types · 16 clusters · Ecuador", "🏪", "#0f9dc2"),
        ("Product Families", "33", "Grocery, Beverages, Produce…", "🛒", "#F4A118"),
        ("Forecast RMSLE", "0.43", "LightGBM · Validation set", "🤖", "#00C896"),
    ]
    for col, (label, val, sub, icon, color) in zip([c1, c2, c3, c4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color};">{val}</div>
              <div class="kpi-sub">{sub}</div>
              <div class="kpi-glow">{icon}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sales Trend Overview</div>', unsafe_allow_html=True)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=MONTHS, y=MONTHLY_SALES, mode='lines+markers',
        line=dict(color='#00C896', width=2.5),
        marker=dict(size=5, color='#00C896'),
        fill='tozeroy',
        fillcolor='rgba(0,200,150,0.08)',
        name='Avg Sales',
        hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:.1f}<extra></extra>'
    ))
    fig_trend.update_layout(
        **base_layout(
            height=220,
            showlegend=False,
            xaxis=xax({'tickfont': dict(size=10), 'tickangle': 45}),
            yaxis=yax({'tickfont': dict(size=10)}),
            annotations=[dict(
                x=0.98, y=0.97, xref='paper', yref='paper',
                text='<b>+121% YoY 2013→2017</b>',
                font=dict(size=11, color='#00C896', family='Space Mono'),
                showarrow=False, align='right',
                bgcolor='rgba(0,200,150,0.1)', bordercolor='rgba(0,200,150,0.3)', borderwidth=1,
                borderpad=6
            )]
        )
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Year-over-Year Growth</div>', unsafe_allow_html=True)
        years  = ['2013','2014','2015','2016','2017']
        yearly = [216.5, 322.9, 371.4, 443.8, 480.1]
        colors = ['rgba(5,84,117,0.55)','rgba(15,107,138,0.65)','rgba(15,107,138,0.75)','rgba(0,200,150,0.65)','rgba(0,200,150,1)']
        fig_yr = go.Figure(go.Bar(
            x=years, y=yearly, marker_color=colors,
            marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:.1f}<extra></extra>'
        ))
        fig_yr.update_traces(marker_cornerradius=6)
        fig_yr.update_layout(
            **base_layout(height=260, xaxis=xax(), yaxis=yax({'title': 'Avg Sales'}))
        )
        st.plotly_chart(fig_yr, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown('<div class="section-title">Day of Week Pattern</div>', unsafe_allow_html=True)
        bar_colors = ['rgba(0,200,150,0.85)' if i >= 5 else 'rgba(15,107,138,0.5)' for i in range(7)]
        fig_dow = go.Figure(go.Bar(
            x=DOW_LABELS, y=DOW_DATA, marker_color=bar_colors,
            marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:.1f}<extra></extra>'
        ))
        fig_dow.update_traces(marker_cornerradius=5)
        fig_dow.update_layout(
            **base_layout(height=260, xaxis=xax(), yaxis=yax({'title': 'Avg Sales'}))
        )
        st.plotly_chart(fig_dow, use_container_width=True, config={'displayModeBar': False})


# ══════════════════════════════════════════════════════════════════════
# PAGE: DEMAND PATTERNS  (all fixes applied here)
# ══════════════════════════════════════════════════════════════════════
elif "Demand" in page:

    pills = [
        ("Holiday Lift",    "+10.6%", "#00C896"),
        ("Promo Lift",      "+619%",  "#10b981"),
        ("Oil Correlation", "r = −0.70", "#F5606A"),
        ("Weekend Premium", "+37%",   "#F4A118"),
        ("Normal Avg Sales","352.2",  "#dce8f8"),
        ("Holiday Avg Sales","389.7", "#00C896"),
    ]
    cols = st.columns(6)
    for col, (label, val, color) in zip(cols, pills):
        with col:
            st.markdown(f"""
            <div class="stat-pill">
                <div class="stat-pill-label">{label}</div>
                <div class="stat-pill-val" style="color:{color};">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Demand Drivers</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_hol = go.Figure(go.Bar(
            x=['Normal Day', 'Holiday'], y=[352.2, 389.7],
            marker_color=['rgba(15,107,138,0.6)', 'rgba(0,200,150,0.88)'],
            marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:.1f}<extra></extra>'
        ))
        fig_hol.update_traces(marker_cornerradius=7)
        # FIX: xaxis & yaxis passed inside base_layout() to avoid duplicate keyword error
        fig_hol.update_layout(
            **base_layout(
                height=280,
                xaxis=xax(),
                yaxis=yax(),
            ),
            title=dict(text='Holiday vs Normal Day Sales', font=dict(size=13, color='#dce8f8'), x=0)
        )
        st.plotly_chart(fig_hol, use_container_width=True, config={'displayModeBar': False})

    with col2:
        fig_promo = go.Figure(go.Bar(
            x=['No Promotion', 'On Promotion'], y=[158.2, 1137.7],
            marker_color=['rgba(100,113,153,0.6)', 'rgba(16,185,129,0.88)'],
            marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:.1f}<extra></extra>'
        ))
        fig_promo.update_traces(marker_cornerradius=7)
        # FIX: xaxis & yaxis passed inside base_layout() to avoid duplicate keyword error
        fig_promo.update_layout(
            **base_layout(
                height=280,
                xaxis=xax(),
                yaxis=yax(),
            ),
            title=dict(text='Promotion Impact (+619%)', font=dict(size=13, color='#dce8f8'), x=0)
        )
        st.plotly_chart(fig_promo, use_container_width=True, config={'displayModeBar': False})

    # Oil dual axis — unchanged (uses manual layout dict, no conflict)
    st.markdown('<div class="section-title">Macro-Economic Correlation</div>', unsafe_allow_html=True)
    fig_oil = go.Figure()
    fig_oil.add_trace(go.Scatter(
        x=MONTHS, y=TOTAL_SALES_M, mode='lines+markers', name='Total Sales (M)',
        line=dict(color='#0f9dc2', width=2.2), marker=dict(size=4),
        yaxis='y', hovertemplate='Sales: %{y:.2f}M<extra></extra>'
    ))
    fig_oil.add_trace(go.Scatter(
        x=MONTHS, y=OIL, mode='lines+markers', name='Oil Price (USD)',
        line=dict(color='#F5606A', width=2.2, dash='dot'), marker=dict(size=4),
        yaxis='y2', hovertemplate='Oil: $%{y}<extra></extra>'
    ))
    fig_oil.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, family='DM Sans'),
        height=260, margin=dict(l=10, r=50, t=30, b=10),
        title=dict(text='Oil Price vs Total Monthly Sales  ·  Pearson r = −0.70', font=dict(size=12, color='#dce8f8'), x=0),
        legend=dict(font=dict(size=11, color='#9ab8cf'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.99),
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10), tickangle=40),
        yaxis=dict(title='Sales (M)', title_font=dict(color='#0f9dc2'), tickfont=dict(color='#0f9dc2'), gridcolor=GRID_COLOR),
        yaxis2=dict(title='Oil Price', title_font=dict(color='#F5606A'), tickfont=dict(color='#F5606A'), overlaying='y', side='right', gridcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig_oil, use_container_width=True, config={'displayModeBar': False})

    # Weekly pattern
    st.markdown('<div class="section-title">Weekly Demand Pattern</div>', unsafe_allow_html=True)
    bar_colors2 = ['rgba(244,161,24,0.85)' if i >= 5 else 'rgba(15,107,138,0.5)' for i in range(7)]
    fig_dow2 = go.Figure(go.Bar(
        x=DOW_LABELS, y=DOW_DATA, marker_color=bar_colors2,
        marker=dict(line=dict(width=0)),
        hovertemplate='<b>%{x}</b><br>Avg Sales: %{y:.1f}<extra></extra>'
    ))
    fig_dow2.update_traces(marker_cornerradius=5)
    # FIX: xaxis & yaxis passed inside base_layout() to avoid duplicate keyword error
    fig_dow2.update_layout(
        **base_layout(height=220, xaxis=xax(), yaxis=yax())
    )
    st.plotly_chart(fig_dow2, use_container_width=True, config={'displayModeBar': False})


# ══════════════════════════════════════════════════════════════════════
# PAGE: PRODUCTS & STORES
# ══════════════════════════════════════════════════════════════════════
elif "Products" in page:

    st.markdown('<div class="section-title">Product Family Analysis</div>', unsafe_allow_html=True)

    families = [
        ("GROCERY I",     343.5, "#00C896"),
        ("BEVERAGES",     217.0, "#0f9dc2"),
        ("PRODUCE",       122.7, "#F5606A"),
        ("CLEANING",       97.5, "#0f9dc2"),
        ("DAIRY",          64.5, "#F5606A"),
        ("BREAD/BAKERY",   42.1, "#F5606A"),
        ("POULTRY",        31.9, "#F4A118"),
        ("MEATS",          31.1, "#F5606A"),
        ("PERSONAL CARE",  24.6, "#0f9dc2"),
        ("DELI",           24.1, "#F4A118"),
    ]
    fnames  = [f[0] for f in families]
    fvals   = [f[1] for f in families]
    fcolors = [f[2] for f in families]

    col1, col2 = st.columns(2)
    with col1:
        fig_fam = go.Figure(go.Bar(
            x=fvals, y=fnames, orientation='h',
            marker_color=fcolors, marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{y}</b><br>Sales: %{x:.1f}M<extra></extra>'
        ))
        fig_fam.update_traces(marker_cornerradius=4)
        fig_fam.update_layout(
            **base_layout(
                height=350,
                xaxis=xax({'title': 'Sales (M)'}),
                yaxis=yax({'gridcolor': 'rgba(0,0,0,0)', 'categoryorder': 'total ascending'}),
            ),
            title=dict(text='Top 10 Product Families · Total Sales (M)', font=dict(size=12, color='#dce8f8'), x=0)
        )
        st.plotly_chart(fig_fam, use_container_width=True, config={'displayModeBar': False})

    with col2:
        fig_pie = go.Figure(go.Pie(
            labels=fnames, values=fvals,
            hole=0.52,
            marker=dict(
                colors=['#00C896','#0f9dc2','#F5606A','#055475','#F4A118',
                        '#10b981','#6b8199','#e05b60','#3b82f6','#a78bfa'],
                line=dict(color='#131a28', width=2)
            ),
            textfont=dict(size=10, color='#9ab8cf'),
            hovertemplate='<b>%{label}</b><br>%{value:.1f}M (%{percent})<extra></extra>'
        ))
        fig_pie.update_layout(
            paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
            height=350, margin=dict(l=0, r=0, t=30, b=0),
            title=dict(text='Sales Distribution by Family', font=dict(size=12, color='#dce8f8'), x=0),
            legend=dict(font=dict(size=9, color='#9ab8cf'), bgcolor='rgba(0,0,0,0)', x=1, y=0.5),
            annotations=[dict(
                text='<b>TOP 3<br>= 64%</b>', x=0.5, y=0.5, showarrow=False,
                font=dict(size=13, color='#00C896', family='Space Mono')
            )]
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="section-title">Store Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        store_types  = ['Type A','Type D','Type C','Type B','Type E']
        store_vals   = [353.0, 351.1, 164.4, 145.3, 59.8]
        store_colors = ['rgba(0,200,150,0.9)','rgba(0,200,150,0.72)','rgba(15,107,138,0.7)','rgba(15,107,138,0.52)','rgba(107,129,153,0.5)']
        fig_st = go.Figure(go.Bar(
            x=store_types, y=store_vals, marker_color=store_colors,
            marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>Sales: %{y}M<extra></extra>'
        ))
        fig_st.update_traces(marker_cornerradius=6)
        fig_st.update_layout(
            **base_layout(
                height=300,
                xaxis=xax(),
                yaxis=yax({'title': 'Total Sales (M)'}),
            ),
            title=dict(text='Sales by Store Type', font=dict(size=12, color='#dce8f8'), x=0)
        )
        st.plotly_chart(fig_st, use_container_width=True, config={'displayModeBar': False})

    with col2:
        perishables = [
            ("PRODUCE",      122.7, "#F5606A"),
            ("DAIRY",         64.5, "#F5606A"),
            ("BREAD/BAKERY",  42.1, "#F4A118"),
            ("POULTRY",       31.9, "#F4A118"),
            ("MEATS",         31.1, "#F5606A"),
            ("DELI",          24.1, "#F4A118"),
            ("SEAFOOD",        8.2, "#F4A118"),
        ]
        p_names  = [p[0] for p in perishables]
        p_vals   = [p[1] for p in perishables]
        p_colors = [p[2] for p in perishables]
        fig_per = go.Figure(go.Bar(
            x=p_vals, y=p_names, orientation='h',
            marker_color=p_colors, marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{y}</b><br>Sales: %{x:.1f}M<extra></extra>'
        ))
        fig_per.update_traces(marker_cornerradius=4)
        fig_per.update_layout(
            **base_layout(
                height=300,
                xaxis=xax({'title': 'Total Sales (M)'}),
                yaxis=yax({'gridcolor': 'rgba(0,0,0,0)', 'categoryorder': 'total ascending'}),
            ),
            title=dict(text='⚠ Perishable Risk Categories', font=dict(size=12, color='#F5606A'), x=0)
        )
        st.plotly_chart(fig_per, use_container_width=True, config={'displayModeBar': False})


# ══════════════════════════════════════════════════════════════════════
# PAGE: FORECASTING MODEL
# ══════════════════════════════════════════════════════════════════════
elif "Model" in page:

    c1, c2, c3, c4 = st.columns(4)
    model_kpis = [
        ("Algorithm",       "LightGBM", "Gradient Boosting Trees",          "🌲", "#00C896"),
        ("Validation RMSLE","0.43",     "Last 28 days of train",             "📐", "#00C896"),
        ("Boost Rounds",    "1,000",    "Early stopping · patience 50",      "⚙️", "#F4A118"),
        ("Features Used",   "24",       "Lag, rolling, date, external",      "🔧", "#0f9dc2"),
    ]
    for col, (label, val, sub, icon, color) in zip([c1, c2, c3, c4], model_kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value" style="color:{color};font-size:{'20px' if label=='Algorithm' else '32px'};">{val}</div>
              <div class="kpi-sub">{sub}</div>
              <div class="kpi-glow">{icon}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Model Pipeline & Feature Importance</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9])
    with col1:
        steps = [
            ("1", "Data Merging",        "train + stores + oil + holidays + transactions into one combined DataFrame"),
            ("2", "Feature Engineering", "Lag features: 7d, 14d, 28d · Rolling means: 7d, 14d · Date parts: year, month, dow, weekofyear"),
            ("3", "Holiday Flags",       "is_national_holiday · is_local_holiday · is_event — binary features from holidays_events.csv"),
            ("4", "Label Encoding",      "family, city, state, store type → integer encodings for tree model compatibility"),
            ("5", "Train / Val Split",   "Last 28 days of training data held out for validation · rest used for training"),
            ("6", "LightGBM Training",   "MAE objective · learning rate 0.05 · 127 leaves · early stopping on val RMSE"),
            ("7", "Evaluation",          "RMSLE metric on validation set · predictions clipped to 0 minimum"),
            ("8", "Predict & Export",    "submission.csv with Aug 2017 forecasts for all store × family combinations"),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div class="pipeline-step">
                <div class="step-num">{num}</div>
                <div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        features = [
            ("sales_lag_7",        100, "#00C896"),
            ("sales_roll_14",       85, "#00C896"),
            ("sales_lag_14",        71, "#0f9dc2"),
            ("onpromotion",         52, "#0f9dc2"),
            ("oil_price",           38, "#F4A118"),
            ("transactions",        32, "#055475"),
            ("is_national_holiday", 24, "#F5606A"),
            ("dayofweek",           18, "#055475"),
        ]
        f_names  = [f[0] for f in features]
        f_vals   = [f[1] for f in features]
        f_colors = [f[2] for f in features]

        fig_feat = go.Figure(go.Bar(
            x=f_vals, y=f_names, orientation='h',
            marker_color=f_colors, marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{y}</b><br>Importance: %{x}%<extra></extra>'
        ))
        fig_feat.update_traces(marker_cornerradius=4)
        fig_feat.update_layout(
            **base_layout(
                height=310,
                xaxis=xax({'title': 'Relative Importance (%)', 'range': [0, 115]}),
                yaxis=yax({'gridcolor': 'rgba(0,0,0,0)', 'categoryorder': 'total ascending', 'tickfont': dict(family='Space Mono', size=10)}),
            ),
            title=dict(text='Feature Importance (Gain)', font=dict(size=12, color='#dce8f8'), x=0)
        )
        st.plotly_chart(fig_feat, use_container_width=True, config={'displayModeBar': False})

        st.markdown("""
        <div class="insight-box" style="margin-top:14px;">
          <div class="insight-icon">🎯</div>
          <div>
            <div class="insight-title">Why LightGBM?</div>
            <div class="insight-body">
              Handles 3M+ rows efficiently on a standard laptop. Naturally manages tabular data with mixed feature types.
              Captures non-linear interactions between promotions, holidays, and lag sales — outperforming ARIMA and
              classical approaches for multi-store, multi-family forecasting.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE: ERP INSIGHTS
# ══════════════════════════════════════════════════════════════════════
elif "ERP" in page:

    st.markdown('<div class="section-title">ERP System Design Recommendations</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
      <div class="insight-icon">📊</div>
      <div>
        <div class="insight-title">Key Finding</div>
        <div class="insight-body">
          Analysis of 3M+ transactions across 54 stores reveals that holidays, promotions, and oil prices are the three
          primary demand drivers. A centralized ERP system integrating these signals can reduce perishable shrinkage by
          pre-positioning stock and trigger automated replenishment based on forecasted demand.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    rec_data = [
        ("🏪", "POS → Warehouse Data Flow",  "Real-time sales data from all 54 stores must feed into the central warehouse daily via ERP integration layer.", "DFD Level 1"),
        ("📅", "Holiday Pre-stocking",        "Auto-increase inventory allocation by 25% before national holidays using calendar integration in the replenishment module.", "Inventory Module"),
        ("🏷️", "Promotion Sync",             "Sync promotion schedule with warehouse allocation — items on promotion need 619% more stock coverage.", "Procurement Module"),
        ("🥦", "Perishable Alert System",     "Automated low-stock alerts for PRODUCE, DAIRY, MEATS, BREAD/BAKERY — high shrinkage risk categories.", "Alert Engine"),
        ("🛢️", "Macro Price Monitoring",      "Integrate WTI oil price feed — when oil drops, consumer spending follows (r=−0.70). Use as a procurement slowdown signal.", "External Data Feed"),
        ("📦", "Cluster-Based Dispatch",      "Priority warehouse dispatch to high-demand store clusters. Type A & D stores have highest volume — allocate accordingly.", "Logistics Module"),
    ]

    cols = st.columns(3)
    for i, (icon, title, body, tag) in enumerate(rec_data):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="rec-card" style="margin-bottom:16px;">
                <div class="rec-icon">{icon}</div>
                <div class="rec-title">{title}</div>
                <div class="rec-body">{body}</div>
                <span class="rec-tag">{tag}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">SAD System Mapping</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_radar = go.Figure(go.Scatterpolar(
            r=[65, 95, 70, 55, 45, 98],
            theta=['Holidays','Promotions','Oil Price','Weekends','Transactions','Lag Sales'],
            fill='toself',
            fillcolor='rgba(0,200,150,0.12)',
            line=dict(color='#00C896', width=2.2),
            marker=dict(size=5, color='#00C896'),
            name='Impact Score',
            hovertemplate='<b>%{theta}</b><br>Score: %{r}<extra></extra>'
        ))
        fig_radar.update_layout(
            paper_bgcolor=PAPER_BG,
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=9, color='#6b8199'), range=[0,100]),
                angularaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=11, color='#9ab8cf'))
            ),
            font=dict(color=FONT_COLOR, family='DM Sans'),
            height=330, margin=dict(l=40, r=40, t=50, b=40),
            title=dict(text='Demand Driver Impact Scores', font=dict(size=12, color='#dce8f8'), x=0),
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    with col2:
        store_types = ['Type A','Type D','Type C','Type B','Type E']
        store_vals  = [353.0, 351.1, 164.4, 145.3, 59.8]
        rep_colors  = ['rgba(245,96,106,0.85)','rgba(245,96,106,0.7)','rgba(244,161,24,0.72)','rgba(15,107,138,0.7)','rgba(107,129,153,0.5)']
        fig_rep = go.Figure(go.Bar(
            x=store_vals, y=store_types, orientation='h',
            marker_color=rep_colors, marker=dict(line=dict(width=0)),
            hovertemplate='<b>%{y}</b><br>Predicted Demand: %{x}M<extra></extra>'
        ))
        fig_rep.update_traces(marker_cornerradius=5)
        fig_rep.update_layout(
            **base_layout(
                height=330,
                xaxis=xax({'title': 'Predicted Demand (M)'}),
                yaxis=yax({'gridcolor': 'rgba(0,0,0,0)', 'categoryorder': 'total ascending'}),
            ),
            title=dict(text='Replenishment Priority by Store Type', font=dict(size=12, color='#dce8f8'), x=0)
        )
        st.plotly_chart(fig_rep, use_container_width=True, config={'displayModeBar': False})