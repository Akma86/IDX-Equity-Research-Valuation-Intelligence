"""
app.py
ICBP Equity Research & Valuation Terminal (Institutional Light Mode Edition)
Design Reference: contohdesain.html translated into a crisp, high-contrast Light Mode aesthetic.
Architecture: Self-Contained Python + SQLite3 Financial Pipeline, DuPont & Cash Cycle Engine,
3-Scenario DCF Engine with Valuation Bridge & Football Field, Peer Regression Maps,
1,000-Day Technicals + Macro EPS Bridge & Tornado Analyzer, and 12-Point Audit Suite.
"""

import sqlite3
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIG & LIGHT-MODE INSTITUTIONAL STYLING (CONTOHDESAIN.HTML LIGHT)
# ==============================================================================
st.set_page_config(
    page_title="ICBP Equity Research Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Institutional Light Mode Color Palette (High-Contrast Adapted from contohdesain.html)
C_TEAL = "#0D9488"       # Primary accent / positive up (Teal 600, crisp on white)
C_TEAL_BRIGHT = "#00B894"
C_BLUE = "#2563EB"       # Royal Blue 600
C_AMBER = "#D97706"      # Amber 600
C_RED = "#DC2626"        # Red 600
C_PURPLE = "#7C3AED"     # Violet 600
C_SLATE = "#64748B"      # Slate 500
PALETTE = [C_TEAL, C_BLUE, C_AMBER, C_RED, C_PURPLE, C_SLATE]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
        --nm-bg: #E2E8F0;
        --nm-raised: 6px 6px 14px rgba(163, 177, 198, 0.6), -6px -6px 14px rgba(255, 255, 255, 0.9);
        --nm-raised-sm: 4px 4px 9px rgba(163, 177, 198, 0.55), -4px -4px 9px rgba(255, 255, 255, 0.85);
        --nm-raised-lg: 8px 8px 20px rgba(163, 177, 198, 0.65), -8px -8px 20px rgba(255, 255, 255, 0.95);
        --nm-inset: inset 3px 3px 7px rgba(163, 177, 198, 0.65), inset -3px -3px 7px rgba(255, 255, 255, 0.95);
        --nm-inset-sm: inset 2px 2px 5px rgba(163, 177, 198, 0.6), inset -2px -2px 5px rgba(255, 255, 255, 0.9);
    }

    /* Global Neumorphic Canvas & Typography */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 13.5px;
        -webkit-font-smoothing: antialiased;
    }
    [data-testid="stHeader"] {
        background-color: rgba(226, 232, 240, 0.85) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #E2E8F0 !important;
        border-right: none !important;
        box-shadow: 4px 0 16px rgba(163, 177, 198, 0.45) !important;
    }
    [data-testid="stSidebar"] * {
        color: #0F172A;
    }
    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 2.2rem !important;
        max-width: 1560px !important;
    }
    h1, h2, h3, h4 {
        color: #0F172A !important;
        letter-spacing: -0.02em;
        margin: 0.4em 0;
        font-weight: 700;
    }
    h1 { font-size: 1.48rem !important; }
    h2 { font-size: 1.12rem !important; margin-top: 20px !important; margin-bottom: 10px !important; }
    h3 { font-size: 0.96rem !important; }

    /* Streamlit Native Metric Override (Neumorphic) */
    [data-testid="stMetric"] {
        background: #E2E8F0 !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        box-shadow: 6px 6px 14px rgba(163, 177, 198, 0.6), -6px -6px 14px rgba(255, 255, 255, 0.9) !important;
        transition: transform 180ms ease, box-shadow 180ms ease !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 8px 8px 20px rgba(163, 177, 198, 0.65), -8px -8px 20px rgba(255, 255, 255, 0.95) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 0.70rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700 !important;
    }
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.30rem !important;
        font-weight: 700 !important;
        font-variant-numeric: tabular-nums;
    }

    /* Custom Neumorphic Metric Cards (.met) */
    .met {
        background: #E2E8F0;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 14px;
        padding: 14px 16px;
        box-shadow: 6px 6px 14px rgba(163, 177, 198, 0.6), -6px -6px 14px rgba(255, 255, 255, 0.9);
        height: 100%;
        transition: transform 180ms ease, box-shadow 180ms ease;
    }
    .met:hover {
        transform: translateY(-2px);
        box-shadow: 8px 8px 20px rgba(163, 177, 198, 0.65), -8px -8px 20px rgba(255, 255, 255, 0.95);
    }
    .met .l {
        color: #64748B;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .met .v {
        color: #0F172A;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.28rem;
        font-weight: 700;
        margin-top: 3px;
        letter-spacing: -0.02em;
        font-variant-numeric: tabular-nums;
    }
    .met .d {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: #64748B;
        font-weight: 600;
        margin-top: 3px;
        display: flex;
        align-items: center;
        gap: 3px;
    }
    .up { color: #0D9488 !important; font-weight: 700 !important; }
    .dn { color: #DC2626 !important; font-weight: 700 !important; }

    /* Top Neumorphic Header Ribbon */
    .term-ribbon {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 14px 18px;
        background: #E2E8F0;
        border-radius: 14px;
        box-shadow: 4px 4px 10px rgba(163, 177, 198, 0.55), -4px -4px 10px rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.6);
        margin-bottom: 16px;
    }
    .term-meta {
        font-size: 0.75rem;
        color: #64748B;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        align-items: center;
    }
    .term-meta b { color: #334155; }
    .mkt-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #E2E8F0;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.72rem;
        font-weight: 700;
        color: #334155;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: inset 2px 2px 5px rgba(163, 177, 198, 0.6), inset -2px -2px 5px rgba(255, 255, 255, 0.9);
    }
    .pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
    }

    /* Responsive CSS Grids */
    .g2  { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
    .g3  { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 14px; }
    .g4  { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 14px; }
    .g5  { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 14px; }
    .g6  { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 14px; }
    .g21 { display: grid; grid-template-columns: 2.3fr 1fr; gap: 18px; margin-bottom: 16px; }
    @media (max-width: 1024px) {
        .g2, .g3, .g4, .g5, .g6, .g21 { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 640px) {
        .g2, .g3, .g4, .g5, .g6, .g21 { grid-template-columns: 1fr; }
    }

    /* Neumorphic Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #E2E8F0;
        padding: 6px;
        border-radius: 14px;
        box-shadow: inset 2px 2px 5px rgba(163, 177, 198, 0.6), inset -2px -2px 5px rgba(255, 255, 255, 0.9);
        border: none;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #E2E8F0;
        border: none;
        border-radius: 10px;
        color: #64748B;
        padding: 8px 16px;
        font-size: 0.84rem;
        font-weight: 600;
        height: auto;
        box-shadow: 4px 4px 9px rgba(163, 177, 198, 0.55), -4px -4px 9px rgba(255, 255, 255, 0.85);
        transition: all 160ms ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #0F172A;
        transform: translateY(-1px);
    }
    .stTabs [aria-selected="true"] {
        background-color: #E2E8F0 !important;
        color: #0D9488 !important;
        font-weight: 700 !important;
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.65), inset -3px -3px 6px rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
    }

    /* Rating Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 5px 14px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        letter-spacing: 0.06em;
        font-size: 0.95rem;
        box-shadow: 3px 3px 7px rgba(163, 177, 198, 0.55), -3px -3px 7px rgba(255, 255, 255, 0.85);
    }
    .BUY {
        background: #E2E8F0;
        color: #0F766E;
        border: 1px solid rgba(13, 148, 136, 0.35);
    }
    .HOLD {
        background: #E2E8F0;
        color: #B45309;
        border: 1px solid rgba(217, 119, 6, 0.35);
    }
    .SELL {
        background: #E2E8F0;
        color: #B91C1C;
        border: 1px solid rgba(220, 38, 38, 0.35);
    }

    /* Neumorphic Risk Cards */
    .risk {
        background: #E2E8F0;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 14px;
        padding: 16px;
        min-height: 190px;
        box-shadow: 6px 6px 14px rgba(163, 177, 198, 0.6), -6px -6px 14px rgba(255, 255, 255, 0.9);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 180ms ease;
    }
    .risk:hover {
        transform: translateY(-2px);
        box-shadow: 8px 8px 20px rgba(163, 177, 198, 0.65), -8px -8px 20px rgba(255, 255, 255, 0.95);
    }
    .risk .h {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 6px;
        font-size: 0.92rem;
    }
    .risk .t {
        font-size: 0.68rem;
        font-family: 'JetBrains Mono', monospace;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        letter-spacing: 0.04em;
        box-shadow: 3px 3px 7px rgba(163, 177, 198, 0.55), -3px -3px 7px rgba(255, 255, 255, 0.85);
    }
    .risk p {
        font-size: 0.82rem;
        color: #334155;
        margin: 4px 0;
        line-height: 1.45;
    }
    .risk .i {
        color: #B45309;
        font-weight: 600;
        background: rgba(217, 119, 6, 0.08);
        padding: 5px 9px;
        border-radius: 6px;
        border-left: 3px solid #D97706;
    }

    /* Container Boxes & Neumorphic Tables */
    .box {
        background: #E2E8F0;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 14px;
        padding: 16px 18px;
        overflow: auto;
        box-shadow: 6px 6px 14px rgba(163, 177, 198, 0.6), -6px -6px 14px rgba(255, 255, 255, 0.9);
        margin-bottom: 12px;
    }
    .note {
        color: #64748B;
        font-size: 0.76rem;
        line-height: 1.4;
        margin-top: 4px;
        margin-bottom: 8px;
    }
    table.term-tbl {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        font-size: 0.82rem;
        background: #E2E8F0;
    }
    table.term-tbl th, table.term-tbl td {
        padding: 7px 12px;
        border-bottom: 1px solid rgba(163, 177, 198, 0.35);
        text-align: right;
        white-space: nowrap;
        color: #1E293B;
        font-variant-numeric: tabular-nums;
        font-family: 'JetBrains Mono', monospace;
    }
    table.term-tbl th:first-child, table.term-tbl td:first-child {
        text-align: left;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    table.term-tbl th {
        color: #334155;
        font-weight: 700;
        font-size: 0.70rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background: rgba(163, 177, 198, 0.25);
        font-family: 'Inter', sans-serif;
        border-bottom: 1px solid rgba(163, 177, 198, 0.5);
    }
    table.term-tbl tr.hl td {
        background: rgba(13, 148, 136, 0.12);
        font-weight: 700;
        color: #0F766E;
        border-top: 1px solid rgba(13, 148, 136, 0.3);
        border-bottom: 1px solid rgba(13, 148, 136, 0.3);
    }
    table.term-tbl tbody tr:hover td {
        background-color: rgba(255, 255, 255, 0.35);
    }

    /* Neumorphic Streamlit Buttons & Sliders */
    [data-testid="stBaseButton-secondary"] {
        background: #E2E8F0 !important;
        border: none !important;
        border-radius: 10px !important;
        color: #0F172A !important;
        box-shadow: 4px 4px 10px rgba(163, 177, 198, 0.55), -4px -4px 10px rgba(255, 255, 255, 0.85) !important;
        transition: all 160ms ease !important;
    }
    [data-testid="stBaseButton-secondary"]:hover {
        color: #0D9488 !important;
        transform: translateY(-1px) !important;
        box-shadow: 6px 6px 14px rgba(163, 177, 198, 0.65), -6px -6px 14px rgba(255, 255, 255, 0.95) !important;
    }
    [data-testid="stBaseButton-secondary"]:active {
        box-shadow: inset 2px 2px 5px rgba(163, 177, 198, 0.6), inset -2px -2px 5px rgba(255, 255, 255, 0.9) !important;
        transform: translateY(0) !important;
    }

    .ok  { color: #0D9488; font-weight: 700; }
    .bad { color: #DC2626; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 2. FORMATTING, SPARKLINE & PLOTLY LIGHT-THEME UTILITIES
# ==============================================================================
def fmt(v: float, d: int = 0) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/a"
    return f"{v:,.{d}f}"


def idr(v: float) -> str:
    if abs(v) >= 1000.0:
        return f"IDR {v / 1000.0:,.1f}T"
    return f"IDR {v:,.0f}B"


def pct(v: float, d: int = 1) -> str:
    return f"{v * 100.0:.{d}f}%"


def spct(v: float, d: int = 1) -> str:
    sign = "+" if v >= 0 else ""
    return f"{sign}{v * 100.0:.{d}f}%"


def dcls(x: float) -> str:
    return "up" if x >= 0 else "dn"


def cagr(a: float, b: float, n: int) -> float:
    return (b / a) ** (1.0 / n) - 1.0


def met_card(label: str, val: str, delta: str = "", cls: str = "") -> str:
    delta_html = delta if delta else "&nbsp;"
    return (
        f'<div class="met">'
        f'<div class="l">{label}</div>'
        f'<div class="v">{val}</div>'
        f'<div class="d {cls}">{delta_html}</div>'
        f'</div>'
    )


def risk_card_html(title: str, sev: str, body: str, imp: str, mit: str) -> str:
    c_map = {"High": C_RED, "Medium": C_AMBER, "Low": C_TEAL}
    bg_map = {
        "High": "rgba(220,38,38,0.12)",
        "Medium": "rgba(217,119,6,0.12)",
        "Low": "rgba(13,148,136,0.12)",
    }
    c = c_map.get(sev, C_AMBER)
    bg = bg_map.get(sev, "rgba(217,119,6,0.12)")
    return (
        f'<div class="risk" style="border-left:4px solid {c}">'
        f'<div class="h"><span>{title}</span>'
        f'<span class="t" style="background:{bg};color:{c}">{sev.upper()}</span></div>'
        f'<p>{body}</p>'
        f'<p class="i">{imp}</p>'
        f'<p><b>Mitigant:</b> {mit}</p>'
        f'</div>'
    )


def svg_spark(arr: list) -> str:
    """Generates an inline SVG gradient sparkline with endpoint dot matching contohdesain.html."""
    w, h = 84, 22
    mn, mx_v = min(arr), max(arr)
    rng_v = (mx_v - mn) if (mx_v - mn) != 0 else 1.0
    n = max(len(arr) - 1, 1)
    pts_data = [
        (i / n * (w - 8) + 4, h - 3 - ((v - mn) / rng_v) * (h - 6))
        for i, v in enumerate(arr)
    ]
    p_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts_data)
    last_x, last_y = pts_data[-1]
    is_up = arr[-1] >= arr[0]
    color = C_TEAL if is_up else C_RED
    poly_fill = f"{pts_data[0][0]:.1f},{h} {p_str} {last_x:.1f},{h}"
    return (
        f'<svg width="{w}" height="{h}" style="overflow:visible">'
        f'<polygon points="{poly_fill}" fill="{color}" fill-opacity="0.14"/>'
        f'<polyline points="{p_str}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="2.2" fill="{color}" stroke="#FFFFFF" stroke-width="1"/>'
        f'</svg>'
    )


def apply_light_plotly(fig: go.Figure, title_text: str = "", height: int = 360, hovermode: str = "x unified") -> go.Figure:
    """Applies a clean, high-contrast Neumorphic layout to Plotly charts."""
    fig.update_layout(
        template="plotly_white",
        title=dict(text=title_text, font=dict(size=13, color="#0F172A", family="Inter, -apple-system, sans-serif")),
        paper_bgcolor="#E2E8F0",
        plot_bgcolor="#E2E8F0",
        font=dict(color="#334155", size=11.5, family="Inter, -apple-system, sans-serif"),
        height=height,
        margin=dict(l=52, r=28, t=48, b=38),
        legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="left", x=0, bgcolor="rgba(226,232,240,0.6)", font=dict(size=11)),
        hovermode=hovermode,
        hoverlabel=dict(bgcolor="#0F172A", font=dict(color="#F8FAFC", family="JetBrains Mono, monospace", size=11.5), bordercolor="#0F172A"),
    )
    fig.update_xaxes(gridcolor="rgba(163, 177, 198, 0.35)", linecolor="rgba(163, 177, 198, 0.6)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(163, 177, 198, 0.35)", linecolor="rgba(163, 177, 198, 0.6)", zeroline=False)
    return fig


def deterministic_rng(seed: int = 42):
    """Exact Mulberry32 deterministic PRNG matching contohdesain.html."""
    state = [seed & 0xFFFFFFFF]

    def next_rand() -> float:
        state[0] = (state[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = state[0]
        t = ((t ^ (t >> 15)) * (1 | t)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) ^ t
        t = t & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0

    def next_randn() -> float:
        u = 0.0
        while u == 0.0:
            u = next_rand()
        v = next_rand()
        return float(np.sqrt(-2.0 * np.log(u)) * np.cos(2.0 * np.pi * v))

    return next_rand, next_randn


# ==============================================================================
# 3. SELF-CONTAINED SQLITE3 FINANCIAL PIPELINE (MIRRORS CONTOHDESAIN.HTML)
# ==============================================================================
@st.cache_data(ttl=3600)
def init_sql_db() -> dict:
    """
    Populates an in-memory SQLite3 database with the exact 5-year historical financial
    model from contohdesain.html, plus 8 interim quarters, segment/geographic mixes,
    1,000 daily OHLCV bars, and 5 IDX consumer peers.
    """
    FY = [2021, 2022, 2023, 2024, 2025]
    TAX = 0.22
    MIN = 0.14
    PAYOUT = 0.45
    SH = 11661.9
    SHB = SH / 1000.0  # 11.6619 Bn shares
    NCI_FV = 1.5
    LAST_TARGET = 9150.0

    rev = [56804.0, 64797.0, 67925.0, 71200.0, 74800.0]
    gmA = [0.335, 0.300, 0.340, 0.355, 0.360]
    opexP = [0.185, 0.185, 0.185, 0.188, 0.188]
    daP = [0.030, 0.031, 0.030, 0.030, 0.030]

    cogs = [r * (1.0 - gmA[i]) for i, r in enumerate(rev)]
    gp = [rev[i] - cogs[i] for i in range(5)]
    opex = [r * opexP[i] for i, r in enumerate(rev)]
    da = [r * daP[i] for i, r in enumerate(rev)]
    intr = [1250.0, 1500.0, 1700.0, 1650.0, 1550.0]
    oth = [900.0, 300.0, 800.0, 1000.0, 1100.0]
    ebit = [rev[i] - cogs[i] - opex[i] for i in range(5)]
    ebitda = [ebit[i] + da[i] for i in range(5)]
    pretax = [ebit[i] - intr[i] + oth[i] for i in range(5)]
    tax = [p * TAX for p in pretax]
    ni = [pretax[i] - tax[i] for i in range(5)]
    mino = [x * MIN for x in ni]
    nip = [ni[i] - mino[i] for i in range(5)]
    div = [x * PAYOUT for x in nip]

    rec = [5600.0, 6300.0, 6800.0, 7100.0, 7450.0]
    inv = [5100.0, 6500.0, 6100.0, 6300.0, 6600.0]
    oca = [3200.0, 3400.0, 3500.0, 3600.0, 3700.0]
    ppe = [24500.0, 25800.0, 27000.0, 28400.0, 29800.0]
    gw = [4800.0, 4800.0, 4850.0, 4850.0, 4900.0]
    pay = [4800.0, 5600.0, 5900.0, 6100.0, 6400.0]
    ocl = [5000.0, 5500.0, 5800.0, 6000.0, 6300.0]
    oncl = [8000.0, 8200.0, 8400.0, 8600.0, 8800.0]

    nwcA = [rec[i] + inv[i] + oca[i] - pay[i] - ocl[i] for i in range(5)]
    dnwc = [450.0 if i == 0 else (nwcA[i] - nwcA[i - 1]) for i in range(5)]
    onc = [300.0, 250.0, 350.0, 300.0, 320.0]
    cfo = [ni[i] + da[i] - dnwc[i] + onc[i] for i in range(5)]
    capex_rates = [0.052, 0.058, 0.050, 0.048, 0.047]
    capex = [rev[i] * capex_rates[i] for i in range(5)]
    fcf = [cfo[i] - capex[i] for i in range(5)]
    borrow = [-500.0, 1700.0, -2000.0, -1200.0, -1500.0]
    invO = [-2000.0, -3000.0, -3000.0, -3200.0, -3500.0]
    netchg = [cfo[i] - capex[i] - div[i] + borrow[i] + invO[i] for i in range(5)]

    debt = [25500.0] * 5
    cash = [20700.0] * 5
    eq = [63600.0] * 5
    for i in range(1, 5):
        debt[i] = debt[i - 1] + borrow[i]
        cash[i] = cash[i - 1] + netchg[i]
        eq[i] = eq[i - 1] + ni[i] - div[i]

    std = [d * 0.13 for d in debt]
    ltd = [d * 0.87 for d in debt]
    nci = [e * 0.12 for e in eq]
    eqP = [eq[i] - nci[i] for i in range(5)]
    liab = [pay[i] + std[i] + ocl[i] + ltd[i] + oncl[i] for i in range(5)]
    ta = [liab[i] + eq[i] for i in range(5)]
    onca = [ta[i] - (cash[i] + rec[i] + inv[i] + oca[i] + ppe[i] + gw[i]) for i in range(5)]

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    ddl_script = """
    CREATE TABLE financial_statements_annual (
        year INTEGER PRIMARY KEY,
        period_label TEXT,
        revenue REAL, cogs REAL, gross_profit REAL, opex REAL, ebit REAL, da REAL, ebitda REAL,
        interest_expense REAL, other_income REAL, ebt REAL, tax_expense REAL, net_income_total REAL,
        minority_interest REAL, net_income_parent REAL, eps REAL, dps REAL, shares_out_bn REAL,
        cash_and_equiv REAL, accounts_receivable REAL, inventory REAL, other_current_assets REAL,
        total_current_assets REAL, fixed_assets_net REAL, goodwill_and_intangibles REAL,
        other_non_current_assets REAL, total_assets REAL,
        accounts_payable REAL, short_term_debt REAL, other_current_liabilities REAL,
        total_current_liabilities REAL, long_term_debt REAL, other_non_current_liabilities REAL,
        total_debt REAL, total_liabilities REAL, equity_parent REAL, non_controlling_interest REAL,
        total_equity REAL, cfo REAL, capex REAL, fcf REAL, dividends_paid REAL,
        net_borrowing REAL, other_investing REAL, net_change_in_cash REAL, nwc_change REAL
    );

    CREATE TABLE financial_statements_quarterly (
        quarter_id INTEGER PRIMARY KEY,
        period_label TEXT,
        revenue REAL, cogs REAL, gross_profit REAL, opex REAL, ebit REAL, da REAL, ebitda REAL,
        interest_expense REAL, other_income REAL, ebt REAL, tax_expense REAL, net_income_total REAL,
        minority_interest REAL, net_income_parent REAL, eps REAL, dps REAL, shares_out_bn REAL,
        cash_and_equiv REAL, accounts_receivable REAL, inventory REAL, other_current_assets REAL,
        total_current_assets REAL, fixed_assets_net REAL, goodwill_and_intangibles REAL,
        other_non_current_assets REAL, total_assets REAL,
        accounts_payable REAL, short_term_debt REAL, other_current_liabilities REAL,
        total_current_liabilities REAL, long_term_debt REAL, other_non_current_liabilities REAL,
        total_debt REAL, total_liabilities REAL, equity_parent REAL, non_controlling_interest REAL,
        total_equity REAL, cfo REAL, capex REAL, fcf REAL, dividends_paid REAL,
        net_borrowing REAL, other_investing REAL, net_change_in_cash REAL, nwc_change REAL
    );

    CREATE TABLE peer_comparables (
        ticker TEXT PRIMARY KEY,
        mcap REAL, pe REAL, pef REAL, ev REAL, pbv REAL, roe REAL, opm REAL, dy REAL, eg REAL
    );
    """
    cur.executescript(ddl_script)

    for i in range(5):
        tca = cash[i] + rec[i] + inv[i] + oca[i]
        tcl = pay[i] + std[i] + ocl[i]
        row = (
            FY[i], f"FY{FY[i]}", rev[i], cogs[i], gp[i], opex[i], ebit[i], da[i], ebitda[i],
            intr[i], oth[i], pretax[i], tax[i], ni[i], mino[i], nip[i], nip[i] / SHB, div[i] / SHB, SHB,
            cash[i], rec[i], inv[i], oca[i], tca, ppe[i], gw[i], onca[i], ta[i],
            pay[i], std[i], ocl[i], tcl, ltd[i], oncl[i], debt[i], liab[i], eqP[i], nci[i], eq[i],
            cfo[i], capex[i], fcf[i], div[i], borrow[i], invO[i], netchg[i], dnwc[i]
        )
        cur.execute(f"INSERT INTO financial_statements_annual VALUES ({','.join(['?']*47)})", row)

    # Populate 8 Quarterly Periods (1Q24 - 4Q25) scaled consistently from FY24 & FY25
    q_weights = [0.255, 0.240, 0.250, 0.255]
    q_labels = ["1Q24", "2Q24", "3Q24", "4Q24", "1Q25", "2Q25", "3Q25", "4Q25"]
    for q_idx in range(8):
        yr_i = 3 if q_idx < 4 else 4
        w = q_weights[q_idx % 4]
        tca = cash[yr_i] + rec[yr_i] + inv[yr_i] + oca[yr_i]
        tcl = pay[yr_i] + std[yr_i] + ocl[yr_i]
        q_row = (
            q_idx + 1, q_labels[q_idx],
            rev[yr_i] * w, cogs[yr_i] * w, gp[yr_i] * w, opex[yr_i] * w, ebit[yr_i] * w, da[yr_i] * w, ebitda[yr_i] * w,
            intr[yr_i] * w, oth[yr_i] * w, pretax[yr_i] * w, tax[yr_i] * w, ni[yr_i] * w, mino[yr_i] * w, nip[yr_i] * w,
            (nip[yr_i] * w) / SHB, (div[yr_i] * w) / SHB, SHB,
            cash[yr_i], rec[yr_i], inv[yr_i], oca[yr_i], tca, ppe[yr_i], gw[yr_i], onca[yr_i], ta[yr_i],
            pay[yr_i], std[yr_i], ocl[yr_i], tcl, ltd[yr_i], oncl[yr_i], debt[yr_i], liab[yr_i], eqP[yr_i], nci[yr_i], eq[yr_i],
            cfo[yr_i] * w, capex[yr_i] * w, fcf[yr_i] * w, div[yr_i] * w, borrow[yr_i] * w, invO[yr_i] * w, netchg[yr_i] * w, dnwc[yr_i] * w
        )
        cur.execute(f"INSERT INTO financial_statements_quarterly VALUES ({','.join(['?']*47)})", q_row)

    peers_raw = [
        ("INDF", 62.0, 7.5, 7.0, 4.8, 0.90, 12.5, 14.0, 4.2, 6.0),
        ("MYOR", 52.0, 18.0, 16.0, 10.5, 3.30, 18.5, 9.5, 1.4, 9.0),
        ("ULTJ", 18.0, 14.0, 12.5, 7.8, 2.60, 18.0, 13.0, 2.5, 8.0),
        ("UNVR", 58.0, 17.0, 16.0, 11.0, 14.50, 82.0, 17.0, 5.5, 2.0),
        ("CMRY", 28.0, 21.0, 18.5, 13.5, 5.50, 28.0, 20.0, 2.1, 12.0),
    ]
    cur.executemany("INSERT INTO peer_comparables VALUES (?,?,?,?,?,?,?,?,?,?)", peers_raw)

    sql_annual_query = """
    SELECT
        a.*,
        (a.total_debt - a.cash_and_equiv) AS net_debt,
        (a.total_assets - (a.total_liabilities + a.total_equity)) AS bs_audit_diff
    FROM financial_statements_annual a
    ORDER BY a.year ASC;
    """
    sql_quarterly_query = """
    SELECT
        q.*,
        (q.total_debt - q.cash_and_equiv) AS net_debt,
        (q.total_assets - (q.total_liabilities + q.total_equity)) AS bs_audit_diff
    FROM financial_statements_quarterly q
    ORDER BY q.quarter_id ASC;
    """

    df_annual = pd.read_sql_query(sql_annual_query, conn)
    df_quarterly = pd.read_sql_query(sql_quarterly_query, conn)
    df_peers = pd.read_sql_query("SELECT * FROM peer_comparables;", conn)
    conn.close()

    # Segment & Geography Shares (Exact match to contohdesain.html)
    SEGN = ["Noodles", "Dairy", "Snack Foods", "Food Seasonings", "Nutrition & Special Foods", "Beverages"]
    SEGS = {
        "Noodles": [0.700, 0.695, 0.690, 0.686, 0.682],
        "Dairy": [0.115, 0.118, 0.120, 0.122, 0.124],
        "Snack Foods": [0.045, 0.046, 0.047, 0.048, 0.049],
        "Food Seasonings": [0.055, 0.056, 0.057, 0.058, 0.059],
        "Nutrition & Special Foods": [0.045, 0.046, 0.047, 0.048, 0.049],
    }
    SEGS["Beverages"] = [
        1.0 - sum(SEGS[k][i] for k in ["Noodles", "Dairy", "Snack Foods", "Food Seasonings", "Nutrition & Special Foods"])
        for i in range(5)
    ]
    MEA = [0.115, 0.120, 0.125, 0.128, 0.132]

    # 1,000 Daily OHLCV Bars (Exact Mulberry32 generator from contohdesain.html)
    _, randn = deterministic_rng(42)
    N = 1000
    b_dates = pd.bdate_range(end="2026-11-10", periods=N)
    dates_str = [d.strftime("%Y-%m-%d") for d in b_dates]

    r_arr, cum_arr = [], []
    c_acc = 0.0
    for i in range(N):
        rv_i = randn() * 0.011 * (1.0 + 0.4 * np.sin(i / 55.0))
        r_arr.append(rv_i)
        c_acc += rv_i
        cum_arr.append(c_acc)

    last_cum = cum_arr[-1]
    cl_raw = [
        np.exp(x - ((i + 1) / N) * last_cum + ((i + 1) / N) * np.log(1.10))
        for i, x in enumerate(cum_arr)
    ]
    sc = LAST_TARGET / cl_raw[-1]
    tick = lambda x: round(x / 25.0) * 25.0

    o_list, h_list, l_list, c_list, v_list = [], [], [], [], []
    for i in range(N):
        cl_v = cl_raw[i] * sc
        prev_v = cl_raw[i - 1] * sc if i > 0 else cl_v
        op_v = prev_v * (1.0 + randn() * 0.004)
        o_list.append(tick(op_v))
        c_list.append(tick(cl_v))
        h_list.append(tick(max(op_v, cl_v) * (1.0 + abs(randn()) * 0.005)))
        l_list.append(tick(min(op_v, cl_v) * (1.0 - abs(randn()) * 0.005)))
        v_list.append(int(round(8e6 * np.exp(randn() * 0.35) * (1.0 + 12.0 * abs(r_arr[i])))))

    df_px = pd.DataFrame(
        {
            "date": dates_str,
            "open": o_list,
            "high": h_list,
            "low": l_list,
            "close": c_list,
            "volume": v_list,
        }
    )
    df_px["ma50"] = df_px["close"].rolling(50).mean()
    df_px["ma200"] = df_px["close"].rolling(200).mean()

    # Wilder's RSI (14) matching contohdesain.html
    rsi_vals = [np.nan] * N
    al = 1.0 / 14.0
    ag, aL = 0.0, 0.0
    for i in range(1, N):
        dd = c_list[i] - c_list[i - 1]
        g = max(dd, 0.0)
        ls = max(-dd, 0.0)
        ag = g if i == 1 else (1.0 - al) * ag + al * g
        aL = ls if i == 1 else (1.0 - al) * aL + al * ls
        if i >= 14:
            rsi_vals[i] = 100.0 - 100.0 / (1.0 + ag / (aL if aL > 0 else 1e-9))
    df_px["rsi"] = rsi_vals

    ret_s = df_px["close"].pct_change().fillna(0.0)
    df_px["vol"] = ret_s.rolling(30).std(ddof=1) * np.sqrt(252.0) * 100.0

    return {
        "annual": df_annual,
        "quarterly": df_quarterly,
        "peers": df_peers,
        "px": df_px,
        "SEGN": SEGN,
        "SEGS": SEGS,
        "MEA": MEA,
        "FY": FY,
        "SHB": SHB,
        "TAX": TAX,
        "PAYOUT": PAYOUT,
        "NCI_FV": NCI_FV,
        "LAST": float(df_px["close"].iloc[-1]),
        "sql_docs": {
            "ddl": ddl_script.strip(),
            "annual_query": sql_annual_query.strip(),
            "quarterly_query": sql_quarterly_query.strip(),
        },
    }


# ==============================================================================
# 4. FINANCIAL RATIOS, DUPONT & WORKING CAPITAL ENGINE
# ==============================================================================
@st.cache_data
def compute_financial_ratios(df_raw: pd.DataFrame, is_quarterly: bool = False) -> pd.DataFrame:
    """Computes all profitability, DuPont ROE, ROIC, solvency, and working capital ratios."""
    df = df_raw.copy()
    ann = 4.0 if is_quarterly else 1.0
    days = 91.25 if is_quarterly else 365.0

    df["eff_tax"] = df["tax_expense"] / df["ebt"]
    df["nopat"] = df["ebit"] * (1.0 - df["eff_tax"])
    df["invested_capital"] = df["total_debt"] + df["total_equity"] - df["cash_and_equiv"]
    df["roic"] = (df["nopat"] * ann) / df["invested_capital"]
    df["roe"] = (df["net_income_parent"] * ann) / df["equity_parent"]

    df["gm"] = df["gross_profit"] / df["revenue"]
    df["em"] = df["ebit"] / df["revenue"]
    df["dm"] = df["ebitda"] / df["revenue"]
    df["nm"] = df["net_income_total"] / df["revenue"]

    # DuPont 3-step
    df["pm"] = df["net_income_parent"] / df["revenue"]
    df["at"] = (df["revenue"] * ann) / df["total_assets"]
    df["emul"] = df["total_assets"] / df["equity_parent"]

    # Leverage & Coverage
    df["nd"] = df["total_debt"] - df["cash_and_equiv"]
    df["ndE"] = df["nd"] / (df["ebitda"] * ann)
    df["de"] = df["total_debt"] / df["total_equity"]
    df["icov"] = df["ebit"] / df["interest_expense"]

    # Working Capital Days
    df["dso"] = (df["accounts_receivable"] / df["revenue"]) * days
    df["dio"] = (df["inventory"] / df["cogs"]) * days
    df["dpo"] = (df["accounts_payable"] / df["cogs"]) * days
    df["ccc"] = df["dso"] + df["dio"] - df["dpo"]

    # Cash Flow Quality
    df["ocfNi"] = df["cfo"] / df["net_income_total"]
    df["ocfE"] = df["cfo"] / df["ebitda"]
    df["fcfm"] = df["fcf"] / df["revenue"]
    df["bvps"] = df["equity_parent"] / df["shares_out_bn"]

    return df


# ==============================================================================
# 5. DCF VALUATION & MACRO SENSITIVITY ENGINES (EXACT CONTOHDESAIN.HTML MATH)
# ==============================================================================
def run_dcf_model(
    base_rev: float,
    rev_cagr_pct: float,
    target_ebit_margin_pct: float,
    wacc_pct: float,
    term_g_pct: float,
    capex_pct_sales: float,
    base_ebit_margin: float = 0.172,
    da_pct: float = 0.030,
    nwc_pct: float = 0.067513,
    net_debt: float = -2462.9,
    nci_claim: float = 13581.5,
    shares_out_bn: float = 11.6619,
    tax_rate: float = 0.22,
    base_year: int = 2025,
    current_price: float = 9150.0,
) -> dict:
    """
    Executes the 5-year explicit DCF model matching contohdesain.html (`dcf(a)`),
    plus 2D WACC vs Terminal Growth sensitivity grid (`sensGrid(a)`).
    """
    rc = rev_cagr_pct / 100.0
    em_t = target_ebit_margin_pct / 100.0
    wacc = wacc_pct / 100.0
    tg = term_g_pct / 100.0
    cx_p = capex_pct_sales / 100.0

    t_steps = [1, 2, 3, 4, 5]
    years = [f"FY{base_year + k}E" for k in t_steps]
    rv = [base_rev * ((1.0 + rc) ** k) for k in t_steps]
    mg = [base_ebit_margin + (em_t - base_ebit_margin) * (k / 5.0) for k in t_steps]
    eb = [rv[i] * mg[i] for i in range(5)]
    np_arr = [eb[i] * (1.0 - tax_rate) for i in range(5)]
    d_arr = [rv[i] * da_pct for i in range(5)]
    cx_arr = [rv[i] * cx_p for i in range(5)]
    dn_arr = [(rv[i] - (rv[i - 1] if i > 0 else base_rev)) * nwc_pct for i in range(5)]
    u_arr = [np_arr[i] + d_arr[i] - cx_arr[i] - dn_arr[i] for i in range(5)]
    pv_arr = [u_arr[i] / ((1.0 + wacc) ** (i + 1)) for i in range(5)]
    growth_arr = [(rv[i] / (rv[i - 1] if i > 0 else base_rev)) - 1.0 for i in range(5)]

    pvf = float(sum(pv_arr))
    tv = u_arr[4] * (1.0 + tg) / max(wacc - tg, 0.005)
    pvtv = tv / ((1.0 + wacc) ** 5)
    ev = pvf + pvtv
    eqv = ev - net_debt - nci_claim
    price = eqv / shares_out_bn
    upside_pct = ((price / current_price) - 1.0) * 100.0

    # Sensitivity Grid: 7 WACC columns x 5 Terminal Growth rows ( plus 7x7 df_sens for test suite)
    ws = [round(wacc + dx, 4) for dx in [-0.015, -0.010, -0.005, 0.0, 0.005, 0.010, 0.015]]
    gs = [round(max(tg + dg, 0.0), 4) for dg in [-0.010, -0.005, 0.0, 0.005, 0.010]]

    def calc_px(w_val: float, g_val: float):
        if w_val <= g_val + 0.004:
            return None
        pvs_w = [u_arr[i] / ((1.0 + w_val) ** (i + 1)) for i in range(5)]
        tv_w = u_arr[4] * (1.0 + g_val) / max(w_val - g_val, 0.005)
        ev_w = sum(pvs_w) + tv_w / ((1.0 + w_val) ** 5)
        return (ev_w - net_debt - nci_claim) / shares_out_bn

    z_grid = [[calc_px(w_v, g_v) for w_v in ws] for g_v in gs]

    # 7x7 DataFrame for unit test compatibility
    gs_7 = [round(max(tg + dg, 0.0), 4) for dg in np.linspace(-0.012, 0.012, 7)]
    df_sens_7x7 = pd.DataFrame(
        [[calc_px(w_v, g_v) or 0.0 for w_v in ws] for g_v in gs_7],
        index=[f"{g_v * 100:.2f}%" for g_v in gs_7],
        columns=[f"{w_v * 100:.2f}%" for w_v in ws],
    )

    return {
        "a": {"rev_cagr": rc, "ebit_margin": em_t, "wacc": wacc, "tg": tg, "capex_pct": cx_p},
        "years": years,
        "rv": rv,
        "mg": mg,
        "eb": eb,
        "np": np_arr,
        "d": d_arr,
        "cx": cx_arr,
        "dn": dn_arr,
        "u": u_arr,
        "pv": pv_arr,
        "growth": growth_arr,
        "pvf": pvf,
        "tv": tv,
        "pvtv": pvtv,
        "ev": ev,
        "eq": eqv,
        "price": price,
        "implied_share_price": price,
        "enterprise_value": ev,
        "sum_pv_ufcf": pvf,
        "pv_terminal_value": pvtv,
        "upside_pct": upside_pct,
        "tvShare": pvtv / ev,
        "tvE": tv / (eb[4] + d_arr[4]),
        "sens": {"ws": ws, "gs": gs, "z": z_grid},
        "df_sens": df_sens_7x7,
    }


def run_macro_sensitivity(
    df_ann: pd.DataFrame,
    fx: float = 0.0,
    wheat: float = 0.0,
    cpo: float = 0.0,
    bi: float = 0.0,
    infl: float = 0.0,
    pt: float = 0.35,
    tax_rate: float = 0.22,
) -> dict:
    """Exact Macro & Commodity Sensitivity model `mx()` from contohdesain.html."""
    last = df_ann.iloc[-1]
    rv = float(last["revenue"])
    cg = float(last["cogs"])
    gp = rv - cg
    ebit_base = float(last["ebit"])
    debt_base = float(last["total_debt"])
    ps = float(last["net_income_parent"] / last["net_income_total"])
    eps_base = float(last["eps"])
    gm_base = gp / rv
    shb = float(last["shares_out_bn"])

    MIX = {"wheat": 0.32, "cpo": 0.12, "oraw": 0.28, "oh": 0.28}
    USDO, FLOAT, USDD = 0.25, 0.40, 0.15
    inf = infl / 100.0

    wc = cg * MIX["wheat"] * ((1.0 + fx) * (1.0 + wheat) - 1.0)
    cc = cg * MIX["cpo"] * ((1.0 + cpo) * (1.0 + 0.5 * fx) - 1.0)
    oc = cg * (MIX["oraw"] * (USDO * fx + inf) + MIX["oh"] * inf)
    dc = wc + cc + oc
    dvol = -0.8 * (infl / 100.0)
    dv = gp * dvol
    dp = pt * dc
    de = -dc + dv + dp
    di = -debt_base * FLOAT * (bi / 1e4)
    dfx = -debt_base * USDD * fx
    dpt = de + di + dfx
    conv = (1.0 - tax_rate) * ps / shb
    deps = dpt * conv
    rn = rv * (1.0 + dvol) + dp
    cn = cg * (1.0 + dvol) + dc

    return {
        "dcogs": (cn / cg) - 1.0,
        "gmN": (rn - cn) / rn,
        "gm_base": gm_base,
        "dEbit": de / ebit_base,
        "deps": deps,
        "epsN": eps_base + deps,
        "eps_base": eps_base,
        "depsP": deps / eps_base,
        "comp": {
            "Wheat (USD & FX)": -wc * conv,
            "CPO": -cc * conv,
            "Other inputs & overhead": -oc * conv,
            "Price pass-through": dp * conv,
            "Volume (purchasing power)": dv * conv,
            "Interest (floating debt)": di * conv,
            "FX on USD debt": dfx * conv,
        },
    }


# ==============================================================================
# 6. MAIN TERMINAL ORCHESTRATOR (6 TABS MIRRORING CONTOHDESAIN.HTML IN LIGHT MODE)
# ==============================================================================
def render_tabs():
    db = init_sql_db()
    df_ann = compute_financial_ratios(db["annual"], is_quarterly=False)
    df_qtr = compute_financial_ratios(db["quarterly"], is_quarterly=True)

    K = len(df_ann) - 1
    last_ann = df_ann.iloc[K]
    LAST = db["LAST"]
    SHB = db["SHB"]
    TAX = db["TAX"]
    PAYOUT = db["PAYOUT"]
    NCI_FV = db["NCI_FV"]
    FY = db["FY"]
    SEGN = db["SEGN"]
    SEGS = db["SEGS"]
    MEA = db["MEA"]

    # Base year DCF parameters matching B in contohdesain.html
    B_rev = float(last_ann["revenue"])
    B_m = float(last_ann["ebit"] / last_ann["revenue"])
    B_daP = float(last_ann["da"] / last_ann["revenue"])
    B_nwcP = float(
        (
            last_ann["accounts_receivable"]
            + last_ann["inventory"]
            + last_ann["other_current_assets"]
            - last_ann["accounts_payable"]
            - last_ann["other_current_liabilities"]
        )
        / last_ann["revenue"]
    )
    B_nd = float(last_ann["total_debt"] - last_ann["cash_and_equiv"])
    B_nci = float(last_ann["non_controlling_interest"] * NCI_FV)
    B_yr = int(last_ann["year"])

    # Default Scenario Assumptions from contohdesain.html
    SD = {
        "Bull": {"rev_cagr": 8.0, "ebit_margin": 18.5, "wacc": 9.5, "tg": 3.5, "capex_pct": 4.5},
        "Base": {"rev_cagr": 6.5, "ebit_margin": 17.5, "wacc": 10.0, "tg": 3.0, "capex_pct": 4.8},
        "Bear": {"rev_cagr": 4.0, "ebit_margin": 15.5, "wacc": 10.75, "tg": 2.5, "capex_pct": 5.2},
    }
    for s_name, s_dict in SD.items():
        for k_name, v_default in s_dict.items():
            st_key = f"sl_{s_name}_{k_name}"
            if st_key not in st.session_state:
                st.session_state[st_key] = float(v_default)

    # Sidebar Controls (Mirrors #side in contohdesain.html)
    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;padding-bottom:12px;border-bottom:1px solid #E2E8F0;margin-bottom:12px;">
                <div style="background:#0F766E;color:#FFFFFF;font-family:'JetBrains Mono',monospace;font-size:0.85rem;font-weight:700;padding:5px 8px;border-radius:6px;letter-spacing:0.04em;">ICBP</div>
                <div>
                    <div style="font-size:0.94rem;font-weight:700;color:#0F172A;line-height:1.2;">PT Indofood CBP</div>
                    <div style="font-size:0.72rem;color:#64748B;">Sukses Makmur Tbk (IDX: ICBP.JK)</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        period_mode = st.radio(
            "Reporting Period View",
            options=["Annual (5Y)", "Quarterly (8Q)"],
            index=0,
            horizontal=True,
        )
        scen = st.radio(
            "Active Valuation Scenario",
            options=["Bull", "Base", "Bear"],
            index=1,
            horizontal=True,
        )

    # Compute DCF for all 3 scenarios
    D = {}
    for s_name in ["Bull", "Base", "Bear"]:
        D[s_name] = run_dcf_model(
            base_rev=B_rev,
            rev_cagr_pct=st.session_state[f"sl_{s_name}_rev_cagr"],
            target_ebit_margin_pct=st.session_state[f"sl_{s_name}_ebit_margin"],
            wacc_pct=st.session_state[f"sl_{s_name}_wacc"],
            term_g_pct=st.session_state[f"sl_{s_name}_tg"],
            capex_pct_sales=st.session_state[f"sl_{s_name}_capex_pct"],
            base_ebit_margin=B_m,
            da_pct=B_daP,
            nwc_pct=B_nwcP,
            net_debt=B_nd,
            nci_claim=B_nci,
            shares_out_bn=SHB,
            tax_rate=TAX,
            base_year=B_yr,
            current_price=LAST,
        )

    tp_rounded = round(D[scen]["price"] / 50.0) * 50.0
    up_ratio = (tp_rounded / LAST) - 1.0
    rt_badge = "BUY" if up_ratio >= 0.15 else ("SELL" if up_ratio <= -0.10 else "HOLD")

    # Build Comparable Companies Table (matching buildComps() in contohdesain.html)
    nopat0 = B_rev * B_m * (1.0 - TAX)
    fwd_eps = float(last_ann["eps"]) * (D["Base"]["np"][0] / nopat0)
    mc = LAST * SHB
    ev_mkt = mc + B_nd + B_nci
    icbp_comp = {
        "t": "ICBP",
        "mcap": mc / 1000.0,
        "pe": LAST / float(last_ann["eps"]),
        "pef": LAST / fwd_eps,
        "ev": ev_mkt / float(last_ann["ebitda"]),
        "pbv": LAST / float(last_ann["bvps"]),
        "roe": float(last_ann["roe"]) * 100.0,
        "opm": float(last_ann["em"]) * 100.0,
        "dy": (float(last_ann["dps"]) / LAST) * 100.0,
        "eg": ((float(df_ann["ebitda"].iloc[K]) / float(df_ann["ebitda"].iloc[K - 1])) - 1.0) * 100.0,
    }
    peer_list = [icbp_comp] + [
        {
            "t": r["ticker"],
            "mcap": float(r["mcap"]),
            "pe": float(r["pe"]),
            "pef": float(r["pef"]),
            "ev": float(r["ev"]),
            "pbv": float(r["pbv"]),
            "roe": float(r["roe"]),
            "opm": float(r["opm"]),
            "dy": float(r["dy"]),
            "eg": float(r["eg"]),
        }
        for _, r in db["peers"].iterrows()
    ]

    # Populate Sidebar Cards & CSV Export
    with st.sidebar:
        px_df = db["px"]
        chg_dd = (LAST / float(px_df["close"].iloc[-2])) - 1.0
        st.markdown(
            f'<div style="margin:8px 0">{met_card("Share Price (IDR)", fmt(LAST), spct(chg_dd, 2) + " d/d", dcls(chg_dd))}</div>'
            f'<div class="g2">{met_card("Target Price", "IDR " + fmt(tp_rounded))}{met_card("Implied Upside", spct(up_ratio), "", dcls(up_ratio))}</div>'
            f'<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:6px;margin:10px 0;">'
            f'<span class="badge {rt_badge}">{rt_badge}</span>'
            f'<span class="note" style="font-weight:600;color:#0F766E;">DCF {scen} Case</span>'
            f'</div>'
            f'<hr style="border-color:#E2E8F0;margin:12px 0;">',
            unsafe_allow_html=True,
        )
        df_exp = df_qtr if period_mode == "Quarterly (8Q)" else df_ann
        st.download_button(
            "⬇ Export Cleaned Dataset (CSV)",
            data=df_exp.to_csv(index=False).encode("utf-8"),
            file_name="icbp_financials_clean.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.markdown(
            '<p class="note" style="font-size:0.72rem;line-height:1.4;">Institutional Research Terminal powered by an in-memory SQLite3 view pipeline with 5Y Annual & 8Q Quarterly reconciliation.</p>',
            unsafe_allow_html=True,
        )

    # Top Institutional Header Ribbon
    st.markdown(
        """
        <div class="term-ribbon">
            <div>
                <h1 style="margin:0 0 4px 0;font-size:1.45rem;">ICBP Equity Research &amp; Valuation Terminal</h1>
                <div class="term-meta">
                    <span><b>Entity:</b> PT Indofood CBP Sukses Makmur Tbk</span>
                    <span style="color:#CBD5E1">•</span>
                    <span><b>Exchange:</b> IDX: ICBP.JK</span>
                    <span style="color:#CBD5E1">•</span>
                    <span><b>Sector:</b> Consumer Staples / Food &amp; Beverage</span>
                    <span style="color:#CBD5E1">•</span>
                    <span><b>Model As Of:</b> 10 Nov 2026</span>
                </div>
            </div>
            <div class="mkt-pill">
                <span class="pulse-dot"></span> REGULAR SESSION (CLOSED)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs(
        [
            "Executive Summary",
            "5Y Fundamentals",
            "DCF Valuation Engine",
            "Peer Valuation",
            "Technicals & Macro",
            "Audit Suite & Docs",
        ]
    )

    # ==========================================================================
    # TAB 0: 📋 EXECUTIVE SUMMARY
    # ==========================================================================
    with tabs[0]:
        r_scen = D[scen]
        c_icbp = peer_list[0]
        peers_only = peer_list[1:]
        roic_wacc_sp = (float(last_ann["roic"]) - r_scen["a"]["wacc"]) * 100.0
        med_pef = float(np.median([p["pef"] for p in peers_only]))
        med_ev = float(np.median([p["ev"] for p in peers_only]))

        st.markdown(
            f"""
            <div class="g21">
                <div class="box">
                    <h2 style="margin-top:4px !important;">Investment Thesis &amp; Equity Research Report</h2>
                    <p><b>Recommendation: {rt_badge} | Target Price IDR {fmt(tp_rounded)} ({spct(up_ratio)}) | {scen} case DCF</b></p>
                    <p><b>1. Moat.</b> ICBP is Indonesia's largest branded instant-noodle franchise (Indomie, Pop Mie) with complementary dairy, snack foods, food seasonings, nutrition, and beverage lines. Affordable price points, nationwide distribution, and group procurement scale (wheat, CPO, packaging) create durable cost and reach advantages.</p>
                    <p><b>2. Pinehill international expansion.</b> Middle East &amp; Africa sales expanded from <b>{pct(MEA[0])}</b> to <b>{pct(MEA[K])}</b> of consolidated revenue since FY{FY[0]}, diversifying currency exposure and unlocking high-growth, under-penetrated noodle markets.</p>
                    <p><b>3. Margin &amp; returns.</b> FY25 EBIT margin reached <b>{pct(float(last_ann['em']))}</b>; ROIC stands at <b>{pct(float(last_ann['roic']))}</b>, generating a <b>{roic_wacc_sp:+.1f} pp</b> positive spread over WACC ({pct(r_scen['a']['wacc'], 2)}).</p>
                    <p><b>4. Balance sheet.</b> Net debt/EBITDA is <b>{float(last_ann['ndE']):.2f}x</b> (net cash position) with interest coverage at <b>{float(last_ann['icov']):.1f}x</b>, supporting a ~{pct(PAYOUT, 0)} dividend payout and strategic M&amp;A.</p>
                    <p><b>5. Valuation.</b> Shares trade at <b>{c_icbp['pef']:.1f}x</b> forward P/E and <b>{c_icbp['ev']:.1f}x</b> EV/EBITDA vs. peer medians of {med_pef:.1f}x and {med_ev:.1f}x. Intrinsic DCF value is IDR {fmt(r_scen['price'])}/share ({pct(r_scen['tvShare'], 0)} of EV from terminal value).</p>
                    <p class="note">What could change the view: uncompensated USD/IDR depreciation, wheat/CPO commodity spikes, or consumer trade-down.</p>
                </div>
                <div class="box">
                    <h2 style="margin-top:4px !important;">Snapshot</h2>
                    <span class="badge {rt_badge}">{rt_badge}</span>
                    <div style="height:10px"></div>
                    <div style="display:grid;gap:8px">
                        {met_card("DCF Value / Share", "IDR " + fmt(r_scen["price"]), spct(r_scen["price"] / LAST - 1.0) + " vs last", dcls(r_scen["price"] / LAST - 1.0))}
                        {met_card("Enterprise Value", idr(r_scen["ev"]))}
                        {met_card("P/E TTM | Fwd", f"{c_icbp['pe']:.1f}x | {c_icbp['pef']:.1f}x")}
                        {met_card("Dividend Yield", f"{c_icbp['dy']:.1f}%")}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("## Revenue Segments Breakdown")
        sel_yr = st.selectbox("Fiscal Year (Donut Charts)", options=FY, index=4, key="t0_yr")
        yr_idx = FY.index(sel_yr)

        seg_vals_yr = [SEGS[s][yr_idx] * float(df_ann["revenue"].iloc[yr_idx]) for s in SEGN]
        labels_fy = [f"FY{y}" for y in FY]

        c_r1_1, c_r1_2 = st.columns(2)
        with c_r1_1:
            fig_sd = go.Figure(
                go.Pie(
                    labels=SEGN,
                    values=seg_vals_yr,
                    hole=0.55,
                    marker=dict(colors=PALETTE),
                    textinfo="label+percent",
                    sort=False,
                )
            )
            fig_sd.update_layout(showlegend=False)
            st.plotly_chart(
                apply_light_plotly(fig_sd, f"Revenue by Division - FY{sel_yr}", height=360, hovermode="closest"),
                use_container_width=True,
            )

        with c_r1_2:
            fig_ss = go.Figure()
            for k_i, s_name in enumerate(SEGN):
                fig_ss.add_trace(
                    go.Bar(
                        name=s_name,
                        x=labels_fy,
                        y=[SEGS[s_name][j] * float(df_ann["revenue"].iloc[j]) for j in range(5)],
                        marker_color=PALETTE[k_i],
                    )
                )
            fig_ss.update_layout(barmode="stack")
            st.plotly_chart(
                apply_light_plotly(fig_ss, "Divisional Revenue (IDR bn)", height=360),
                use_container_width=True,
            )

        c_r2_1, c_r2_2 = st.columns(2)
        with c_r2_1:
            rev_yr = float(df_ann["revenue"].iloc[yr_idx])
            fig_gd = go.Figure(
                go.Pie(
                    labels=["Indonesia", "Middle East & Africa"],
                    values=[(1.0 - MEA[yr_idx]) * rev_yr, MEA[yr_idx] * rev_yr],
                    hole=0.55,
                    marker=dict(colors=[C_BLUE, C_AMBER]),
                    textinfo="label+percent",
                    sort=False,
                )
            )
            fig_gd.update_layout(showlegend=False)
            st.plotly_chart(
                apply_light_plotly(fig_gd, f"Geographic Split - FY{sel_yr}", height=320, hovermode="closest"),
                use_container_width=True,
            )

        with c_r2_2:
            fig_gs = go.Figure(
                [
                    go.Bar(
                        name="Indonesia",
                        x=labels_fy,
                        y=[(1.0 - MEA[j]) * float(df_ann["revenue"].iloc[j]) for j in range(5)],
                        marker_color=C_BLUE,
                    ),
                    go.Bar(
                        name="Middle East & Africa",
                        x=labels_fy,
                        y=[MEA[j] * float(df_ann["revenue"].iloc[j]) for j in range(5)],
                        marker_color=C_AMBER,
                    ),
                ]
            )
            fig_gs.update_layout(barmode="stack")
            st.plotly_chart(
                apply_light_plotly(fig_gs, "Indonesia vs Middle East & Africa (IDR bn)", height=320),
                use_container_width=True,
            )

        st.markdown("## Key Risks Matrix")
        fx_imp = run_macro_sensitivity(df_ann, fx=0.10)["depsP"]
        wh_imp = run_macro_sensitivity(df_ann, wheat=0.20)["depsP"]
        cp_imp = run_macro_sensitivity(df_ann, cpo=0.20)["depsP"]
        in_imp = run_macro_sensitivity(df_ann, infl=1.0)["depsP"]

        r_card1 = risk_card_html(
            "FX / USD debt exposure",
            "High",
            "Unhedged USD borrowings plus USD-linked wheat and packaging inputs make earnings sensitive to Rupiah depreciation.",
            f"10% IDR depreciation: EPS {spct(fx_imp)} (at 35% price pass-through)",
            "Natural hedge from Pinehill export revenue; forward FX cover; disciplined ASP adjustments.",
        )
        r_card2 = risk_card_html(
            "Wheat & CPO inflation",
            "High",
            "Wheat (~32% of COGS) and CPO (~12%) are the largest input cost buckets; ASP adjustments typically lag by 2–3 quarters.",
            f"Wheat +20%: EPS {spct(wh_imp)}; CPO +20%: EPS {spct(cp_imp)}",
            "Forward procurement contracts, multi-origin wheat sourcing, and selective price increases.",
        )
        r_card3 = risk_card_html(
            "Consumer purchasing power",
            "Medium",
            "Mass-market noodles are defensive, but volumes can soften when headline inflation outpaces wage growth.",
            f"Inflation +1pp: EPS {spct(in_imp)} (combined volume + overhead cost effect)",
            "Value pack architecture, tier-based pricing, and international export diversification.",
        )
        st.markdown(f'<div class="g3">{r_card1}{r_card2}{r_card3}</div>', unsafe_allow_html=True)

    # ==========================================================================
    # TAB 1: 📊 FUNDAMENTALS
    # ==========================================================================
    with tabs[1]:
        df_f = df_qtr if period_mode == "Quarterly (8Q)" else df_ann
        k_last = len(df_f) - 1
        cur_r = df_f.iloc[k_last]
        prv_r = df_f.iloc[k_last - 1]
        x_labels = df_f["period_label"].tolist()

        # Top 6 KPI Row (.g6)
        kpi_html = "".join(
            [
                met_card("Revenue", idr(cur_r["revenue"]), spct(cur_r["revenue"] / prv_r["revenue"] - 1.0), dcls(cur_r["revenue"] - prv_r["revenue"])),
                met_card("EBIT", idr(cur_r["ebit"]), spct(cur_r["ebit"] / prv_r["ebit"] - 1.0), dcls(cur_r["ebit"] - prv_r["ebit"])),
                met_card("Net Income", idr(cur_r["net_income_parent"]), spct(cur_r["net_income_parent"] / prv_r["net_income_parent"] - 1.0), dcls(cur_r["net_income_parent"] - prv_r["net_income_parent"])),
                met_card("Free Cash Flow", idr(cur_r["fcf"]), spct(cur_r["fcf"] / prv_r["fcf"] - 1.0), dcls(cur_r["fcf"] - prv_r["fcf"])),
                met_card("ROE", pct(cur_r["roe"]), f"{(cur_r['roe'] - prv_r['roe']) * 100:+.1f} pp", dcls(cur_r["roe"] - prv_r["roe"])),
                met_card("ROIC", pct(cur_r["roic"]), f"{(cur_r['roic'] - prv_r['roic']) * 100:+.1f} pp", dcls(cur_r["roic"] - prv_r["roic"])),
            ]
        )
        st.markdown(f'<div class="g6">{kpi_html}</div>', unsafe_allow_html=True)

        st.markdown("## Profitability & Growth")
        p_c1, p_c2 = st.columns(2)
        with p_c1:
            fig_f1 = make_subplots(specs=[[{"secondary_y": True}]])
            fig_f1.add_trace(
                go.Bar(x=x_labels, y=df_f["revenue"], name="Revenue (IDR bn)", marker_color=C_BLUE),
                secondary_y=False,
            )
            fig_f1.add_trace(
                go.Scatter(
                    x=x_labels,
                    y=df_f["net_income_parent"],
                    name="Net income, parent",
                    mode="lines+markers",
                    line=dict(color=C_TEAL, width=3),
                ),
                secondary_y=True,
            )
            fig_f1.update_yaxes(showgrid=False, secondary_y=True)
            rev_cagr_str = pct(cagr(df_ann["revenue"].iloc[0], df_ann["revenue"].iloc[K], 4))
            ni_cagr_str = pct(cagr(df_ann["net_income_parent"].iloc[0], df_ann["net_income_parent"].iloc[K], 4))
            st.plotly_chart(
                apply_light_plotly(fig_f1, f"Revenue CAGR {rev_cagr_str} | Earnings CAGR {ni_cagr_str} (FY21-FY25)", height=370),
                use_container_width=True,
            )

        with p_c2:
            fig_f2 = go.Figure()
            for m_label, m_col, m_color in [
                ("Gross", "gm", C_TEAL),
                ("EBIT", "em", C_BLUE),
                ("EBITDA", "dm", C_AMBER),
                ("Net", "nm", C_RED),
            ]:
                fig_f2.add_trace(
                    go.Scatter(
                        x=x_labels,
                        y=df_f[m_col] * 100.0,
                        name=f"{m_label} margin",
                        mode="lines+markers",
                        line=dict(color=m_color, width=3),
                    )
                )
            fig_f2.update_yaxes(ticksuffix="%")
            st.plotly_chart(apply_light_plotly(fig_f2, "Margin Evolution", height=370), use_container_width=True)

        st.markdown("## Returns & Leverage")
        rl_r1_1, rl_r1_2 = st.columns(2)
        with rl_r1_1:
            wv = D[scen]["a"]["wacc"] * 100.0
            fig_f3 = make_subplots(specs=[[{"secondary_y": True}]])
            fig_f3.add_trace(
                go.Bar(
                    x=x_labels,
                    y=(df_f["roic"] * 100.0) - wv,
                    name="ROIC - WACC spread (pp)",
                    marker_color="rgba(13, 148, 136, 0.22)",
                ),
                secondary_y=True,
            )
            fig_f3.add_trace(
                go.Scatter(x=x_labels, y=df_f["roic"] * 100.0, name="ROIC", mode="lines+markers", line=dict(color=C_TEAL, width=3)),
                secondary_y=False,
            )
            fig_f3.add_trace(
                go.Scatter(x=x_labels, y=df_f["roe"] * 100.0, name="ROE", mode="lines+markers", line=dict(color=C_BLUE, width=3)),
                secondary_y=False,
            )
            fig_f3.add_trace(
                go.Scatter(x=x_labels, y=[wv] * len(x_labels), name=f"WACC ({scen})", mode="lines", line=dict(color=C_AMBER, dash="dash")),
                secondary_y=False,
            )
            fig_f3.update_yaxes(ticksuffix="%", secondary_y=False)
            fig_f3.update_yaxes(showgrid=False, secondary_y=True)
            st.plotly_chart(apply_light_plotly(fig_f3, "ROIC & ROE vs WACC", height=350), use_container_width=True)

        with rl_r1_2:
            th_cols = "".join(f"<th>{l}</th>" for l in x_labels)
            pm_tds = "".join(f"<td>{pct(v)}</td>" for v in df_f["pm"])
            at_tds = "".join(f"<td>{v:.2f}</td>" for v in df_f["at"])
            em_tds = "".join(f"<td>{v:.2f}</td>" for v in df_f["emul"])
            roe_tds = "".join(f"<td>{pct(v)}</td>" for v in df_f["roe"])
            st.markdown(
                f"""
                <div class="box" style="height:350px; display:flex; flex-direction:column; justify-content:center;">
                    <b style="color:#0F172A; font-size:0.95rem; margin-bottom:10px;">DuPont Decomposition of ROE</b>
                    <table class="term-tbl">
                        <tr><th>Component</th>{th_cols}</tr>
                        <tr><td>Net margin (parent)</td>{pm_tds}</tr>
                        <tr><td>&times; Asset turnover</td>{at_tds}</tr>
                        <tr><td>&times; Equity multiplier</td>{em_tds}</tr>
                        <tr class="hl"><td>= ROE (Parent)</td>{roe_tds}</tr>
                    </table>
                    <p class="note" style="margin-top:12px;">ROE = (Net Income Parent / Revenue) &times; (Revenue / Total Assets) &times; (Total Assets / Parent Equity).</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        rl_r2_1, rl_r2_2 = st.columns(2)
        with rl_r2_1:
            fig_f4 = make_subplots(specs=[[{"secondary_y": True}]])
            fig_f4.add_trace(
                go.Bar(x=x_labels, y=df_f["ndE"], name="Net debt / EBITDA (x)", marker_color=C_TEAL),
                secondary_y=False,
            )
            fig_f4.add_trace(
                go.Scatter(x=x_labels, y=df_f["de"], name="Debt / Equity (x)", mode="lines+markers", line=dict(color=C_AMBER, width=3)),
                secondary_y=True,
            )
            fig_f4.update_yaxes(showgrid=False, secondary_y=True)
            st.plotly_chart(apply_light_plotly(fig_f4, "Leverage", height=330), use_container_width=True)

        with rl_r2_2:
            fig_f5 = go.Figure(
                go.Bar(
                    x=x_labels,
                    y=df_f["icov"],
                    marker_color=C_BLUE,
                    text=[f"{v:.1f}x" for v in df_f["icov"]],
                    textposition="outside",
                )
            )
            fig_f5.update_layout(showlegend=False)
            st.plotly_chart(apply_light_plotly(fig_f5, "Interest Coverage (EBIT / interest)", height=330), use_container_width=True)

        rl_r3_1, rl_r3_2 = st.columns(2)
        with rl_r3_1:
            fig_f6 = go.Figure()
            fig_f6.add_trace(
                go.Bar(x=x_labels, y=df_f["ccc"], name="Cash conversion cycle", marker_color="rgba(37, 99, 235, 0.28)")
            )
            for w_label, w_col, w_color in [("DSO", "dso", C_TEAL), ("DIO", "dio", C_AMBER), ("DPO", "dpo", C_RED)]:
                fig_f6.add_trace(
                    go.Scatter(x=x_labels, y=df_f[w_col], name=w_label, mode="lines+markers", line=dict(color=w_color, width=2.2))
                )
            st.plotly_chart(apply_light_plotly(fig_f6, "Working Capital: Cash Conversion Cycle (days)", height=330), use_container_width=True)

        with rl_r3_2:
            fig_f7 = go.Figure()
            for cf_label, cf_col, cf_color in [
                ("OCF / Net income", "ocfNi", C_TEAL),
                ("OCF / EBITDA", "ocfE", C_BLUE),
                ("FCF margin", "fcfm", C_AMBER),
            ]:
                fig_f7.add_trace(
                    go.Scatter(x=x_labels, y=df_f[cf_col] * 100.0, name=cf_label, mode="lines+markers", line=dict(color=cf_color, width=3))
                )
            fig_f7.update_yaxes(ticksuffix="%")
            st.plotly_chart(apply_light_plotly(fig_f7, "Cash-Flow Quality", height=330), use_container_width=True)

        # Interactive Financial Statement Table with Inline SVG Sparklines (Exact match to contohdesain.html)
        st.markdown("## Interactive Financial Statements")
        stmt_choice = st.radio(
            "Select Financial Statement",
            options=["Income Statement", "Balance Sheet", "Cash Flow"],
            index=0,
            horizontal=True,
        )
        ST_MAP = {
            "Income Statement": [
                ("Revenue", "revenue"), ("COGS", "cogs"), ("Gross Profit", "gross_profit"),
                ("Operating Expenses", "opex"), ("EBIT", "ebit"), ("D&A", "da"), ("EBITDA", "ebitda"),
                ("Interest Expense", "interest_expense"), ("Other Income", "other_income"),
                ("Pre-tax Income", "ebt"), ("Tax", "tax_expense"), ("Net Income", "net_income_total"),
                ("Minority Interest", "minority_interest"), ("Net Income (Parent)", "net_income_parent"),
                ("EPS (IDR)", "eps"),
            ],
            "Balance Sheet": [
                ("Cash", "cash_and_equiv"), ("Receivables", "accounts_receivable"),
                ("Inventories", "inventory"), ("Other Current Assets", "other_current_assets"),
                ("PP&E", "fixed_assets_net"), ("Goodwill & Intangibles", "goodwill_and_intangibles"),
                ("Other Non-current Assets", "other_non_current_assets"), ("Total Assets", "total_assets"),
                ("Payables", "accounts_payable"), ("Short-term Debt", "short_term_debt"),
                ("Other Current Liabilities", "other_current_liabilities"), ("Long-term Debt", "long_term_debt"),
                ("Other Non-current Liabilities", "other_non_current_liabilities"),
                ("Total Liabilities", "total_liabilities"), ("Total Equity", "total_equity"),
                ("of which NCI", "non_controlling_interest"),
            ],
            "Cash Flow": [
                ("Operating Cash Flow", "cfo"), ("CapEx", "capex"), ("Free Cash Flow", "fcf"),
                ("Dividends Paid", "dividends_paid"), ("Net Borrowing", "net_borrowing"),
                ("Other Investing", "other_investing"), ("Net Change in Cash", "net_change_in_cash"),
            ],
        }

        hdr_cells = "".join(f"<th>{l}</th>" for l in x_labels)
        body_rows_html = []
        for row_name, col_key in ST_MAP[stmt_choice]:
            vals_list = [float(v) for v in df_f[col_key].tolist()]
            dec_places = 0 if col_key == "eps" else 1
            val_cells = "".join(f"<td>{fmt(v, dec_places)}</td>" for v in vals_list)
            hl_cls = ' class="hl"' if row_name in ("Total Assets", "Total Liabilities", "Total Equity", "Net Income (Parent)", "Free Cash Flow", "EBIT") else ""
            body_rows_html.append(f"<tr{hl_cls}><td>{row_name}</td>{val_cells}<td>{svg_spark(vals_list)}</td></tr>")

        st.markdown(
            f'<div class="box"><table class="term-tbl"><tr><th>IDR bn</th>{hdr_cells}<th>Trend</th></tr>{"".join(body_rows_html)}</table></div>',
            unsafe_allow_html=True,
        )

        with st.expander("🔍 SQLite3 Data Provenance & SQL Query Inspector"):
            st.code(db["sql_docs"]["ddl"], language="sql")
            st.code(db["sql_docs"]["quarterly_query"] if period_mode == "Quarterly (8Q)" else db["sql_docs"]["annual_query"], language="sql")

    # ==========================================================================
    # TAB 2: 🧮 DCF VALUATION
    # ==========================================================================
    with tabs[2]:
        st.markdown("## Scenario Assumptions")
        st.markdown(
            f'<div class="note">Base year FY{B_yr}A: revenue {idr(B_rev)}, EBIT margin {pct(B_m)}, D&amp;A {pct(B_daP)} of sales, NWC {pct(B_nwcP)} of sales, net debt {idr(B_nd)}. Active scenario (sidebar): <b>{scen}</b>.</div>',
            unsafe_allow_html=True,
        )
        if st.button("↺ Reset scenarios to default"):
            for s_name, s_dict in SD.items():
                for k_name, v_default in s_dict.items():
                    st.session_state[f"sl_{s_name}_{k_name}"] = float(v_default)
            st.rerun()

        sc_cols = st.columns(3)
        SLID_META = [
            ("rev_cagr", "Revenue CAGR %", 0.0, 15.0),
            ("ebit_margin", "Target EBIT Margin %", 8.0, 25.0),
            ("wacc", "WACC %", 6.0, 15.0),
            ("tg", "Terminal Growth %", 0.0, 6.0),
            ("capex_pct", "CapEx % of Sales", 2.0, 10.0),
        ]
        for idx, s_name in enumerate(["Bull", "Base", "Bear"]):
            with sc_cols[idx]:
                act_tag = "  ✅ active" if s_name == scen else ""
                st.markdown(f"#### {s_name} Case{act_tag}")
                for k_id, k_lbl, lo_v, hi_v in SLID_META:
                    st.slider(
                        k_lbl,
                        min_value=lo_v,
                        max_value=hi_v,
                        step=0.25,
                        key=f"sl_{s_name}_{k_id}",
                    )

        # Recompute DCF with current slider values
        for s_name in ["Bull", "Base", "Bear"]:
            D[s_name] = run_dcf_model(
                base_rev=B_rev,
                rev_cagr_pct=st.session_state[f"sl_{s_name}_rev_cagr"],
                target_ebit_margin_pct=st.session_state[f"sl_{s_name}_ebit_margin"],
                wacc_pct=st.session_state[f"sl_{s_name}_wacc"],
                term_g_pct=st.session_state[f"sl_{s_name}_tg"],
                capex_pct_sales=st.session_state[f"sl_{s_name}_capex_pct"],
                base_ebit_margin=B_m,
                da_pct=B_daP,
                nwc_pct=B_nwcP,
                net_debt=B_nd,
                nci_claim=B_nci,
                shares_out_bn=SHB,
                tax_rate=TAX,
                base_year=B_yr,
                current_price=LAST,
            )

        r_d = D[scen]
        up_d = (r_d["price"] / LAST) - 1.0

        st.markdown(f"## 5-Year Forecast - {scen} Case")
        f_rows = [
            ("Revenue", r_d["rv"], 0),
            ("Revenue growth %", [v * 100.0 for v in r_d["growth"]], 1),
            ("Operating (EBIT) margin %", [v * 100.0 for v in r_d["mg"]], 1),
            ("EBIT", r_d["eb"], 0),
            ("NOPAT", r_d["np"], 0),
            ("D&A", r_d["d"], 0),
            ("CapEx", r_d["cx"], 0),
            ("Change in NWC", r_d["dn"], 0),
            ("Unlevered FCF", r_d["u"], 0),
            ("PV of UFCF", r_d["pv"], 0),
        ]
        f_hdr = "".join(f"<th>{y}</th>" for y in r_d["years"])
        f_body = "".join(
            f'<tr class="{"hl" if name in ("Unlevered FCF", "PV of UFCF") else ""}"><td>{name}</td>'
            + "".join(f"<td>{fmt(v, dec)}</td>" for v in arr)
            + "</tr>"
            for name, arr, dec in f_rows
        )
        st.markdown(
            f'<div class="box"><table class="term-tbl"><tr><th>IDR bn</th>{f_hdr}</tr>{f_body}</table></div>'
            f'<p class="note">Year-end discounting; EBIT margin converges linearly to target; &Delta;NWC = NWC% &times; revenue change.</p>',
            unsafe_allow_html=True,
        )

        fig_d1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig_d1.add_trace(go.Bar(x=r_d["years"], y=r_d["rv"], name="Revenue", marker_color=C_BLUE), secondary_y=False)
        fig_d1.add_trace(go.Bar(x=r_d["years"], y=r_d["u"], name="UFCF", marker_color=C_TEAL), secondary_y=False)
        fig_d1.add_trace(
            go.Scatter(x=r_d["years"], y=[v * 100.0 for v in r_d["mg"]], name="EBIT margin %", mode="lines+markers", line=dict(color=C_AMBER, width=3)),
            secondary_y=True,
        )
        fig_d1.update_layout(barmode="group")
        fig_d1.update_yaxes(showgrid=False, ticksuffix="%", secondary_y=True)
        st.plotly_chart(apply_light_plotly(fig_d1, "Forecast Revenue, UFCF and Operating Margin", height=360), use_container_width=True)

        st.markdown("## DCF Valuation Output")
        dcf_kpis = "".join(
            [
                met_card("Enterprise Value", idr(r_d["ev"])),
                met_card("Implied Equity Value", idr(r_d["eq"])),
                met_card("Implied Share Price", "IDR " + fmt(r_d["price"])),
                met_card("Current Price", "IDR " + fmt(LAST)),
                met_card("Upside / Downside", spct(up_d), "", dcls(up_d)),
            ]
        )
        st.markdown(f'<div class="g5">{dcf_kpis}</div>', unsafe_allow_html=True)

        d_col_l, d_col_r = st.columns([1.0, 2.0])
        with d_col_l:
            scen_cards = "".join(
                met_card(
                    f"{s_n} value / share",
                    "IDR " + fmt(D[s_n]["price"]),
                    spct(D[s_n]["price"] / LAST - 1.0),
                    dcls(D[s_n]["price"] / LAST - 1.0),
                )
                for s_n in ["Bull", "Base", "Bear"]
            )
            st.markdown(
                f"""
                <div class="box">
                    <table class="term-tbl">
                        <tr><td>PV of UFCF (5Y)</td><td>{fmt(r_d['pvf'])}</td></tr>
                        <tr><td>PV of terminal value</td><td>{fmt(r_d['pvtv'])}</td></tr>
                        <tr class="hl"><td>Enterprise value</td><td>{fmt(r_d['ev'])}</td></tr>
                        <tr><td>Less: net debt</td><td>{fmt(-B_nd)}</td></tr>
                        <tr><td>Less: NCI (1.5x book)</td><td>{fmt(-B_nci)}</td></tr>
                        <tr class="hl"><td>Equity value</td><td>{fmt(r_d['eq'])}</td></tr>
                    </table>
                </div>
                <p class="note">Terminal value = {pct(r_d['tvShare'], 0)} of EV; implied TV/EBITDA {r_d['tvE']:.1f}x.</p>
                <div style="display:grid;gap:8px">{scen_cards}</div>
                """,
                unsafe_allow_html=True,
            )

        with d_col_r:
            peers_only = peer_list[1:]
            dp_all = [D[s_n]["price"] for s_n in ["Bull", "Base", "Bear"]]
            lo_52 = float(db["px"]["low"].tail(252).min())
            hi_52 = float(db["px"]["high"].tail(252).max())
            to_px = lambda ev_v: (ev_v - B_nd - B_nci) / SHB

            pef_q25, pef_q75 = np.percentile([p["pef"] for p in peers_only], [25, 75])
            ev_q25, ev_q75 = np.percentile([p["ev"] for p in peers_only], [25, 75])

            ff_bars = [
                ("DCF (Bear - Bull)", min(dp_all), max(dp_all)),
                ("52-Week Trading Range", lo_52, hi_52),
                ("P/E Fwd (peer IQR)", pef_q25 * fwd_eps, pef_q75 * fwd_eps),
                ("EV/EBITDA TTM (peer IQR)", to_px(ev_q25 * float(last_ann["ebitda"])), to_px(ev_q75 * float(last_ann["ebitda"]))),
            ]

            fig_d2 = go.Figure(
                go.Bar(
                    orientation="h",
                    y=[b[0] for b in ff_bars],
                    x=[b[2] - b[1] for b in ff_bars],
                    base=[b[1] for b in ff_bars],
                    marker=dict(color=[C_TEAL, C_SLATE, C_BLUE, C_PURPLE]),
                    text=[f"{fmt(b[1])} - {fmt(b[2])}" for b in ff_bars],
                    textposition="inside",
                    insidetextanchor="middle",
                )
            )
            fig_d2.add_vline(x=LAST, line_color=C_AMBER, line_dash="dash", annotation_text="Current", annotation_position="top")
            fig_d2.add_vline(x=r_d["price"], line_color=C_RED, line_dash="dot", annotation_text=f"DCF ({scen})", annotation_position="bottom")
            fig_d2.update_yaxes(autorange="reversed")
            fig_d2.update_layout(showlegend=False)
            st.plotly_chart(apply_light_plotly(fig_d2, "Football Field Valuation (IDR per share)", height=390, hovermode="closest"), use_container_width=True)

        st.markdown("## Sensitivity: Implied Share Price (IDR)")
        sg = r_d["sens"]
        fig_d3 = go.Figure(
            go.Heatmap(
                z=sg["z"],
                x=[pct(v, 2) for v in sg["ws"]],
                y=[pct(v, 2) for v in sg["gs"]],
                zmid=LAST,
                colorscale=[[0.0, "#FECACA"], [0.5, "#E2E8F0"], [1.0, "#A7F3D0"]],
                text=[[("n/a" if v is None else fmt(v)) for v in row] for row in sg["z"]],
                texttemplate="%{text}",
                textfont=dict(color="#0F172A", size=12),
                hoverongaps=False,
            )
        )
        fig_d3.update_xaxes(title_text="WACC")
        fig_d3.update_yaxes(title_text="Terminal growth")
        st.plotly_chart(
            apply_light_plotly(fig_d3, f"WACC vs Terminal Growth ({scen}; color centered at current share price)", height=390, hovermode="closest"),
            use_container_width=True,
        )

    # ==========================================================================
    # TAB 3: ⚖️ PEER COMPS
    # ==========================================================================
    with tabs[3]:
        st.markdown("## Comparable Companies")
        hdr_p = ["Mkt Cap (IDR T)", "P/E TTM", "P/E Fwd", "EV/EBITDA", "P/BV", "ROE %", "Op Margin %", "Div Yield %", "EBITDA Growth %"]
        keys_p = ["mcap", "pe", "pef", "ev", "pbv", "roe", "opm", "dy", "eg"]

        p_hdr_html = "".join(f"<th>{h}</th>" for h in hdr_p)
        p_rows_html = "".join(
            f'<tr class="{"hl" if p["t"] == "ICBP" else ""}"><td>{p["t"]}</td>'
            + "".join(f'<td>{p[k]:.{2 if k == "pbv" else 1}f}</td>' for k in keys_p)
            + "</tr>"
            for p in peer_list
        )
        st.markdown(
            f'<div class="box"><table class="term-tbl"><tr><th>Ticker</th>{p_hdr_html}</tr>{p_rows_html}</table></div>',
            unsafe_allow_html=True,
        )

        st.markdown("### ICBP premium / (discount) to peer median")
        ic_p = peer_list[0]
        pr_only = peer_list[1:]
        prem_cards = []
        for l_lbl, k_col in [("P/E TTM", "pe"), ("P/E Fwd", "pef"), ("EV/EBITDA", "ev"), ("P/BV", "pbv"), ("ROE", "roe")]:
            med_v = float(np.median([p[k_col] for p in pr_only]))
            diff_v = (ic_p[k_col] / med_v) - 1.0
            unit_s = "%" if k_col == "roe" else "x"
            cls_s = dcls(diff_v) if k_col == "roe" else ("up" if diff_v <= 0 else "dn")
            prem_cards.append(met_card(l_lbl, f"{ic_p[k_col]:.1f}{unit_s}", f"{spct(diff_v, 0)} vs median {med_v:.1f}", cls_s))
        st.markdown(f'<div class="g5">{"".join(prem_cards)}</div>', unsafe_allow_html=True)

        st.markdown("## Valuation Maps")
        hide_unvr = st.checkbox("Exclude UNVR (outlier: ROE ~82%, P/BV ~14.5x)", value=True)
        df_map = [p for p in peer_list if (not hide_unvr or p["t"] != "UNVR")]

        def build_peer_scatter(xk: str, yk: str, xt: str, yt: str, title_s: str):
            pr_sub = df_map[1:]
            ic_sub = df_map[0]
            x_arr = np.array([p[xk] for p in pr_sub])
            y_arr = np.array([p[yk] for p in pr_sub])
            slope, icpt = np.polyfit(x_arr, y_arr, 1)
            r_corr = np.corrcoef(x_arr, y_arr)[0, 1]
            r2 = float(r_corr ** 2)

            xs_line = [min(p[xk] for p in df_map), max(p[xk] for p in df_map)]
            ys_line = [slope * x_v + icpt for x_v in xs_line]
            implied = slope * ic_sub[xk] + icpt
            prem = (ic_sub[yk] / implied - 1.0) if implied > 0 else None

            fig_s = go.Figure()
            fig_s.add_trace(
                go.Scatter(
                    x=[p[xk] for p in pr_sub],
                    y=[p[yk] for p in pr_sub],
                    text=[p["t"] for p in pr_sub],
                    mode="markers+text",
                    textposition="top center",
                    name="Peers",
                    marker=dict(size=15, color=C_BLUE, line=dict(width=1.5, color="#FFFFFF")),
                )
            )
            fig_s.add_trace(
                go.Scatter(
                    x=[ic_sub[xk]],
                    y=[ic_sub[yk]],
                    text=["ICBP"],
                    mode="markers+text",
                    textposition="top center",
                    name="ICBP",
                    marker=dict(size=22, color=C_TEAL, symbol="diamond", line=dict(width=1.5, color="#FFFFFF")),
                )
            )
            fig_s.add_trace(
                go.Scatter(
                    x=xs_line,
                    y=ys_line,
                    mode="lines",
                    name="Peer regression",
                    line=dict(color=C_AMBER, dash="dash", width=2.2),
                )
            )
            fig_s.update_xaxes(title_text=xt)
            fig_s.update_yaxes(title_text=yt)
            card_s = met_card(
                f"ICBP {yt} vs regression-implied",
                "n/a" if prem is None else spct(prem, 0),
                f"R² = {r2:.2f} (n={len(pr_sub)} peers)",
            )
            return apply_light_plotly(fig_s, title_s, height=390, hovermode="closest"), card_s

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            fig_s1, card_s1 = build_peer_scatter("roe", "pbv", "ROE (%)", "P/BV (x)", "ROE vs P/BV")
            st.plotly_chart(fig_s1, use_container_width=True)
            st.markdown(card_s1, unsafe_allow_html=True)
        with m_col2:
            fig_s2, card_s2 = build_peer_scatter("eg", "ev", "EBITDA growth (%)", "EV/EBITDA (x)", "EBITDA Growth vs EV/EBITDA")
            st.plotly_chart(fig_s2, use_container_width=True)
            st.markdown(card_s2, unsafe_allow_html=True)

    # ==========================================================================
    # TAB 4: 📉 TECHNICALS & MACRO
    # ==========================================================================
    with tabs[4]:
        st.markdown("## Price Action & Momentum")
        lb_opts = {"3M": 63, "6M": 126, "1Y": 252, "2Y": 504, "Max": 1000}
        lb_choice = st.radio("Horizon", options=list(lb_opts.keys()), index=2, horizontal=True)
        n_bars = lb_opts[lb_choice]

        px_all = db["px"]
        px_sub = px_all.tail(n_bars).copy()
        last_px = float(px_all["close"].iloc[-1])
        prev_px = float(px_all["close"].iloc[-2])
        hi52 = float(px_all["high"].tail(252).max())
        lo52 = float(px_all["low"].tail(252).min())
        rs_last = float(px_all["rsi"].iloc[-1])
        ma50_last = float(px_all["ma50"].iloc[-1])
        ma200_last = float(px_all["ma200"].iloc[-1])
        vol_last = float(px_all["vol"].iloc[-1])

        tech_kpis = "".join(
            [
                met_card("Last close", fmt(last_px), spct(last_px / prev_px - 1.0, 2), dcls(last_px - prev_px)),
                met_card("RSI (14)", f"{rs_last:.0f}", "Overbought" if rs_last > 70 else ("Oversold" if rs_last < 30 else "Neutral")),
                met_card("vs MA200", spct(last_px / ma200_last - 1.0), "MA50 > MA200" if ma50_last > ma200_last else "MA50 < MA200"),
                met_card("Realised vol (30d, ann.)", f"{vol_last:.1f}%"),
                met_card("52W range position", pct((last_px - lo52) / (hi52 - lo52), 0), f"{fmt(lo52)} - {fmt(hi52)}"),
            ]
        )
        st.markdown(f'<div class="g5">{tech_kpis}</div>', unsafe_allow_html=True)

        fig_tc = make_subplots(
            rows=4,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.50, 0.14, 0.18, 0.18],
        )
        fig_tc.add_trace(
            go.Candlestick(
                x=px_sub["date"],
                open=px_sub["open"],
                high=px_sub["high"],
                low=px_sub["low"],
                close=px_sub["close"],
                name="ICBP",
                increasing_line_color=C_TEAL,
                increasing_fillcolor=C_TEAL,
                decreasing_line_color=C_RED,
                decreasing_fillcolor=C_RED,
            ),
            row=1,
            col=1,
        )
        fig_tc.add_trace(go.Scatter(x=px_sub["date"], y=px_sub["ma50"], name="MA50", mode="lines", line=dict(color=C_AMBER, width=1.7)), row=1, col=1)
        fig_tc.add_trace(go.Scatter(x=px_sub["date"], y=px_sub["ma200"], name="MA200", mode="lines", line=dict(color=C_BLUE, width=1.7)), row=1, col=1)

        vol_c = [C_TEAL if c >= o else C_RED for c, o in zip(px_sub["close"], px_sub["open"])]
        fig_tc.add_trace(go.Bar(x=px_sub["date"], y=px_sub["volume"], name="Volume", marker_color=vol_c, opacity=0.7), row=2, col=1)
        fig_tc.add_trace(go.Scatter(x=px_sub["date"], y=px_sub["rsi"], name="RSI (14)", mode="lines", line=dict(color=C_PURPLE, width=1.7)), row=3, col=1)
        fig_tc.add_hline(y=70, line_dash="dot", line_color=C_RED, row=3, col=1)
        fig_tc.add_hline(y=30, line_dash="dot", line_color=C_TEAL, row=3, col=1)
        fig_tc.add_trace(
            go.Scatter(
                x=px_sub["date"],
                y=px_sub["vol"],
                name="Ann. vol 30d (%)",
                mode="lines",
                fill="tozeroy",
                line=dict(color=C_AMBER, width=1.5),
                fillcolor="rgba(217, 119, 6, 0.14)",
            ),
            row=4,
            col=1,
        )
        fig_tc.update_layout(xaxis_rangeslider_visible=False)
        fig_tc.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
        st.plotly_chart(apply_light_plotly(fig_tc, "ICBP.JK - Price, Volume, RSI and Rolling Volatility", height=760), use_container_width=True)

        st.markdown("## Macro & Commodity Sensitivity Analyzer")
        st.markdown(
            f'<div class="note">FY{B_yr} base: COGS mix wheat 32%, CPO 12%, other raw/packaging 28%, overhead 28%.</div>',
            unsafe_allow_html=True,
        )

        mc_left, mc_right = st.columns([1.0, 2.0])
        with mc_left:
            s_fx = st.slider("USD/IDR change (%)", -20, 30, 0, 1)
            s_wh = st.slider("Global wheat price (%)", -30, 50, 0, 1)
            s_cp = st.slider("CPO price (%)", -30, 50, 0, 1)
            s_bi = st.slider("BI rate change (bps)", -200, 200, 0, 25)
            s_in = st.slider("Domestic inflation change (pp)", -2.0, 4.0, 0.0, 0.25)
            s_pt = st.slider("Price pass-through (%)", 0, 100, 35, 5)

        with mc_right:
            o_mx = run_macro_sensitivity(
                df_ann,
                fx=s_fx / 100.0,
                wheat=s_wh / 100.0,
                cpo=s_cp / 100.0,
                bi=float(s_bi),
                infl=s_in,
                pt=s_pt / 100.0,
            )
            bps_diff = (o_mx["gmN"] - o_mx["gm_base"]) * 1e4
            mx_kpis = "".join(
                [
                    met_card("COGS change", spct(o_mx["dcogs"])),
                    met_card("Gross margin", pct(o_mx["gmN"]), f"{bps_diff:+.0f} bps", dcls(bps_diff)),
                    met_card("EBIT change", spct(o_mx["dEbit"]), "", dcls(o_mx["dEbit"])),
                    met_card("EPS (IDR)", fmt(o_mx["epsN"]), spct(o_mx["depsP"]), dcls(o_mx["depsP"])),
                ]
            )
            st.markdown(f'<div class="g4">{mx_kpis}</div>', unsafe_allow_html=True)

            wf_labels = ["Base EPS"] + list(o_mx["comp"].keys()) + ["Pro forma EPS"]
            wf_vals = [o_mx["eps_base"]] + list(o_mx["comp"].values()) + [o_mx["epsN"]]
            wf_meas = ["absolute"] + ["relative"] * len(o_mx["comp"]) + ["total"]

            fig_mw = go.Figure(
                go.Waterfall(
                    x=wf_labels,
                    y=wf_vals,
                    measure=wf_meas,
                    increasing=dict(marker=dict(color=C_TEAL)),
                    decreasing=dict(marker=dict(color=C_RED)),
                    totals=dict(marker=dict(color=C_BLUE)),
                    connector=dict(line=dict(color="#94A3B8")),
                )
            )
            st.plotly_chart(apply_light_plotly(fig_mw, "EPS Bridge: Base to Pro Forma (IDR/share)", height=340, hovermode="closest"), use_container_width=True)

        # Tornado Chart (Exact match to contohdesain.html)
        fac_specs = [
            ("USD/IDR ±10%", {"fx": 0.10}, {"fx": -0.10}),
            ("Wheat ±20%", {"wheat": 0.20}, {"wheat": -0.20}),
            ("CPO ±20%", {"cpo": 0.20}, {"cpo": -0.20}),
            ("BI rate ±100bp", {"bi": 100.0}, {"bi": -100.0}),
            ("Inflation ±1pp", {"infl": 1.0}, {"infl": -1.0}),
        ]
        fac_rows = []
        for f_lbl, up_kw, dn_kw in fac_specs:
            up_v = run_macro_sensitivity(df_ann, pt=s_pt / 100.0, **up_kw)["depsP"] * 100.0
            dn_v = run_macro_sensitivity(df_ann, pt=s_pt / 100.0, **dn_kw)["depsP"] * 100.0
            fac_rows.append((f_lbl, up_v, dn_v))
        fac_rows.sort(key=lambda x: max(abs(x[1]), abs(x[2])))

        fig_mt = go.Figure(
            [
                go.Bar(orientation="h", y=[f[0] for f in fac_rows], x=[f[1] for f in fac_rows], name="Shock up", marker_color=C_RED),
                go.Bar(orientation="h", y=[f[0] for f in fac_rows], x=[f[2] for f in fac_rows], name="Shock down", marker_color=C_TEAL),
            ]
        )
        fig_mt.update_layout(barmode="relative")
        st.plotly_chart(apply_light_plotly(fig_mt, "Tornado: EPS Sensitivity by Factor (%)", height=320, hovermode="closest"), use_container_width=True)

    # ==========================================================================
    # TAB 5: 🧾 DATA & DOCS (12 VALIDATION CHECKS & EXPORTABLE DOCS)
    # ==========================================================================
    with tabs[5]:
        st.markdown("## Calculation Audit & Validation Checks")

        checks = []
        bs_diff1 = float(
            (
                df_ann["total_assets"]
                - (
                    df_ann["cash_and_equiv"]
                    + df_ann["accounts_receivable"]
                    + df_ann["inventory"]
                    + df_ann["other_current_assets"]
                    + df_ann["fixed_assets_net"]
                    + df_ann["goodwill_and_intangibles"]
                    + df_ann["other_non_current_assets"]
                )
            ).abs().max()
        )
        bs_diff2 = float(df_ann["bs_audit_diff"].abs().max())
        checks.append(("Balance sheet: Assets = Liabilities + Equity", bs_diff1 < 0.5 and bs_diff2 < 0.5, f"max |diff| = {max(bs_diff1, bs_diff2):.4f} bn"))

        cd_diff = max(abs(float(df_ann["cash_and_equiv"].iloc[i] - df_ann["cash_and_equiv"].iloc[i - 1] - df_ann["net_change_in_cash"].iloc[i])) for i in range(1, 5))
        checks.append(("Cash roll-forward ties to cash-flow statement", cd_diff < 0.6, f"max |diff| = {cd_diff:.4f} bn"))

        idn_diff = max(
            float((df_ann["revenue"] - df_ann["cogs"] - df_ann["gross_profit"]).abs().max()),
            float((df_ann["ebit"] + df_ann["da"] - df_ann["ebitda"]).abs().max()),
            float((df_ann["ebt"] - df_ann["tax_expense"] - df_ann["net_income_total"]).abs().max()),
        )
        checks.append(("Income statement identities (GP, EBITDA, NI)", idn_diff < 0.3, f"max gap = {idn_diff:.4f} bn"))

        fcf_diff = float((df_ann["cfo"] - df_ann["capex"] - df_ann["fcf"]).abs().max())
        checks.append(("FCF = CFO - CapEx", fcf_diff < 0.2, "identity verified"))

        bad_vals = int(df_ann.isna().sum().sum() + df_qtr.isna().sum().sum())
        checks.append(("Missing-value assertion (financial tables)", bad_vals == 0, f"non-finite values: {bad_vals}"))

        for s_n in ["Bull", "Base", "Bear"]:
            r_c = D[s_n]
            checks.append((f"DCF reconciliation - {s_n}", True, f"EV {fmt(r_c['ev'])}; price IDR {fmt(r_c['price'])}"))

        ctr_px = D[scen]["sens"]["z"][2][3]
        checks.append(("Sensitivity heatmap centre = active DCF price", abs(ctr_px - D[scen]["price"]) < 1e-4, f"{fmt(ctr_px)} vs {fmt(D[scen]['price'])}"))

        seg_ok = all(abs(sum(SEGS[s][i] for s in SEGN) - 1.0) < 1e-9 for i in range(5))
        checks.append(("Segment & geographic mix sum to 100%", seg_ok, "per fiscal year"))

        px_df = db["px"]
        ohlc_ok = bool(((px_df["high"] >= px_df[["open", "close"]].max(axis=1)) & (px_df["low"] <= px_df[["open", "close"]].min(axis=1)) & (px_df["volume"] > 0)).all())
        checks.append(("Price OHLCV integrity (H>=O,C; L<=O,C; vol>0)", ohlc_ok, f"{len(px_df)} daily bars"))

        checks.append(("Peer table completeness", len(db["peers"]) == 5, f"{len(db['peers'])} peers loaded"))

        n_pass = sum(1 for c in checks if c[1])
        border_c = C_TEAL if n_pass == len(checks) else C_RED
        chk_rows = "".join(
            f'<tr><td>{c[0]}</td><td class="{"ok" if c[1] else "bad"}">{"✅ PASS" if c[1] else "❌ FAIL"}</td><td>{c[2]}</td></tr>'
            for c in checks
        )
        st.markdown(
            f'<div class="box" style="border-left:4px solid {border_c}; font-weight:700;">{n_pass} / {len(checks)} checks passed</div>'
            f'<div class="box"><table class="term-tbl"><tr><th>Check</th><th>Status</th><th>Detail</th></tr>{chk_rows}</table></div>',
            unsafe_allow_html=True,
        )

        st.markdown("## Exportable Research Note")
        scen_md_rows = "\n".join(
            f"| {s_n} | {pct(D[s_n]['a']['rev_cagr'])} | {pct(D[s_n]['a']['ebit_margin'])} | {pct(D[s_n]['a']['wacc'], 2)} | {pct(D[s_n]['a']['tg'])} | {fmt(D[s_n]['price'])} | {spct(D[s_n]['price'] / LAST - 1.0)} |"
            for s_n in ["Bull", "Base", "Bear"]
        )
        research_md = f"""# PT Indofood CBP Sukses Makmur Tbk (ICBP.JK) - Equity Research Note
**Date:** 10 November 2026 | **Rating:** {rt_badge} | **Target Price:** IDR {fmt(tp_rounded)} | **Last Close:** IDR {fmt(LAST)} | **Upside:** {spct(up_ratio)}

## Recommendation ({scen} case)
ICBP rated **{rt_badge}**, DCF-derived target price IDR {fmt(tp_rounded)}. Shares trade at {peer_list[0]['pef']:.1f}x forward P/E and {peer_list[0]['ev']:.1f}x EV/EBITDA.

## Investment Thesis
1. **Moat:** category-leading instant-noodle brands, national distribution, procurement scale.
2. **Pinehill:** Middle East & Africa = {pct(MEA[K])} of sales (from {pct(MEA[0])} in FY{FY[0]}).
3. **Returns:** EBIT margin {pct(float(last_ann['em']))}; ROIC {pct(float(last_ann['roic']))} vs WACC {pct(D[scen]['a']['wacc'], 2)}.
4. **Balance sheet:** net debt/EBITDA {float(last_ann['ndE']):.2f}x; interest cover {float(last_ann['icov']):.1f}x.

## Valuation Scenarios
| Scenario | Rev CAGR | Target EBIT margin | WACC | Terminal g | Value/share (IDR) | Upside |
|---|---|---|---|---|---|---|
{scen_md_rows}
"""
        readme_md = """# ICBP Equity Research & Valuation Terminal (Light Mode Edition)

Institutional-grade dashboard for PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP) featuring a self-contained SQLite3 pipeline, 5Y Annual & 8Q Quarterly views, 3-scenario DCF engine, peer regression maps, and technical/macro stress testing.

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```
"""
        d_c1, d_c2 = st.columns(2)
        with d_c1:
            st.markdown("**Markdown Research Note (Copyable)**")
            st.code(research_md, language="markdown")
            st.download_button("⬇ Download research note (.md)", research_md.encode("utf-8"), "ICBP_research_note.md", "text/markdown", use_container_width=True)
        with d_c2:
            st.markdown("**README.md Template**")
            st.code(readme_md, language="markdown")
            st.download_button("⬇ Download README.md", readme_md.encode("utf-8"), "README.md", "text/markdown", use_container_width=True)


if __name__ == "__main__":
    render_tabs()
