"""
ICBP Equity Research & Valuation Terminal
=========================================
PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP.JK)

Self-contained Streamlit dashboard. All data is SYNTHETIC (calibrated to ICBP's
approximate scale) and generated inside `init_sql_db()` into an in-memory SQLite
database. Raw tables hold IDR millions; SQL views clean/convert to IDR billions and
derive subtotals; pandas then computes ratios, DCF, technicals and macro sensitivities.

Run:  streamlit run app.py
"""
from __future__ import annotations

import sqlite3

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="ICBP Equity Research Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 0. CONSTANTS & STYLING
# =============================================================================
TICKER = "ICBP.JK"
COMPANY = "PT Indofood CBP Sukses Makmur Tbk"
AS_OF = pd.Timestamp("2026-11-10")
FISCAL_YEARS = [2021, 2022, 2023, 2024, 2025]
SHARES_MN = 11_661.9          # millions of shares
TAX_RATE = 0.22
MINORITY_SHARE = 0.14         # share of consolidated NI attributable to NCI
NCI_BOOK_PCT = 0.12           # NCI as % of total equity (book)
NCI_FV_MULT = 1.5             # NCI valued at 1.5x book in the EV->equity bridge
PAYOUT = 0.45
LAST_CLOSE_TARGET = 9_150.0

TEAL, BLUE, AMBER, RED = "#00F5D4", "#3B82F6", "#F59E0B", "#EF4444"
PALETTE = [TEAL, BLUE, AMBER, RED, "#8B5CF6", "#94A3B8"]
SCENARIOS = ["Bull", "Base", "Bear"]
SEGMENTS = ["Noodles", "Dairy", "Snack Foods", "Food Seasonings", "Nutrition & Special Foods", "Beverages"]
REGIONS = ["Indonesia", "Middle East & Africa"]

CSS = """
<style>
.block-container {padding-top: 1.1rem; padding-bottom: 1rem; max-width: 1550px;}
.stApp {background-color: #0B1220;}
.stApp, .stApp p, .stApp li, .stApp label, .stMarkdown {color: #E5E7EB;}
h1, h2, h3, h4 {color: #F8FAFC; letter-spacing: -0.01em;}
[data-testid="stSidebar"] {background: #0F172A; border-right: 1px solid #1F2A44;}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #111A2E, #0F172A);
    border: 1px solid #223052; border-radius: 10px;
    padding: 14px 16px; margin-bottom: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,.35);
}
[data-testid="stMetricLabel"] {color: #94A3B8; font-size: .75rem; text-transform: uppercase; letter-spacing: .05em;}
[data-testid="stMetricValue"] {color: #F8FAFC; font-size: 1.45rem;}
.stTabs [data-baseweb="tab-list"] {gap: 4px; border-bottom: 1px solid #223052;}
.stTabs [data-baseweb="tab"] {background: #0F172A; border-radius: 8px 8px 0 0; padding: 8px 16px; color: #94A3B8;}
.stTabs [aria-selected="true"] {background: #16233F; color: #00F5D4; border-bottom: 2px solid #00F5D4;}
.badge {display:inline-block; padding: 4px 16px; border-radius: 6px; font-weight: 800; letter-spacing: .08em; font-size: 1.05rem;}
.badge-BUY {background:#00F5D422; color:#00F5D4; border:1px solid #00F5D4;}
.badge-HOLD {background:#F59E0B22; color:#F59E0B; border:1px solid #F59E0B;}
.badge-SELL {background:#EF444422; color:#EF4444; border:1px solid #EF4444;}
.risk-card {background:#0F172A; border:1px solid #223052; border-radius:10px; padding:14px 16px; margin-bottom:12px; min-height: 210px;}
.risk-head {display:flex; justify-content:space-between; align-items:center; font-weight:700; color:#F8FAFC; margin-bottom:6px;}
.risk-card .tag {font-size:.7rem; padding:2px 8px; border-radius:4px; letter-spacing:.06em;}
.risk-card p {font-size:.85rem; margin: 4px 0; color:#CBD5E1;}
.risk-card .impact {color:#F59E0B; font-weight:600;}
.small-note {color:#94A3B8; font-size:.78rem;}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def style_fig(fig: go.Figure, height: int = 380, title: str | None = None, unified: bool = True) -> go.Figure:
    """Apply the shared institutional chart theme."""
    fig.update_layout(
        template="plotly_dark", height=height, colorway=PALETTE,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.55)",
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#E5E7EB"),
        margin=dict(l=10, r=10, t=55 if title else 25, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        title=dict(text=title, font=dict(size=14, color="#F8FAFC")) if title else None,
        hovermode="x unified" if unified else "closest",
    )
    fig.update_xaxes(gridcolor="#1F2A44", zeroline=False)
    fig.update_yaxes(gridcolor="#1F2A44", zeroline=False)
    return fig


def show_chart(fig: go.Figure, key: str | None = None) -> None:
    try:
        st.plotly_chart(fig, width="stretch", key=key)
    except Exception:
        st.plotly_chart(fig, use_container_width=True, key=key)


def show_df(df, **kwargs) -> None:
    try:
        st.dataframe(df, width="stretch", **kwargs)
    except Exception:
        st.dataframe(df, use_container_width=True, **kwargs)


def fmt_idr(v: float) -> str:
    return f"IDR {v / 1000:,.1f}T" if abs(v) >= 1000 else f"IDR {v:,.0f}B"


def cagr(first: float, last: float, periods: int) -> float:
    return (last / first) ** (1 / periods) - 1 if first > 0 and last > 0 and periods > 0 else float("nan")


# =============================================================================
# 1. SYNTHETIC DATA GENERATION
# =============================================================================
def _mn(x) -> np.ndarray:
    """IDR billions -> integer IDR millions (raw-table storage unit)."""
    return np.round(np.asarray(x, dtype=float) * 1000).astype("int64")


def _generate_annual() -> dict[str, pd.DataFrame]:
    n = len(FISCAL_YEARS)
    rev = np.array([56_804, 64_797, 67_925, 71_200, 74_800], dtype=float)
    cogs = rev * (1 - np.array([0.335, 0.300, 0.340, 0.355, 0.360]))
    opex = rev * np.array([0.185, 0.185, 0.185, 0.188, 0.188])
    da = rev * np.array([0.030, 0.031, 0.030, 0.030, 0.030])
    interest = np.array([1_250, 1_500, 1_700, 1_650, 1_550], dtype=float)
    other_inc = np.array([900, 300, 800, 1_000, 1_100], dtype=float)
    ebit = rev - cogs - opex
    pretax = ebit - interest + other_inc
    tax = pretax * TAX_RATE
    ni = pretax - tax
    minority = ni * MINORITY_SHARE
    dividends = (ni - minority) * PAYOUT

    rec = np.array([5_600, 6_300, 6_800, 7_100, 7_450], dtype=float)
    inv = np.array([5_100, 6_500, 6_100, 6_300, 6_600], dtype=float)
    oca = np.array([3_200, 3_400, 3_500, 3_600, 3_700], dtype=float)
    ppe = np.array([24_500, 25_800, 27_000, 28_400, 29_800], dtype=float)
    gw = np.array([4_800, 4_800, 4_850, 4_850, 4_900], dtype=float)
    pay = np.array([4_800, 5_600, 5_900, 6_100, 6_400], dtype=float)
    ocl = np.array([5_000, 5_500, 5_800, 6_000, 6_300], dtype=float)
    oncl = np.array([8_000, 8_200, 8_400, 8_600, 8_800], dtype=float)

    nwc = rec + inv + oca - pay - ocl
    d_nwc = np.diff(nwc, prepend=nwc[0] - 450.0)       # FY21 change assumed +450
    other_noncash = np.array([300, 250, 350, 300, 320], dtype=float)
    cfo = ni + da - d_nwc + other_noncash
    capex = rev * np.array([0.052, 0.058, 0.050, 0.048, 0.047])
    borrow = np.array([-500, 1_700, -2_000, -1_200, -1_500], dtype=float)
    inv_other = np.array([-2_000, -3_000, -3_000, -3_200, -3_500], dtype=float)

    debt = np.zeros(n)
    debt[0] = 25_500
    debt[1:] = debt[0] + np.cumsum(borrow[1:])
    st_debt, lt_debt = debt * 0.13, debt * 0.87

    net_change = cfo - capex - dividends + borrow + inv_other
    cash = np.zeros(n)
    cash[0] = 20_700
    cash[1:] = cash[0] + np.cumsum(net_change[1:])           # cash roll-forward ties to CF

    equity = np.zeros(n)
    equity[0] = 63_600
    equity[1:] = equity[0] + np.cumsum((ni - dividends)[1:])  # retained earnings roll-forward
    nci = equity * NCI_BOOK_PCT
    liabilities = pay + st_debt + ocl + lt_debt + oncl
    other_nca = liabilities + equity - (cash + rec + inv + oca + ppe + gw)  # balancing item

    income = pd.DataFrame({
        "fiscal_year": FISCAL_YEARS, "revenue_mn": _mn(rev), "cogs_mn": _mn(cogs), "opex_mn": _mn(opex),
        "da_mn": _mn(da), "interest_mn": _mn(interest), "other_income_mn": _mn(other_inc),
        "tax_mn": _mn(tax), "minority_mn": _mn(minority), "shares_mn": SHARES_MN,
    })
    balance = pd.DataFrame({
        "fiscal_year": FISCAL_YEARS, "cash_mn": _mn(cash), "receivables_mn": _mn(rec),
        "inventories_mn": _mn(inv), "other_ca_mn": _mn(oca), "ppe_mn": _mn(ppe), "goodwill_mn": _mn(gw),
        "other_nca_mn": _mn(other_nca), "payables_mn": _mn(pay), "st_debt_mn": _mn(st_debt),
        "other_cl_mn": _mn(ocl), "lt_debt_mn": _mn(lt_debt), "other_ncl_mn": _mn(oncl),
        "total_equity_mn": _mn(equity), "nci_mn": _mn(nci),
    })
    cashflow = pd.DataFrame({
        "fiscal_year": FISCAL_YEARS, "cfo_mn": _mn(cfo), "capex_mn": _mn(capex), "dividends_mn": _mn(dividends),
        "net_borrowing_mn": _mn(borrow), "other_investing_mn": _mn(inv_other),
    })
    return {"raw_income_statement": income, "raw_balance_sheet": balance, "raw_cash_flow": cashflow}


def _generate_quarterly() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    labels = ["2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]
    ends = ["2024-12-31", "2025-03-31", "2025-06-30", "2025-09-30",
            "2025-12-31", "2026-03-31", "2026-06-30", "2026-09-30"]
    season = np.array([0.245, 0.245, 0.255, 0.255])
    rev = np.concatenate([[71_200 * 0.255], 74_800 * season, 74_800 * season[:3] * np.array([1.062, 1.066, 1.070])])
    gm = np.array([0.352, 0.355, 0.358, 0.362, 0.365, 0.363, 0.366, 0.368]) + rng.normal(0, 0.002, 8)
    cogs = rev * (1 - gm)
    opex = rev * (0.188 + rng.normal(0, 0.002, 8))
    da = rev * 0.030
    interest = np.array([415, 400, 395, 390, 385, 380, 378, 375], dtype=float)
    other = np.array([240, 250, 260, 270, 280, 280, 285, 290], dtype=float)
    pretax = rev - cogs - opex - interest + other
    tax = pretax * TAX_RATE
    ni = pretax - tax
    cfo = (ni + da) * 0.93 + rng.normal(0, 100, 8)
    capex = rev * 0.047 * (1 + rng.normal(0, 0.05, 8))
    return pd.DataFrame({
        "period": labels, "period_end": ends, "revenue_mn": _mn(rev), "cogs_mn": _mn(cogs), "opex_mn": _mn(opex),
        "da_mn": _mn(da), "interest_mn": _mn(interest), "other_income_mn": _mn(other), "tax_mn": _mn(tax),
        "minority_mn": _mn(ni * MINORITY_SHARE), "shares_mn": SHARES_MN, "cfo_mn": _mn(cfo), "capex_mn": _mn(capex),
    })


def _generate_prices() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.bdate_range(end=AS_OF, periods=1_000)
    n = len(dates)
    vol = 0.011 * (1 + 0.4 * np.sin(np.arange(n) / 55))
    r = rng.normal(0, 1, n) * vol
    cum = np.cumsum(r)
    w = np.arange(1, n + 1) / n
    cum = cum - w * cum[-1] + w * np.log(1.10)               # Brownian bridge: ends +10% above start
    close = np.exp(cum)
    close = close / close[-1] * LAST_CLOSE_TARGET
    prev = np.roll(close, 1)
    prev[0] = close[0]
    open_ = prev * (1 + rng.normal(0, 0.004, n))
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.005, n)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.005, n)))
    tick = lambda x: np.round(x / 25) * 25                    # IDX tick size above IDR 5,000
    volume = (rng.lognormal(np.log(8e6), 0.35, n) * (1 + 12 * np.abs(r))).astype("int64")
    return pd.DataFrame({
        "trade_date": dates.strftime("%Y-%m-%d"), "open": tick(open_), "high": tick(high),
        "low": tick(low), "close": tick(close), "volume": volume,
    })


def _generate_macro() -> pd.DataFrame:
    rng = np.random.default_rng(11)
    m = 60
    idx = np.arange(m)
    dates = pd.date_range(end="2026-10-01", periods=m, freq="MS")
    smooth = lambda x: pd.Series(x).rolling(3, min_periods=1).mean().to_numpy()
    usdidr = smooth(np.linspace(14_300, 16_600, m) + rng.normal(0, 140, m))
    wheat = smooth(7.6 + 1.5 * np.sin(idx / 9) - idx / m * 1.5 + rng.normal(0, 0.25, m))
    cpo = smooth(900 + 120 * np.sin(idx / 7 + 1) + rng.normal(0, 35, m))
    bi = np.interp(idx, [0, 12, 30, 45, m - 1], [3.5, 3.5, 6.25, 6.25, 5.5])
    infl = np.clip(2.0 + 1.2 * np.sin(idx / 10) + rng.normal(0, 0.2, m), 1.2, None)
    return pd.DataFrame({
        "obs_date": dates.strftime("%Y-%m-%d"), "usdidr": np.round(usdidr, 0), "wheat_usd_bu": np.round(wheat, 2),
        "cpo_usd_t": np.round(cpo, 0), "bi_rate_pct": np.round(bi, 2), "inflation_yoy_pct": np.round(infl, 2),
    })


def _generate_peers() -> pd.DataFrame:
    rows = [
        ("INDF", "PT Indofood Sukses Makmur", 62.0, 7.5, 7.0, 4.8, 0.90, 12.5, 14.0, 4.2, 6.0),
        ("MYOR", "PT Mayora Indah", 52.0, 18.0, 16.0, 10.5, 3.30, 18.5, 9.5, 1.4, 9.0),
        ("ULTJ", "PT Ultrajaya Milk Industry", 18.0, 14.0, 12.5, 7.8, 2.60, 18.0, 13.0, 2.5, 8.0),
        ("UNVR", "PT Unilever Indonesia", 58.0, 17.0, 16.0, 11.0, 14.50, 82.0, 17.0, 5.5, 2.0),
        ("CMRY", "PT Cisarua Mountain Dairy", 28.0, 21.0, 18.5, 13.5, 5.50, 28.0, 20.0, 2.1, 12.0),
    ]
    return pd.DataFrame(rows, columns=["ticker", "name", "mcap_tn", "pe_ttm", "pe_fwd", "ev_ebitda", "pbv",
                                       "roe", "op_margin", "div_yield", "ebitda_growth"])


def _generate_mix() -> tuple[pd.DataFrame, pd.DataFrame]:
    shares = {
        "Noodles": [.700, .695, .690, .686, .682], "Dairy": [.115, .118, .120, .122, .124],
        "Snack Foods": [.045, .046, .047, .048, .049], "Food Seasonings": [.055, .056, .057, .058, .059],
        "Nutrition & Special Foods": [.045, .046, .047, .048, .049],
    }
    shares["Beverages"] = list(np.round(1 - np.sum(list(shares.values()), axis=0), 4))
    seg = pd.DataFrame([(y, s, float(v)) for s, vals in shares.items() for y, v in zip(FISCAL_YEARS, vals)],
                       columns=["fiscal_year", "segment", "share"])
    mea = np.array([0.115, 0.120, 0.125, 0.128, 0.132])
    geo = pd.DataFrame(
        [(y, "Indonesia", float(1 - m)) for y, m in zip(FISCAL_YEARS, mea)]
        + [(y, "Middle East & Africa", float(m)) for y, m in zip(FISCAL_YEARS, mea)],
        columns=["fiscal_year", "region", "share"])
    return seg, geo


# =============================================================================
# 2. SQL LAYER (raw tables -> cleaned views)
# =============================================================================
def _bn(expr: str, alias: str) -> str:
    """SQL fragment: IDR millions -> IDR billions, NULL-safe, rounded to 0.1bn."""
    return f"ROUND(COALESCE({expr}, 0) / 1000.0, 1) AS {alias}"


GP_MN = "(revenue_mn - cogs_mn)"
EBIT_MN = f"({GP_MN} - opex_mn)"
PRETAX_MN = f"({EBIT_MN} - interest_mn + other_income_mn)"
NI_MN = f"({PRETAX_MN} - tax_mn)"
NIP_MN = f"({NI_MN} - minority_mn)"
IS_SELECT = ",\n       ".join([
    _bn("revenue_mn", "revenue"), _bn("cogs_mn", "cogs"), _bn(GP_MN, "gross_profit"), _bn("opex_mn", "opex"),
    _bn(EBIT_MN, "ebit"), _bn("da_mn", "da"), _bn(f"({EBIT_MN} + da_mn)", "ebitda"),
    _bn("interest_mn", "interest_expense"), _bn("other_income_mn", "other_income"),
    _bn(PRETAX_MN, "pretax_income"), _bn("tax_mn", "tax"), _bn(NI_MN, "net_income"),
    _bn("minority_mn", "minority_interest"), _bn(NIP_MN, "net_income_parent"),
    f"ROUND({NIP_MN} / 1000.0 / (shares_mn / 1000.0), 1) AS eps", "shares_mn",
])
ASSET_COLS = ["cash", "receivables", "inventories", "other_ca", "ppe", "goodwill", "other_nca"]
LIAB_COLS = ["payables", "st_debt", "other_cl", "lt_debt", "other_ncl"]
_sum = lambda cols: "(" + " + ".join(f"{c}_mn" for c in cols) + ")"
BS_SELECT = ",\n       ".join(
    [_bn(f"{c}_mn", c) for c in ASSET_COLS + LIAB_COLS]
    + [_bn(_sum(["cash", "receivables", "inventories", "other_ca"]), "total_current_assets"),
       _bn(_sum(ASSET_COLS), "total_assets"), _bn("(st_debt_mn + lt_debt_mn)", "total_debt"),
       _bn(_sum(LIAB_COLS), "total_liabilities"), _bn("total_equity_mn", "total_equity"),
       _bn("nci_mn", "nci"), _bn("(total_equity_mn - nci_mn)", "equity_parent")])
CF_SELECT = ",\n       ".join([
    _bn("cfo_mn", "cfo"), _bn("capex_mn", "capex"), _bn("dividends_mn", "dividends"),
    _bn("net_borrowing_mn", "net_borrowing"), _bn("other_investing_mn", "other_investing"),
    _bn("(cfo_mn - capex_mn)", "fcf"),
    _bn("(cfo_mn - capex_mn - dividends_mn + net_borrowing_mn + other_investing_mn)", "net_change_cash"),
])

VIEW_SQL = {
    "v_income_statement": f"CREATE VIEW v_income_statement AS\nSELECT fiscal_year,\n       {IS_SELECT}\nFROM raw_income_statement;",
    "v_balance_sheet": f"CREATE VIEW v_balance_sheet AS\nSELECT fiscal_year,\n       {BS_SELECT}\nFROM raw_balance_sheet;",
    "v_cash_flow": f"CREATE VIEW v_cash_flow AS\nSELECT fiscal_year,\n       {CF_SELECT}\nFROM raw_cash_flow;",
    "v_quarterly": (
        "CREATE VIEW v_quarterly AS\nSELECT period, period_end,\n       " + IS_SELECT + ",\n       "
        + _bn("cfo_mn", "cfo") + ",\n       " + _bn("capex_mn", "capex") + ",\n       "
        + _bn("(cfo_mn - capex_mn)", "fcf") + "\nFROM raw_quarterly;"),
    "v_price": ("CREATE VIEW v_price AS\nSELECT trade_date, ROUND(open,0) AS open, ROUND(high,0) AS high,\n"
                "       ROUND(low,0) AS low, ROUND(close,0) AS close, volume\nFROM raw_price_daily\n"
                "WHERE volume > 0 AND high >= low AND close > 0;"),
}
RAW_TABLE_OF_VIEW = {"v_income_statement": "raw_income_statement", "v_balance_sheet": "raw_balance_sheet",
                     "v_cash_flow": "raw_cash_flow", "v_quarterly": "raw_quarterly", "v_price": "raw_price_daily"}
SQL_QUERIES = {
    "income": "SELECT * FROM v_income_statement ORDER BY fiscal_year",
    "balance": "SELECT * FROM v_balance_sheet ORDER BY fiscal_year",
    "cashflow": "SELECT * FROM v_cash_flow ORDER BY fiscal_year",
    "quarterly": "SELECT * FROM v_quarterly ORDER BY period_end",
    "price": "SELECT * FROM v_price ORDER BY trade_date",
    "macro": "SELECT * FROM raw_macro ORDER BY obs_date",
    "peers": "SELECT * FROM peers",
    "segments": "SELECT * FROM segment_mix ORDER BY fiscal_year, segment",
    "geo": "SELECT * FROM geo_mix ORDER BY fiscal_year, region",
}
SQL_PIPELINE_DOC = """-- PIPELINE:  raw_* tables (IDR millions, integers)  -->  v_* views  -->  pandas
-- 1. Unit conversion : IDR mn -> IDR bn  (/1000.0), ROUND(.., 1)
-- 2. NULL safety     : COALESCE(col, 0) on every numeric field
-- 3. Derivations     : gross_profit, EBIT, EBITDA, pre-tax, net income, parent NI, EPS,
--                      total assets / liabilities / debt, FCF, net change in cash
-- 4. Price cleaning  : v_price drops rows with volume <= 0, high < low or close <= 0
-- 5. Safety          : the connection is opened with PRAGMA query_only = ON (read-only)
"""


@st.cache_resource(show_spinner=False)
def init_sql_db() -> sqlite3.Connection:
    """Create the in-memory SQLite database: raw tables, cleaned views, reference tables."""
    con = sqlite3.connect(":memory:", check_same_thread=False)
    tables = _generate_annual()
    tables["raw_quarterly"] = _generate_quarterly()
    tables["raw_price_daily"] = _generate_prices()
    tables["raw_macro"] = _generate_macro()
    tables["peers"] = _generate_peers()
    tables["segment_mix"], tables["geo_mix"] = _generate_mix()
    for name, df in tables.items():
        df.to_sql(name, con, index=False, if_exists="replace")
    for sql in VIEW_SQL.values():
        con.execute(sql)
    con.commit()
    con.execute("PRAGMA query_only = ON")
    return con


@st.cache_data(show_spinner="Querying SQLite pipeline...")
def load_data() -> dict[str, pd.DataFrame]:
    """Run all cleaning queries once and return pandas frames."""
    con = init_sql_db()
    out = {k: pd.read_sql_query(q, con) for k, q in SQL_QUERIES.items()}
    out["price"]["trade_date"] = pd.to_datetime(out["price"]["trade_date"])
    out["macro"]["obs_date"] = pd.to_datetime(out["macro"]["obs_date"])
    out["quarterly"]["period_end"] = pd.to_datetime(out["quarterly"]["period_end"])
    return out


@st.cache_data(show_spinner=False)
def run_sql(query: str) -> pd.DataFrame:
    return pd.read_sql_query(query, init_sql_db())


# =============================================================================
# 3. ANALYTICS: RATIOS, LTM, DCF, MACRO, TECHNICALS
# =============================================================================
def compute_financial_ratios(income: pd.DataFrame, balance: pd.DataFrame, cashflow: pd.DataFrame,
                             wacc: float = 0.10) -> pd.DataFrame:
    """Merge the three statements and derive growth, margin, return, leverage and cash metrics."""
    df = (income.merge(balance, on="fiscal_year").merge(cashflow, on="fiscal_year")
          .sort_values("fiscal_year").reset_index(drop=True))
    df["period_label"] = "FY" + df["fiscal_year"].astype(str)
    df["rev_growth"] = df["revenue"].pct_change()
    df["ni_growth"] = df["net_income_parent"].pct_change()
    df["ebit_growth"] = df["ebit"].pct_change()
    for name, col in {"gross_margin": "gross_profit", "ebit_margin": "ebit",
                      "ebitda_margin": "ebitda", "net_margin": "net_income"}.items():
        df[name] = df[col] / df["revenue"]
    df["fcf_margin"] = df["fcf"] / df["revenue"]
    df["eff_tax"] = df["tax"] / df["pretax_income"]
    df["nopat"] = df["ebit"] * (1 - df["eff_tax"])
    df["invested_capital"] = df["total_debt"] + df["total_equity"] - df["cash"]
    df["roic"] = df["nopat"] / df["invested_capital"]
    df["roe"] = df["net_income_parent"] / df["equity_parent"]
    df["dupont_margin"] = df["net_income_parent"] / df["revenue"]
    df["asset_turnover"] = df["revenue"] / df["total_assets"]
    df["equity_multiplier"] = df["total_assets"] / df["equity_parent"]
    df["roic_wacc_spread"] = df["roic"] - wacc
    df["net_debt"] = df["total_debt"] - df["cash"]
    df["net_debt_ebitda"] = df["net_debt"] / df["ebitda"]
    df["debt_equity"] = df["total_debt"] / df["total_equity"]
    df["interest_cov"] = df["ebit"] / df["interest_expense"]
    df["dso"] = df["receivables"] / df["revenue"] * 365
    df["dio"] = df["inventories"] / df["cogs"] * 365
    df["dpo"] = df["payables"] / df["cogs"] * 365
    df["ccc"] = df["dso"] + df["dio"] - df["dpo"]
    df["ocf_to_ni"] = df["cfo"] / df["net_income"]
    df["ocf_to_ebitda"] = df["cfo"] / df["ebitda"]
    df["dps"] = df["dividends"] / (df["shares_mn"] / 1000)
    df["bvps"] = df["equity_parent"] / (df["shares_mn"] / 1000)
    return df


def build_quarterly_frame(q: pd.DataFrame) -> pd.DataFrame:
    d = q.copy()
    for name, col in {"gross_margin": "gross_profit", "ebit_margin": "ebit",
                      "ebitda_margin": "ebitda", "net_margin": "net_income"}.items():
        d[name] = d[col] / d["revenue"]
    d["rev_yoy"] = d["revenue"].pct_change(4)
    return d


def ltm_block(q: pd.DataFrame, fin: pd.DataFrame) -> dict:
    """Last-4-quarter (LTM) vs prior-4-quarter aggregates."""
    def agg(d: pd.DataFrame, bs_row: pd.Series) -> dict:
        out = {k: float(d[k].sum()) for k in
               ["revenue", "gross_profit", "ebit", "ebitda", "net_income", "net_income_parent", "fcf", "da", "cfo", "capex"]}
        out["eps"] = out["net_income_parent"] / (d["shares_mn"].iloc[-1] / 1000)
        out["roe"] = out["net_income_parent"] / bs_row["equity_parent"]
        out["roic"] = out["ebit"] * (1 - TAX_RATE) / bs_row["invested_capital"]
        return out
    return {"cur": agg(q.tail(4), fin.iloc[-1]), "prv": agg(q.head(4), fin.iloc[-2])}


def build_dcf_base(fin: pd.DataFrame) -> dict:
    l = fin.iloc[-1]
    return dict(
        base_year=int(l["fiscal_year"]), revenue=float(l["revenue"]), ebit_margin=float(l["ebit"] / l["revenue"]),
        da_pct=float(l["da"] / l["revenue"]),
        nwc_pct=float((l["receivables"] + l["inventories"] + l["other_ca"] - l["payables"] - l["other_cl"]) / l["revenue"]),
        tax=TAX_RATE, net_debt=float(l["total_debt"] - l["cash"]), nci_fv=float(l["nci"] * NCI_FV_MULT),
        shares_bn=float(l["shares_mn"] / 1000),
    )


def run_dcf_model(base: dict, a: dict, current_price: float) -> dict:
    """
    5-year unlevered DCF.  `a` keys (decimals): rev_cagr, ebit_margin, wacc, tg, capex_pct.
    EBIT margin glides linearly to target; NWC change = nwc% x change in revenue;
    terminal value by Gordon growth on year-5 UFCF; equity bridge deducts net debt and NCI (1.5x book).
    """
    n = 5
    t = np.arange(1, n + 1)
    years = [f"FY{base['base_year'] + i}E" for i in t]
    revenue = base["revenue"] * (1 + a["rev_cagr"]) ** t
    margin = base["ebit_margin"] + (a["ebit_margin"] - base["ebit_margin"]) * t / n
    ebit = revenue * margin
    nopat = ebit * (1 - base["tax"])
    da = revenue * base["da_pct"]
    capex = revenue * a["capex_pct"]
    prev_rev = np.concatenate([[base["revenue"]], revenue[:-1]])
    d_nwc = (revenue - prev_rev) * base["nwc_pct"]
    ufcf = nopat + da - capex - d_nwc
    disc = (1 + a["wacc"]) ** t
    pv = ufcf / disc
    spread = max(a["wacc"] - a["tg"], 0.005)
    tv = ufcf[-1] * (1 + a["tg"]) / spread
    pv_tv = tv / disc[-1]
    ev = float(pv.sum() + pv_tv)
    equity = ev - base["net_debt"] - base["nci_fv"]
    price = equity / base["shares_bn"]
    fc = pd.DataFrame({
        "revenue": revenue, "growth": np.concatenate([[revenue[0] / base["revenue"] - 1], revenue[1:] / revenue[:-1] - 1]),
        "ebit_margin": margin, "ebit": ebit, "nopat": nopat, "da": da, "capex": capex, "d_nwc": d_nwc,
        "ufcf": ufcf, "disc_factor": 1 / disc, "pv_ufcf": pv,
    }, index=years)
    return dict(forecast=fc, ev=ev, pv_fcf=float(pv.sum()), pv_tv=float(pv_tv), tv=float(tv),
                tv_share=float(pv_tv / ev), equity=float(equity), price=float(price),
                upside=float(price / current_price - 1), assumptions=a, net_debt=base["net_debt"], nci_fv=base["nci_fv"],
                tv_ebitda=float(tv / (ebit[-1] + da[-1])))


def sensitivity_grid(base: dict, a: dict, price: float):
    waccs = np.round(a["wacc"] + np.arange(-0.015, 0.0151, 0.005), 4)
    gs = np.round(np.clip(a["tg"] + np.arange(-0.01, 0.0101, 0.005), 0, None), 4)
    z = np.array([[run_dcf_model(base, {**a, "wacc": w, "tg": g}, price)["price"] if w > g + 0.004 else np.nan
                   for w in waccs] for g in gs])
    return waccs, gs, z


def rating_from_upside(u: float) -> str:
    return "BUY" if u >= 0.15 else ("SELL" if u <= -0.10 else "HOLD")


# ---- macro / commodity sensitivity model ----------------------------------------
COST_MIX = {"wheat": 0.32, "cpo": 0.12, "other_raw": 0.28, "overhead": 0.28}   # share of COGS
USD_LINKED_OTHER = 0.25        # share of packaging / other raw materials priced off USD
FLOATING_DEBT = 0.40           # share of debt repricing with BI rate
USD_DEBT = 0.15                # share of debt denominated in USD (unhedged)


def macro_base(fin: pd.DataFrame) -> dict:
    l = fin.iloc[-1]
    return dict(revenue=float(l["revenue"]), cogs=float(l["cogs"]), opex=float(l["opex"]),
                total_debt=float(l["total_debt"]), shares_bn=float(l["shares_mn"] / 1000),
                parent_share=float(l["net_income_parent"] / l["net_income"]), eps=float(l["eps"]),
                gross_margin=float(l["gross_profit"] / l["revenue"]), ebit=float(l["ebit"]))


def macro_impact(b: dict, fx=0.0, wheat=0.0, cpo=0.0, bi_bps=0.0, infl_pp=0.0,
                 pass_through=0.35, vol_elasticity=0.8) -> dict:
    """Shocks: fx/wheat/cpo as decimals, bi_bps in bp, infl_pp in percentage points."""
    rev, cogs = b["revenue"], b["cogs"]
    gp = rev - cogs
    infl = infl_pp / 100
    wheat_cost = cogs * COST_MIX["wheat"] * ((1 + fx) * (1 + wheat) - 1)
    cpo_cost = cogs * COST_MIX["cpo"] * ((1 + cpo) * (1 + 0.5 * fx) - 1)
    other_cost = cogs * (COST_MIX["other_raw"] * (USD_LINKED_OTHER * fx + infl) + COST_MIX["overhead"] * infl)
    d_cost = wheat_cost + cpo_cost + other_cost
    dvol = -vol_elasticity * infl_pp / 100
    d_vol = gp * dvol
    d_price = pass_through * d_cost
    d_ebit = -d_cost + d_vol + d_price
    d_interest = -b["total_debt"] * FLOATING_DEBT * bi_bps / 1e4
    d_fxdebt = -b["total_debt"] * USD_DEBT * fx
    d_pretax = d_ebit + d_interest + d_fxdebt
    conv = (1 - TAX_RATE) * b["parent_share"] / b["shares_bn"]
    d_eps = d_pretax * conv
    rev_new = rev * (1 + dvol) + d_price
    cogs_new = cogs * (1 + dvol) + d_cost
    return dict(
        d_cogs_pct=(cogs_new / cogs - 1), gm_new=(rev_new - cogs_new) / rev_new, gm_base=b["gross_margin"],
        d_ebit=d_ebit, d_ebit_pct=d_ebit / b["ebit"], d_eps=d_eps, eps_new=b["eps"] + d_eps, d_eps_pct=d_eps / b["eps"],
        components={"Wheat (USD & FX)": -wheat_cost * conv, "CPO": -cpo_cost * conv,
                    "Other inputs & overhead": -other_cost * conv, "Price pass-through": d_price * conv,
                    "Volume (purchasing power)": d_vol * conv, "Interest (floating debt)": d_interest * conv,
                    "FX on USD debt": d_fxdebt * conv},
    )


def macro_correlation(price: pd.DataFrame, macro: pd.DataFrame) -> pd.DataFrame:
    p = price.copy()
    p["m"] = p["trade_date"].dt.to_period("M")
    pm = p.groupby("m")["close"].last().pct_change()
    m = macro.copy()
    m["m"] = m["obs_date"].dt.to_period("M")
    m = m.set_index("m")
    ch = pd.DataFrame({
        "ICBP return": pm, "USD/IDR": m["usdidr"].pct_change(), "Wheat": m["wheat_usd_bu"].pct_change(),
        "CPO": m["cpo_usd_t"].pct_change(), "BI rate (chg)": m["bi_rate_pct"].diff(),
        "Inflation (chg)": m["inflation_yoy_pct"].diff(),
    }).dropna()
    return ch.corr()


def add_indicators(px: pd.DataFrame) -> pd.DataFrame:
    d = px.copy()
    c = d["close"]
    d["ma50"], d["ma200"] = c.rolling(50).mean(), c.rolling(200).mean()
    delta = c.diff()
    gain, loss = delta.clip(lower=0), -delta.clip(upper=0)
    ag = gain.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    al = loss.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    d["rsi"] = 100 - 100 / (1 + ag / al)
    d["vol30"] = c.pct_change().rolling(30).std() * np.sqrt(252) * 100
    return d


# =============================================================================
# 4. SESSION STATE / SCENARIOS
# =============================================================================
SCENARIO_DEFAULTS = {
    "Bull": dict(rev_cagr=8.0, ebit_margin=18.5, wacc=9.5, tg=3.5, capex_pct=4.5),
    "Base": dict(rev_cagr=6.5, ebit_margin=17.5, wacc=10.0, tg=3.0, capex_pct=4.8),
    "Bear": dict(rev_cagr=4.0, ebit_margin=15.5, wacc=10.75, tg=2.5, capex_pct=5.2),
}
SLIDER_SPECS = [("rev_cagr", "Revenue CAGR %", 0.0, 15.0), ("ebit_margin", "Target EBIT Margin %", 8.0, 25.0),
                ("wacc", "WACC %", 6.0, 15.0), ("tg", "Terminal Growth %", 0.0, 6.0),
                ("capex_pct", "CapEx % of Sales", 2.0, 10.0)]


def init_state() -> None:
    st.session_state.setdefault("period", "Annual (5Y)")
    st.session_state.setdefault("scenario", "Base")
    for scn, d in SCENARIO_DEFAULTS.items():
        for k, v in d.items():
            st.session_state.setdefault(f"{scn}_{k}", float(v))


def reset_scenarios() -> None:
    for scn, d in SCENARIO_DEFAULTS.items():
        for k, v in d.items():
            st.session_state[f"{scn}_{k}"] = float(v)


def get_assumptions(scn: str) -> dict:
    return {k: st.session_state[f"{scn}_{k}"] / 100 for k in SCENARIO_DEFAULTS["Base"]}


# =============================================================================
# 5. CONTEXT ASSEMBLY (comps, football field, KPIs, validation, documents)
# =============================================================================
def build_comps(ctx: dict) -> pd.DataFrame:
    fin, ltm, base, price = ctx["fin"], ctx["ltm"]["cur"], ctx["base"], ctx["last_close"]
    base_fc = ctx["dcf"]["Base"]["forecast"]
    nopat0 = base["revenue"] * base["ebit_margin"] * (1 - base["tax"])
    fwd_eps = ltm["eps"] * base_fc["nopat"].iloc[0] / nopat0
    ebitda0 = float(fin.iloc[-1]["ebitda"])
    fwd_ebitda = ltm["ebitda"] * (base_fc["ebit"].iloc[0] + base_fc["da"].iloc[0]) / ebitda0
    ctx["fwd_eps"], ctx["fwd_ebitda"] = fwd_eps, fwd_ebitda
    mcap_bn = price * base["shares_bn"]
    ev = mcap_bn + base["net_debt"] + base["nci_fv"]
    l = fin.iloc[-1]
    icbp = dict(ticker="ICBP", name=COMPANY, mcap_tn=mcap_bn / 1000, pe_ttm=price / ltm["eps"], pe_fwd=price / fwd_eps,
                ev_ebitda=ev / ltm["ebitda"], pbv=price / l["bvps"], roe=ltm["roe"] * 100,
                op_margin=ltm["ebit"] / ltm["revenue"] * 100, div_yield=l["dps"] / price * 100,
                ebitda_growth=(ltm["ebitda"] / ctx["ltm"]["prv"]["ebitda"] - 1) * 100)
    comps = pd.concat([pd.DataFrame([icbp]), ctx["data"]["peers"]], ignore_index=True)
    return comps


def football_field_data(ctx: dict) -> pd.DataFrame:
    px, comps, base = ctx["data"]["price"], ctx["comps"], ctx["base"]
    peers = comps[comps["ticker"] != "ICBP"]
    dcf_prices = [ctx["dcf"][s]["price"] for s in SCENARIOS]
    last252 = px.tail(252)
    pe_lo, pe_hi = peers["pe_fwd"].quantile([0.25, 0.75]) * ctx["fwd_eps"]
    ev_lo, ev_hi = peers["ev_ebitda"].quantile([0.25, 0.75]) * ctx["ltm"]["cur"]["ebitda"]
    to_px = lambda ev: (ev - base["net_debt"] - base["nci_fv"]) / base["shares_bn"]
    return pd.DataFrame([
        ("DCF (Bear - Bull)", min(dcf_prices), max(dcf_prices)),
        ("52-Week Trading Range", last252["low"].min(), last252["high"].max()),
        ("P/E Fwd (peer IQR)", pe_lo, pe_hi),
        ("EV/EBITDA TTM (peer IQR)", to_px(ev_lo), to_px(ev_hi)),
    ], columns=["method", "low", "high"])


def kpi_values(ctx: dict) -> list[tuple[str, str, str]]:
    fin, ltm = ctx["fin"], ctx["ltm"]
    pct = lambda a, b: f"{(a / b - 1) * 100:+.1f}%"
    pp = lambda a, b: f"{(a - b) * 100:+.1f} pp"
    if ctx["period"].startswith("Annual"):
        l, p = fin.iloc[-1], fin.iloc[-2]
        return [("Revenue", fmt_idr(l.revenue), pct(l.revenue, p.revenue)),
                ("EBIT", fmt_idr(l.ebit), pct(l.ebit, p.ebit)),
                ("Net Income", fmt_idr(l.net_income_parent), pct(l.net_income_parent, p.net_income_parent)),
                ("Free Cash Flow", fmt_idr(l.fcf), pct(l.fcf, p.fcf)),
                ("ROE", f"{l.roe:.1%}", pp(l.roe, p.roe)), ("ROIC", f"{l.roic:.1%}", pp(l.roic, p.roic))]
    c, p = ltm["cur"], ltm["prv"]
    return [("Revenue (LTM)", fmt_idr(c["revenue"]), pct(c["revenue"], p["revenue"])),
            ("EBIT (LTM)", fmt_idr(c["ebit"]), pct(c["ebit"], p["ebit"])),
            ("Net Income (LTM)", fmt_idr(c["net_income_parent"]), pct(c["net_income_parent"], p["net_income_parent"])),
            ("FCF (LTM)", fmt_idr(c["fcf"]), pct(c["fcf"], p["fcf"])),
            ("ROE (LTM)", f"{c['roe']:.1%}", pp(c["roe"], p["roe"])),
            ("ROIC (LTM)", f"{c['roic']:.1%}", pp(c["roic"], p["roic"]))]


def run_validation(ctx: dict) -> pd.DataFrame:
    fin, data, checks = ctx["fin"], ctx["data"], []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"Check": name, "Status": "✅ PASS" if ok else "❌ FAIL", "Detail": detail})

    bs_diff = (fin["total_assets"] - fin["total_liabilities"] - fin["total_equity"]).abs().max()
    add("Balance sheet: Assets = Liabilities + Equity", bs_diff < 0.5, f"max |difference| = {bs_diff:.3f} bn (tolerance 0.5)")
    cash_diff = (fin["cash"].diff() - fin["net_change_cash"]).abs().iloc[1:].max()
    add("Cash roll-forward ties to cash-flow statement", cash_diff < 0.6, f"max |difference| = {cash_diff:.3f} bn")
    gp_d = (fin["revenue"] - fin["cogs"] - fin["gross_profit"]).abs().max()
    eb_d = (fin["ebit"] + fin["da"] - fin["ebitda"]).abs().max()
    ni_d = (fin["pretax_income"] - fin["tax"] - fin["net_income"]).abs().max()
    add("Income statement identities (GP, EBITDA, NI)", max(gp_d, eb_d, ni_d) < 0.3, f"max rounding gap = {max(gp_d, eb_d, ni_d):.3f} bn")
    fcf_d = (fin["cfo"] - fin["capex"] - fin["fcf"]).abs().max()
    add("FCF = CFO - CapEx", fcf_d < 0.2, f"max |difference| = {fcf_d:.3f} bn")
    nulls = {k: int(v.isna().sum().sum()) for k, v in data.items()}
    add("Missing-value assertion (all SQL outputs)", sum(nulls.values()) == 0, f"NaN counts: {nulls}")
    for scn in SCENARIOS:
        r = ctx["dcf"][scn]
        a, fc = r["assumptions"], r["forecast"]
        pv = sum(u / (1 + a["wacc"]) ** i for i, u in enumerate(fc["ufcf"], start=1))
        tv = fc["ufcf"].iloc[-1] * (1 + a["tg"]) / max(a["wacc"] - a["tg"], 0.005)
        ev_chk = pv + tv / (1 + a["wacc"]) ** 5
        px_chk = (ev_chk - r["net_debt"] - r["nci_fv"]) / ctx["base"]["shares_bn"]
        add(f"DCF reconciliation - {scn}", abs(ev_chk - r["ev"]) < 1e-6 * r["ev"] and abs(px_chk - r["price"]) < 1e-6 * r["price"],
            f"EV {r['ev']:,.0f} vs independent {ev_chk:,.0f}; price {r['price']:,.0f} vs {px_chk:,.0f}")
    act = ctx["dcf"][ctx["scenario"]]
    waccs, gs, z = sensitivity_grid(ctx["base"], act["assumptions"], ctx["last_close"])
    centre = z[int(np.argmin(abs(gs - act["assumptions"]["tg"]))), int(np.argmin(abs(waccs - act["assumptions"]["wacc"])))]
    add("Sensitivity heatmap centre = active DCF price", abs(centre - act["price"]) < 1e-6 * act["price"], f"{centre:,.0f} vs {act['price']:,.0f}")
    seg_ok = (data["segments"].groupby("fiscal_year")["share"].sum() - 1).abs().max() < 1e-6
    geo_ok = (data["geo"].groupby("fiscal_year")["share"].sum() - 1).abs().max() < 1e-6
    add("Segment & geographic mix sum to 100%", bool(seg_ok and geo_ok), "per fiscal year")
    px = data["price"]
    ohlc_ok = bool((px["high"] >= px[["open", "close"]].max(axis=1)).all() and (px["low"] <= px[["open", "close"]].min(axis=1)).all() and (px["volume"] > 0).all())
    add("Price OHLCV integrity (H>=O,C; L<=O,C; volume>0)", ohlc_ok, f"{len(px):,} daily bars")
    q25 = data["quarterly"][data["quarterly"]["period"].str.startswith("2025")]["revenue"].sum()
    add("FY2025 quarterly revenue reconciles to annual", abs(q25 - fin.iloc[-1]["revenue"]) / fin.iloc[-1]["revenue"] < 0.01,
        f"sum of quarters {q25:,.0f} vs annual {fin.iloc[-1]['revenue']:,.0f}")
    add("Peer table completeness", len(data["peers"]) == 5, f"{len(data['peers'])} peers loaded")
    return pd.DataFrame(checks)


def build_research_note(ctx: dict) -> str:
    l, res, sc = ctx["fin"].iloc[-1], ctx["dcf"][ctx["scenario"]], ctx["scenario"]
    a = res["assumptions"]
    comps, c = ctx["comps"], ctx["comps"].iloc[0]
    peers = comps[comps["ticker"] != "ICBP"]
    scen_rows = "\n".join(
        f"| {s} | {ctx['dcf'][s]['assumptions']['rev_cagr']:.1%} | {ctx['dcf'][s]['assumptions']['ebit_margin']:.1%} | "
        f"{ctx['dcf'][s]['assumptions']['wacc']:.2%} | {ctx['dcf'][s]['assumptions']['tg']:.1%} | "
        f"{ctx['dcf'][s]['price']:,.0f} | {ctx['dcf'][s]['upside']:+.1%} |" for s in SCENARIOS)
    return f"""# {COMPANY} ({TICKER}) - Equity Research Note
**Date:** {AS_OF:%d %B %Y}  |  **Rating:** {ctx['rating']}  |  **Target Price:** IDR {ctx['tp']:,.0f}  |  **Last Close:** IDR {ctx['last_close']:,.0f}  |  **Upside:** {ctx['tp'] / ctx['last_close'] - 1:+.1%}

> Illustrative research note built on SYNTHETIC data. Not investment advice.

## Recommendation ({sc} case)
We rate ICBP **{ctx['rating']}** with a DCF-derived target price of IDR {ctx['tp']:,.0f}. The shares trade at {c['pe_fwd']:.1f}x forward P/E and {c['ev_ebitda']:.1f}x TTM EV/EBITDA versus peer medians of {peers['pe_fwd'].median():.1f}x and {peers['ev_ebitda'].median():.1f}x.

## Investment Thesis
1. **Defensible moat:** category-leading instant-noodle brands, nationwide distribution and procurement scale.
2. **Pinehill international runway:** Middle East & Africa now contributes {ctx['mea_share']:.1%} of sales (from {ctx['mea_share_start']:.1%} in FY{FISCAL_YEARS[0]}).
3. **Margin and returns:** EBIT margin {l['ebit_margin']:.1%}; ROIC {l['roic']:.1%} versus a {a['wacc']:.2%} WACC ({scenario_spread(l['roic'], a['wacc'])}).
4. **Fortress balance sheet:** net debt / EBITDA {l['net_debt_ebitda']:.2f}x; interest cover {l['interest_cov']:.1f}x.

## Financial Snapshot (FY{int(l['fiscal_year'])}, IDR bn)
| Revenue | EBIT | Net income (parent) | FCF | ROE | EPS (IDR) |
|---|---|---|---|---|---|
| {l['revenue']:,.0f} | {l['ebit']:,.0f} | {l['net_income_parent']:,.0f} | {l['fcf']:,.0f} | {l['roe']:.1%} | {l['eps']:,.0f} |

## Valuation Scenarios
| Scenario | Rev CAGR | Target EBIT margin | WACC | Terminal g | Value / share (IDR) | Upside |
|---|---|---|---|---|---|---|
{scen_rows}

Active-case enterprise value IDR {res['ev']:,.0f}bn; terminal value is {res['tv_share']:.0%} of EV (implied TV/EBITDA {res['tv_ebitda']:.1f}x).

## Key Risks
- **FX / USD exposure:** unhedged USD debt and USD-linked wheat and packaging costs.
- **Commodity inflation:** wheat and CPO are the largest COGS lines; pass-through lags by 2-3 quarters.
- **Consumer purchasing power:** volume elasticity to inflation in the low-income consumer base.
- **Competition and trade-down:** price wars in instant noodles; private-label risk.
"""


def scenario_spread(roic: float, wacc: float) -> str:
    return f"{(roic - wacc) * 100:+.1f} pp spread"


def build_readme() -> str:
    f = "`" * 3
    return f"""# ICBP Equity Research & Valuation Terminal

An institutional-style Streamlit dashboard for **PT Indofood CBP Sukses Makmur Tbk (IDX: ICBP)** covering
fundamentals, 3-scenario DCF, peer comps, technicals and macro sensitivities.

> All financial, price, macro and peer data is **synthetic** (generated in code, calibrated to ICBP's rough scale).
> This project is for portfolio/educational use and is not investment advice.

## Features
- **SQLite pipeline:** raw tables (IDR mn) -> cleaned SQL views (IDR bn, derived subtotals) -> pandas
- **6 tabs:** Executive Summary, 5Y Fundamentals, DCF Engine, Peer Comps, Technicals & Macro, Data Provenance
- **DCF:** Bull/Base/Bear sliders, football field, WACC x terminal-growth heatmap
- **Macro model:** USD/IDR, wheat, CPO, BI rate and inflation -> COGS, gross margin and EPS (waterfall + tornado)
- **Audit:** automated balance-sheet, cash roll-forward, DCF reconciliation and missing-value checks

## Quick start
{f}bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
{f}

## Project structure
{f}text
app.py             # entire application (init_sql_db, compute_financial_ratios, run_dcf_model, render_tabs)
requirements.txt
.streamlit/config.toml   # optional dark theme
{f}

## Methodology notes
- EBIT margin glides linearly to the target; NWC change = NWC % of sales x change in revenue.
- Terminal value uses Gordon growth; equity bridge deducts net debt and NCI (1.5x book).
- Rating: BUY if upside >= 15%, SELL if <= -10%, otherwise HOLD (target price rounded to IDR 50).

## Disclaimer
Educational demo using fabricated data. Replace `init_sql_db()` generators with licensed data feeds before any real use.
"""


# =============================================================================
# 6. UI: SIDEBAR
# =============================================================================
def render_sidebar(ctx: dict) -> None:
    with st.sidebar:
        st.markdown(f"### {TICKER}")
        st.caption(COMPANY)
        px = ctx["data"]["price"]
        chg = ctx["last_close"] / px["close"].iloc[-2] - 1
        st.metric("Share Price (mock, IDR)", f"{ctx['last_close']:,.0f}", f"{chg:+.2%} d/d")
        c1, c2 = st.columns(2)
        c1.metric("Target Price", f"{ctx['tp']:,.0f}")
        c2.metric("Upside", f"{ctx['tp'] / ctx['last_close'] - 1:+.1%}")
        st.markdown(f"<span class='badge badge-{ctx['rating']}'>{ctx['rating']}</span> "
                    f"<span class='small-note'>&nbsp;{ctx['scenario']} case DCF</span>", unsafe_allow_html=True)
        st.divider()
        st.radio("Reporting Period", ["Annual (5Y)", "Quarterly (LTM)"], key="period")
        st.radio("Active Valuation Scenario", SCENARIOS, key="scenario", horizontal=True)
        if ctx["period"].startswith("Annual"):
            export = ctx["fin"].drop(columns=["period_label"], errors="ignore")
            fname = "icbp_annual_financials_clean.csv"
        else:
            export = ctx["q"]
            fname = "icbp_quarterly_financials_clean.csv"
        st.download_button("⬇ Export cleaned dataset (CSV)", data=export.to_csv(index=False).encode("utf-8"),
                           file_name=fname, mime="text/csv")
        st.divider()
        st.caption(f"Data as of {AS_OF:%d %b %Y}. Synthetic data; not investment advice.")


# =============================================================================
# 7. UI: TAB 1 - EXECUTIVE SUMMARY
# =============================================================================
def risk_card(title: str, severity: str, body: str, impact: str, mitigant: str) -> str:
    color = {"High": RED, "Medium": AMBER, "Low": TEAL}[severity]
    return (f"<div class='risk-card' style='border-left:4px solid {color}'>"
            f"<div class='risk-head'><span>{title}</span><span class='tag' style='background:{color}22;color:{color}'>{severity.upper()}</span></div>"
            f"<p>{body}</p><p class='impact'>{impact}</p><p><b>Mitigant:</b> {mitigant}</p></div>")


def render_summary_tab(ctx: dict) -> None:
    l = ctx["fin"].iloc[-1]
    res, comps = ctx["dcf"][ctx["scenario"]], ctx["comps"]
    peers, c = comps[comps["ticker"] != "ICBP"], comps.iloc[0]
    left, right = st.columns([2.3, 1])
    with left:
        st.subheader("Investment Thesis & Equity Research Report")
        st.markdown(f"""
**Recommendation: {ctx['rating']}  |  Target Price IDR {ctx['tp']:,.0f} ({ctx['tp'] / ctx['last_close'] - 1:+.1%})  |  {ctx['scenario']}-case DCF**

**1. Moat - brands, scale and distribution.** ICBP is Indonesia's largest branded instant-noodle franchise (Indomie, Pop Mie)
with adjacent dairy, snacks, seasonings, nutrition and beverage lines. Affordable price points, a nationwide distribution
network and group-wide procurement scale (wheat, CPO, packaging) give it a cost and reach advantage that sub-scale rivals struggle to match.

**2. Pinehill international expansion.** The Middle East & Africa business (Pinehill) has grown from
**{ctx['mea_share_start']:.1%}** to **{ctx['mea_share']:.1%}** of sales since FY{FISCAL_YEARS[0]}, diversifying away from rupiah-only demand and
adding a structurally higher-growth, under-penetrated noodle market.

**3. Margins and returns.** EBIT margin has expanded to **{l['ebit_margin']:.1%}** and ROIC of **{l['roic']:.1%}** now sits
{scenario_spread(l['roic'], res['assumptions']['wacc'])} versus the active-scenario WACC of {res['assumptions']['wacc']:.2%}.

**4. Balance sheet.** Net debt/EBITDA of **{l['net_debt_ebitda']:.2f}x** and interest cover of **{l['interest_cov']:.1f}x** leave ample capacity for
dividends (payout ~{PAYOUT:.0%}) and bolt-on M&A.

**5. Valuation.** Shares trade at **{c['pe_fwd']:.1f}x** forward P/E and **{c['ev_ebitda']:.1f}x** EV/EBITDA versus peer medians
of {peers['pe_fwd'].median():.1f}x and {peers['ev_ebitda'].median():.1f}x. Our DCF yields IDR {res['price']:,.0f} per share;
{res['tv_share']:.0%} of EV comes from terminal value.

**What would change our view:** sustained USD/IDR weakness without pricing action, wheat/CPO spikes above our bull-case cost
assumptions, or a trade-down shift in noodles volume.
""")
        st.caption("All figures are produced from synthetic data for demonstration purposes.")
    with right:
        st.subheader("Snapshot")
        st.markdown(f"<span class='badge badge-{ctx['rating']}'>{ctx['rating']}</span>", unsafe_allow_html=True)
        st.metric("DCF Value / Share", f"IDR {res['price']:,.0f}", f"{res['upside']:+.1%} vs last")
        st.metric("Enterprise Value", fmt_idr(res["ev"]))
        st.metric("P/E TTM  |  Fwd", f"{c['pe_ttm']:.1f}x  |  {c['pe_fwd']:.1f}x")
        st.metric("Dividend Yield", f"{c['div_yield']:.1f}%")

    st.divider()
    st.subheader("Revenue Segments Breakdown")
    seg = ctx["data"]["segments"].merge(ctx["fin"][["fiscal_year", "revenue"]], on="fiscal_year")
    seg["rev_bn"] = seg["share"] * seg["revenue"]
    geo = ctx["data"]["geo"].merge(ctx["fin"][["fiscal_year", "revenue"]], on="fiscal_year")
    geo["rev_bn"] = geo["share"] * geo["revenue"]
    yr = st.select_slider("Fiscal year (donut charts)", options=FISCAL_YEARS, value=FISCAL_YEARS[-1], key="seg_year")
    r1a, r1b = st.columns(2)
    with r1a:
        s = seg[seg["fiscal_year"] == yr].set_index("segment").loc[SEGMENTS].reset_index()
        fig = go.Figure(go.Pie(labels=s["segment"], values=s["rev_bn"], hole=0.55, marker=dict(colors=PALETTE),
                               textinfo="label+percent", sort=False))
        show_chart(style_fig(fig, 360, f"Revenue by Division - FY{yr}", unified=False), key="seg_donut")
    with r1b:
        fig = go.Figure()
        for i, name in enumerate(SEGMENTS):
            d = seg[seg["segment"] == name]
            fig.add_bar(x=[f"FY{y}" for y in d["fiscal_year"]], y=d["rev_bn"], name=name, marker_color=PALETTE[i])
        fig.update_layout(barmode="stack")
        fig.update_yaxes(title="IDR bn")
        show_chart(style_fig(fig, 360, "Divisional Revenue, FY21-FY25 (IDR bn)"), key="seg_stack")
    r2a, r2b = st.columns(2)
    with r2a:
        g = geo[geo["fiscal_year"] == yr]
        fig = go.Figure(go.Pie(labels=g["region"], values=g["rev_bn"], hole=0.55, marker=dict(colors=[BLUE, AMBER]),
                               textinfo="label+percent", sort=False))
        show_chart(style_fig(fig, 320, f"Geographic Split - FY{yr}", unified=False), key="geo_donut")
    with r2b:
        fig = go.Figure()
        for i, name in enumerate(REGIONS):
            d = geo[geo["region"] == name]
            fig.add_bar(x=[f"FY{y}" for y in d["fiscal_year"]], y=d["rev_bn"], name=name, marker_color=[BLUE, AMBER][i])
        fig.update_layout(barmode="stack")
        fig.update_yaxes(title="IDR bn")
        show_chart(style_fig(fig, 320, "Indonesia vs Middle East & Africa (IDR bn)"), key="geo_stack")

    st.divider()
    st.subheader("Key Risks Matrix")
    mb = macro_base(ctx["fin"])
    fx = macro_impact(mb, fx=0.10)["d_eps_pct"]
    wh = macro_impact(mb, wheat=0.20)["d_eps_pct"]
    cp = macro_impact(mb, cpo=0.20)["d_eps_pct"]
    inf = macro_impact(mb, infl_pp=1.0)["d_eps_pct"]
    cols = st.columns(3)
    cards = [
        risk_card("FX / USD debt exposure", "High", "Unhedged USD borrowings plus USD-linked wheat and packaging make earnings sensitive to rupiah weakness.",
                  f"10% IDR depreciation: EPS {fx:+.1%} (after 35% pass-through)", "Natural USD hedge from Pinehill revenue; forward cover; pricing actions."),
        risk_card("Wheat & CPO inflation", "High", "Wheat (~32% of COGS) and palm oil (~12%) are the largest cost lines; price increases lag input costs by 2-3 quarters.",
                  f"Wheat +20%: EPS {wh:+.1%}; CPO +20%: EPS {cp:+.1%}", "Forward purchasing, multi-origin sourcing, selective price increases."),
        risk_card("Consumer purchasing power", "Medium", "Mass-market noodles are defensive but volumes soften when inflation outpaces wages; trade-down hits premium lines.",
                  f"Inflation +1pp: EPS {inf:+.1%} (volume and cost effects)", "Value packs, price-point architecture, export diversification."),
    ]
    for col, html in zip(cols, cards):
        col.markdown(html, unsafe_allow_html=True)
    cols2 = st.columns(3)
    cols2[0].markdown(risk_card("Competition", "Medium", "Aggressive local noodle brands and regional price wars can pressure share and promotional spend.",
                                "Each 100 bp of gross-margin erosion is roughly 5-6% of EBIT", "Brand strength, distribution depth, innovation pipeline."), unsafe_allow_html=True)
    cols2[1].markdown(risk_card("Regulation & tariffs", "Low", "Wheat import policy, halal/labelling rules and sugar/sodium regulation could raise costs or compliance burden.",
                                "Hard to quantify; monitor policy calendar", "Government engagement, reformulation capability."), unsafe_allow_html=True)
    with cols2[2]:
        rk = pd.DataFrame({"risk": ["FX", "Wheat/CPO", "Purchasing power", "Competition", "Regulation"],
                           "likelihood": [4, 4, 3, 3, 2], "impact": [4, 4, 3, 3, 2]})
        fig = go.Figure(go.Scatter(x=rk["likelihood"], y=rk["impact"], mode="markers+text", text=rk["risk"],
                                   textposition="top center", marker=dict(size=18, color=[RED, RED, AMBER, AMBER, TEAL])))
        fig.update_xaxes(range=[0.5, 5.5], title="Likelihood")
        fig.update_yaxes(range=[0.5, 5.5], title="Impact")
        show_chart(style_fig(fig, 250, "Likelihood / Impact", unified=False), key="risk_matrix")


# =============================================================================
# 8. UI: TAB 2 - FUNDAMENTALS
# =============================================================================
IS_LINES = [("Revenue", "revenue"), ("COGS", "cogs"), ("Gross Profit", "gross_profit"), ("Operating Expenses", "opex"),
            ("EBIT", "ebit"), ("D&A", "da"), ("EBITDA", "ebitda"), ("Interest Expense", "interest_expense"),
            ("Other Income", "other_income"), ("Pre-tax Income", "pretax_income"), ("Tax", "tax"),
            ("Net Income", "net_income"), ("Minority Interest", "minority_interest"),
            ("Net Income (Parent)", "net_income_parent"), ("EPS (IDR)", "eps")]
BS_LINES = [("Cash", "cash"), ("Receivables", "receivables"), ("Inventories", "inventories"),
            ("Other Current Assets", "other_ca"), ("PP&E", "ppe"), ("Goodwill & Intangibles", "goodwill"),
            ("Other Non-current Assets", "other_nca"), ("Total Assets", "total_assets"), ("Payables", "payables"),
            ("Short-term Debt", "st_debt"), ("Other Current Liabilities", "other_cl"), ("Long-term Debt", "lt_debt"),
            ("Other Non-current Liabilities", "other_ncl"), ("Total Liabilities", "total_liabilities"),
            ("Total Equity", "total_equity"), ("of which NCI", "nci")]
CF_LINES = [("Operating Cash Flow", "cfo"), ("CapEx", "capex"), ("Free Cash Flow", "fcf"), ("Dividends Paid", "dividends"),
            ("Net Borrowing", "net_borrowing"), ("Other Investing", "other_investing"), ("Net Change in Cash", "net_change_cash")]


def statement_table(df: pd.DataFrame, lines: list, label_col: str) -> pd.DataFrame:
    t = df.set_index(label_col)[[c for _, c in lines]].T.astype(float)
    t.index = [lab for lab, _ in lines]
    t.columns = [str(c) for c in t.columns]
    t["Trend"] = t.apply(lambda r: r.tolist(), axis=1)
    return t


def render_fundamentals_tab(ctx: dict) -> None:
    fin, q, annual = ctx["fin"], ctx["q"], ctx["period"].startswith("Annual")
    st.caption(f"View: **{ctx['period']}**. Return, leverage and working-capital ratios are balance-sheet based and always shown annually.")
    cols = st.columns(6)
    for col, (lab, val, delta) in zip(cols, kpi_values(ctx)):
        col.metric(lab, val, delta)

    d = fin if annual else q
    xs = list(fin["period_label"]) if annual else list(q["period"])

    st.subheader("Profitability & Growth")
    a, b = st.columns(2)
    with a:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_bar(x=xs, y=d["revenue"], name="Revenue (IDR bn)", marker_color=BLUE, secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=d["net_income_parent"], name="Net income, parent (IDR bn)", mode="lines+markers",
                                 line=dict(color=TEAL, width=3)), secondary_y=True)
        if annual:
            title = (f"Revenue CAGR {cagr(fin['revenue'].iloc[0], fin['revenue'].iloc[-1], len(fin) - 1):.1%} | "
                     f"Earnings CAGR {cagr(fin['net_income_parent'].iloc[0], fin['net_income_parent'].iloc[-1], len(fin) - 1):.1%} (FY21-FY25)")
        else:
            title = f"LTM revenue growth {ctx['ltm']['cur']['revenue'] / ctx['ltm']['prv']['revenue'] - 1:+.1%} vs prior LTM"
        show_chart(style_fig(fig, 380, title), key="rev_ni")
    with b:
        fig = go.Figure()
        for (name, col), color in zip({"Gross": "gross_margin", "EBIT": "ebit_margin", "EBITDA": "ebitda_margin", "Net": "net_margin"}.items(),
                                      [TEAL, BLUE, AMBER, RED]):
            fig.add_trace(go.Scatter(x=xs, y=d[col] * 100, name=f"{name} margin", mode="lines+markers", line=dict(color=color, width=3)))
        fig.update_yaxes(title="%", ticksuffix="%")
        show_chart(style_fig(fig, 380, "Margin Evolution"), key="margins")

    st.subheader("Returns & Leverage")
    wacc = ctx["dcf"][ctx["scenario"]]["assumptions"]["wacc"]
    labels = list(fin["period_label"])
    a, b = st.columns(2)
    with a:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_bar(x=labels, y=fin["roic_wacc_spread"] * 100, name="ROIC - WACC spread (pp)", marker_color="rgba(0,245,212,0.25)", secondary_y=True)
        fig.add_trace(go.Scatter(x=labels, y=fin["roic"] * 100, name="ROIC", mode="lines+markers", line=dict(color=TEAL, width=3)), secondary_y=False)
        fig.add_trace(go.Scatter(x=labels, y=fin["roe"] * 100, name="ROE", mode="lines+markers", line=dict(color=BLUE, width=3)), secondary_y=False)
        fig.add_trace(go.Scatter(x=labels, y=[wacc * 100] * len(labels), name=f"WACC ({ctx['scenario']})", mode="lines",
                                 line=dict(color=AMBER, dash="dash", width=2)), secondary_y=False)
        fig.update_yaxes(title_text="%", secondary_y=False)
        fig.update_yaxes(title_text="Spread (pp)", secondary_y=True, showgrid=False)
        show_chart(style_fig(fig, 360, "ROIC & ROE vs WACC"), key="roic_wacc")
    with b:
        st.markdown("**DuPont decomposition of ROE**")
        dp = pd.DataFrame({"Net margin (parent)": fin["dupont_margin"] * 100, "x Asset turnover": fin["asset_turnover"],
                           "x Equity multiplier": fin["equity_multiplier"], "= ROE (%)": fin["roe"] * 100}).T
        dp.columns = labels
        sty = dp.style.format("{:.2f}").format("{:.1f}%", subset=pd.IndexSlice[["Net margin (parent)", "= ROE (%)"], :])
        show_df(sty)
        st.caption("ROE = (Parent NI / Revenue) x (Revenue / Assets) x (Assets / Parent equity), on year-end balances.")
    a, b = st.columns(2)
    with a:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_bar(x=labels, y=fin["net_debt_ebitda"], name="Net debt / EBITDA (x)", marker_color=TEAL, secondary_y=False)
        fig.add_trace(go.Scatter(x=labels, y=fin["debt_equity"], name="Debt / Equity (x)", mode="lines+markers", line=dict(color=AMBER, width=3)), secondary_y=True)
        show_chart(style_fig(fig, 340, "Leverage"), key="leverage")
    with b:
        fig = go.Figure(go.Bar(x=labels, y=fin["interest_cov"], marker_color=BLUE, text=[f"{v:.1f}x" for v in fin["interest_cov"]], textposition="outside"))
        fig.update_yaxes(title="EBIT / interest (x)")
        show_chart(style_fig(fig, 340, "Interest Coverage"), key="int_cov")
    a, b = st.columns(2)
    with a:
        fig = go.Figure()
        fig.add_bar(x=labels, y=fin["ccc"], name="Cash conversion cycle", marker_color="rgba(59,130,246,0.35)")
        for name, col, color in [("DSO", "dso", TEAL), ("DIO", "dio", AMBER), ("DPO", "dpo", RED)]:
            fig.add_trace(go.Scatter(x=labels, y=fin[col], name=name, mode="lines+markers", line=dict(color=color, width=2)))
        fig.update_yaxes(title="days")
        show_chart(style_fig(fig, 340, "Working Capital: Cash Conversion Cycle"), key="ccc")
    with b:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labels, y=fin["ocf_to_ni"] * 100, name="OCF / Net income", mode="lines+markers", line=dict(color=TEAL, width=3)))
        fig.add_trace(go.Scatter(x=labels, y=fin["ocf_to_ebitda"] * 100, name="OCF / EBITDA", mode="lines+markers", line=dict(color=BLUE, width=3)))
        fig.add_trace(go.Scatter(x=labels, y=fin["fcf_margin"] * 100, name="FCF margin", mode="lines+markers", line=dict(color=AMBER, width=3)))
        fig.update_yaxes(title="%", ticksuffix="%")
        show_chart(style_fig(fig, 340, "Cash-Flow Quality"), key="ocf")

    st.subheader("Interactive Financial Statements")
    if annual:
        choice = st.radio("Statement", ["Income Statement", "Balance Sheet", "Cash Flow"], horizontal=True, key="stmt_a")
        view = {"Income Statement": ("v_income_statement", IS_LINES), "Balance Sheet": ("v_balance_sheet", BS_LINES),
                "Cash Flow": ("v_cash_flow", CF_LINES)}[choice]
        tbl = statement_table(fin.assign(period=fin["period_label"]), view[1], "period")
    else:
        choice = st.radio("Statement (quarterly)", ["Income Statement", "Cash Flow"], horizontal=True, key="stmt_q")
        view = ("v_quarterly", IS_LINES if choice == "Income Statement" else
                [("Operating Cash Flow", "cfo"), ("CapEx", "capex"), ("Free Cash Flow", "fcf")])
        tbl = statement_table(q, view[1], "period")
    cfg = {c: st.column_config.NumberColumn(c, format="%.1f") for c in tbl.columns if c != "Trend"}
    cfg["Trend"] = st.column_config.LineChartColumn("Trend", width="small")
    show_df(tbl, column_config=cfg)
    st.caption("IDR billions (EPS in IDR). Sparkline shows the trajectory across the displayed periods.")

    with st.expander("🔎 SQL data provenance inspector", expanded=False):
        st.code(SQL_PIPELINE_DOC, language="sql")
        st.markdown(f"**Cleaning view definition: `{view[0]}`**")
        st.code(VIEW_SQL[view[0]], language="sql")
        raw = RAW_TABLE_OF_VIEW[view[0]]
        st.markdown(f"**Raw table preview: `{raw}` (IDR millions, uncleaned)**")
        show_df(run_sql(f"SELECT * FROM {raw} LIMIT 5"))
        st.markdown("**Run your own read-only query**")
        user_sql = st.text_area("SQL (SELECT only)", value=f"SELECT fiscal_year, revenue, ebit, net_income_parent FROM v_income_statement", key="user_sql")
        stripped = user_sql.strip().rstrip(";")
        if stripped.lower().startswith("select") and ";" not in stripped:
            try:
                show_df(run_sql(stripped))
            except Exception as exc:
                st.error(f"Query error: {exc}")
        else:
            st.warning("Only a single SELECT statement is allowed.")


# =============================================================================
# 9. UI: TAB 3 - DCF
# =============================================================================
def render_dcf_tab(ctx: dict) -> None:
    base, scn, price = ctx["base"], ctx["scenario"], ctx["last_close"]
    st.subheader("Scenario Assumptions")
    head_l, head_r = st.columns([5, 1])
    head_l.caption(f"Base year FY{base['base_year']}A: revenue {fmt_idr(base['revenue'])}, EBIT margin {base['ebit_margin']:.1%}, "
                   f"D&A {base['da_pct']:.1%} of sales, NWC {base['nwc_pct']:.1%} of sales, net debt {fmt_idr(base['net_debt'])}. "
                   f"Active scenario (sidebar): **{scn}**.")
    head_r.button("Reset scenarios", on_click=reset_scenarios)
    cols = st.columns(3)
    for col, s in zip(cols, SCENARIOS):
        with col:
            st.markdown(f"**{s} Case**" + ("  ✅ active" if s == scn else ""))
            for key, label, lo, hi in SLIDER_SPECS:
                st.slider(label, lo, hi, step=0.25, key=f"{s}_{key}")

    res = ctx["dcf"][scn]
    fc = res["forecast"]
    st.subheader(f"5-Year Forecast - {scn} Case")
    tbl = pd.DataFrame({
        "Revenue": fc["revenue"], "Revenue growth %": fc["growth"] * 100, "Operating (EBIT) margin %": fc["ebit_margin"] * 100,
        "EBIT": fc["ebit"], "NOPAT": fc["nopat"], "D&A": fc["da"], "CapEx": fc["capex"],
        "Change in NWC": fc["d_nwc"], "Unlevered FCF": fc["ufcf"], "PV of UFCF": fc["pv_ufcf"],
    }).T
    sty = tbl.style.format("{:,.0f}").format("{:.1f}", subset=pd.IndexSlice[["Revenue growth %", "Operating (EBIT) margin %"], :])
    show_df(sty)
    st.caption("IDR billions unless stated. Year-end discounting; EBIT margin glides linearly to target.")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(x=fc.index, y=fc["revenue"], name="Revenue", marker_color=BLUE, secondary_y=False)
    fig.add_bar(x=fc.index, y=fc["ufcf"], name="UFCF", marker_color=TEAL, secondary_y=False)
    fig.add_trace(go.Scatter(x=fc.index, y=fc["ebit_margin"] * 100, name="EBIT margin %", mode="lines+markers",
                             line=dict(color=AMBER, width=3)), secondary_y=True)
    fig.update_layout(barmode="group")
    fig.update_yaxes(title_text="IDR bn", secondary_y=False)
    fig.update_yaxes(title_text="EBIT margin %", secondary_y=True, showgrid=False)
    show_chart(style_fig(fig, 360, "Forecast Revenue, UFCF and Operating Margin"), key="fc_chart")

    st.subheader("DCF Valuation Output")
    m = st.columns(5)
    m[0].metric("Enterprise Value", fmt_idr(res["ev"]))
    m[1].metric("Implied Equity Value", fmt_idr(res["equity"]))
    m[2].metric("Implied Share Price", f"IDR {res['price']:,.0f}")
    m[3].metric("Current Price", f"IDR {price:,.0f}")
    m[4].metric("Upside / Downside", f"{res['upside']:+.1%}")
    a, b = st.columns([1, 2])
    with a:
        bridge = pd.DataFrame({"IDR bn": [res["pv_fcf"], res["pv_tv"], res["ev"], -res["net_debt"], -res["nci_fv"], res["equity"]]},
                              index=["PV of UFCF (5Y)", "PV of terminal value", "Enterprise value", "Less: net debt (negative = net cash)",
                                     "Less: NCI (1.5x book)", "Equity value"])
        show_df(bridge.style.format("{:,.0f}"))
        st.caption(f"Terminal value = {res['tv_share']:.0%} of EV; implied TV/EBITDA {res['tv_ebitda']:.1f}x.")
        for s in SCENARIOS:
            r = ctx["dcf"][s]
            st.metric(f"{s} value / share", f"IDR {r['price']:,.0f}", f"{r['upside']:+.1%}")
    with b:
        ff = football_field_data(ctx)
        fig = go.Figure(go.Bar(
            y=ff["method"], x=ff["high"] - ff["low"], base=ff["low"], orientation="h",
            marker=dict(color=[TEAL, "#94A3B8", BLUE, "#8B5CF6"]),
            text=[f"{lo:,.0f} - {hi:,.0f}" for lo, hi in zip(ff["low"], ff["high"])], textposition="inside", insidetextanchor="middle"))
        fig.add_vline(x=price, line_dash="dash", line_color=AMBER, annotation_text="Current", annotation_position="top")
        fig.add_vline(x=res["price"], line_dash="dot", line_color=RED, annotation_text=f"DCF ({scn})", annotation_position="bottom")
        fig.update_xaxes(title="IDR per share")
        fig.update_yaxes(autorange="reversed")
        show_chart(style_fig(fig, 360, "Football Field Valuation", unified=False), key="football")

    st.subheader("Sensitivity: Implied Share Price (IDR)")
    waccs, gs, z = sensitivity_grid(base, res["assumptions"], price)
    fig = go.Figure(go.Heatmap(
        z=z, x=[f"{w:.2%}" for w in waccs], y=[f"{g:.2%}" for g in gs], zmid=price,
        colorscale=[[0, RED], [0.5, "#1F2937"], [1, TEAL]], text=np.where(np.isnan(z), "n/a", np.round(z, 0).astype(int).astype(str)),
        texttemplate="%{text}", colorbar=dict(title="IDR")))
    fig.update_xaxes(title="WACC")
    fig.update_yaxes(title="Terminal growth")
    show_chart(style_fig(fig, 400, f"WACC vs Terminal Growth ({scn}; colour centred on current price)", unified=False), key="heatmap")


# =============================================================================
# 10. UI: TAB 4 - PEER COMPS
# =============================================================================
def scatter_with_trend(df: pd.DataFrame, x: str, y: str, xt: str, yt: str, title: str, key: str):
    peers, icbp = df[df["ticker"] != "ICBP"], df[df["ticker"] == "ICBP"].iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=peers[x], y=peers[y], mode="markers+text", text=peers["ticker"], textposition="top center",
                             name="Peers", marker=dict(size=15, color=BLUE, line=dict(width=1, color="#F8FAFC"))))
    fig.add_trace(go.Scatter(x=[icbp[x]], y=[icbp[y]], mode="markers+text", text=["ICBP"], textposition="top center",
                             name="ICBP", marker=dict(size=22, color=TEAL, symbol="diamond", line=dict(width=1, color="#F8FAFC"))))
    prem, r2 = None, None
    if len(peers) >= 3:
        slope, icpt = np.polyfit(peers[x], peers[y], 1)
        xs = np.linspace(min(peers[x].min(), icbp[x]), max(peers[x].max(), icbp[x]), 50)
        fig.add_trace(go.Scatter(x=xs, y=slope * xs + icpt, mode="lines", name="Peer regression", line=dict(color=AMBER, dash="dash")))
        implied = slope * icbp[x] + icpt
        prem = icbp[y] / implied - 1 if implied > 0 else None
        r2 = float(np.corrcoef(peers[x], peers[y])[0, 1] ** 2)
    fig.update_xaxes(title=xt)
    fig.update_yaxes(title=yt)
    show_chart(style_fig(fig, 400, title, unified=False), key=key)
    return prem, r2


def render_comps_tab(ctx: dict) -> None:
    comps = ctx["comps"]
    st.subheader("Comparable Companies")
    names = {"mcap_tn": "Mkt Cap (IDR T)", "pe_ttm": "P/E TTM", "pe_fwd": "P/E Fwd", "ev_ebitda": "EV/EBITDA", "pbv": "P/BV",
             "roe": "ROE %", "op_margin": "Op Margin %", "div_yield": "Div Yield %", "ebitda_growth": "EBITDA Growth %"}
    t = comps.set_index("ticker")[list(names)].rename(columns=names)
    sty = (t.style.format("{:,.1f}").format("{:,.2f}", subset=["P/BV"])
           .apply(lambda r: ["background-color: rgba(0,245,212,0.15); font-weight:700" if r.name == "ICBP" else "" for _ in r], axis=1))
    show_df(sty)
    peers = comps[comps["ticker"] != "ICBP"]
    icbp = comps.iloc[0]
    st.markdown("**ICBP premium / (discount) to peer median**")
    cols = st.columns(5)
    for col, (lab, key) in zip(cols, [("P/E TTM", "pe_ttm"), ("P/E Fwd", "pe_fwd"), ("EV/EBITDA", "ev_ebitda"), ("P/BV", "pbv"), ("ROE", "roe")]):
        med = peers[key].median()
        col.metric(lab, f"{icbp[key]:.1f}{'%' if key == 'roe' else 'x'}", f"{(icbp[key] / med - 1) * 100:+.0f}% vs median {med:.1f}")
    st.caption("ICBP multiples are computed from the model (price, LTM earnings, FY25 book value); peer figures are synthetic.")

    st.subheader("Valuation Maps")
    hide = st.checkbox("Exclude UNVR (outlier: ROE ~80%, P/BV ~14x) from charts and regression", value=True, key="hide_unvr")
    df = comps[comps["ticker"] != "UNVR"] if hide else comps
    a, b = st.columns(2)
    with a:
        prem, r2 = scatter_with_trend(df, "roe", "pbv", "ROE (%)", "P/BV (x)", "ROE vs P/BV", "sc1")
        if prem is not None:
            st.metric("ICBP P/BV vs regression-implied", f"{prem:+.0%}", f"R² = {r2:.2f} (n={len(df) - 1} peers)")
    with b:
        prem2, r22 = scatter_with_trend(df, "ebitda_growth", "ev_ebitda", "EBITDA growth (%)", "EV/EBITDA (x)", "EBITDA Growth vs EV/EBITDA", "sc2")
        if prem2 is not None:
            st.metric("ICBP EV/EBITDA vs regression-implied", f"{prem2:+.0%}", f"R² = {r22:.2f} (n={len(df) - 1} peers)")
    st.caption("With only 4-5 peers the regressions are illustrative; treat the premium/discount as a screening signal, not a valuation.")


# =============================================================================
# 11. UI: TAB 5 - TECHNICALS & MACRO
# =============================================================================
def render_technical_tab(ctx: dict) -> None:
    px = add_indicators(ctx["data"]["price"])
    st.subheader("Price Action & Momentum")
    lb = st.radio("Lookback", ["3M", "6M", "1Y", "2Y", "Max"], index=2, horizontal=True, key="lookback")
    n = {"3M": 63, "6M": 126, "1Y": 252, "2Y": 504, "Max": None}[lb]
    d = px.tail(n) if n else px
    last = px.iloc[-1]
    m = st.columns(5)
    m[0].metric("Last close", f"{last['close']:,.0f}", f"{last['close'] / px['close'].iloc[-2] - 1:+.2%}")
    m[1].metric("RSI (14)", f"{last['rsi']:.0f}", "Overbought" if last["rsi"] > 70 else ("Oversold" if last["rsi"] < 30 else "Neutral"), delta_color="off")
    m[2].metric("vs MA200", f"{(last['close'] / last['ma200'] - 1) * 100:+.1f}%", "MA50 > MA200" if last["ma50"] > last["ma200"] else "MA50 < MA200", delta_color="off")
    m[3].metric("Realised vol (30d, ann.)", f"{last['vol30']:.1f}%")
    hi52, lo52 = px.tail(252)["high"].max(), px.tail(252)["low"].min()
    m[4].metric("52W range position", f"{(last['close'] - lo52) / (hi52 - lo52):.0%}", f"{lo52:,.0f} - {hi52:,.0f}", delta_color="off")

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.5, 0.14, 0.18, 0.18])
    fig.add_trace(go.Candlestick(x=d["trade_date"], open=d["open"], high=d["high"], low=d["low"], close=d["close"], name="ICBP",
                                 increasing_line_color=TEAL, increasing_fillcolor=TEAL,
                                 decreasing_line_color=RED, decreasing_fillcolor=RED), row=1, col=1)
    fig.add_trace(go.Scatter(x=d["trade_date"], y=d["ma50"], name="MA50", line=dict(color=AMBER, width=1.6)), row=1, col=1)
    fig.add_trace(go.Scatter(x=d["trade_date"], y=d["ma200"], name="MA200", line=dict(color=BLUE, width=1.6)), row=1, col=1)
    vcol = np.where(d["close"] >= d["open"], TEAL, RED)
    fig.add_trace(go.Bar(x=d["trade_date"], y=d["volume"], marker_color=vcol, name="Volume", opacity=0.7), row=2, col=1)
    fig.add_trace(go.Scatter(x=d["trade_date"], y=d["rsi"], name="RSI (14)", line=dict(color="#8B5CF6", width=1.6)), row=3, col=1)
    fig.add_hline(y=70, line_dash="dot", line_color=RED, row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color=TEAL, row=3, col=1)
    fig.add_trace(go.Scatter(x=d["trade_date"], y=d["vol30"], name="Ann. vol 30d (%)", fill="tozeroy",
                             line=dict(color=AMBER, width=1.4), fillcolor="rgba(245,158,11,0.15)"), row=4, col=1)
    fig.update_xaxes(rangeslider_visible=False, rangebreaks=[dict(bounds=["sat", "mon"])])
    fig.update_yaxes(title_text="IDR", row=1, col=1)
    fig.update_yaxes(title_text="Vol", row=2, col=1)
    fig.update_yaxes(title_text="RSI", range=[0, 100], row=3, col=1)
    fig.update_yaxes(title_text="Vol %", row=4, col=1)
    show_chart(style_fig(fig, 820, f"{TICKER} - Price, Volume, RSI and Rolling Volatility"), key="tech")


def render_macro_section(ctx: dict) -> None:
    st.subheader("Macro & Commodity Sensitivity Analyzer")
    mb = macro_base(ctx["fin"])
    macro = ctx["data"]["macro"]
    now = macro.iloc[-1]
    st.caption(f"Latest macro (mock): USD/IDR {now['usdidr']:,.0f} | wheat ${now['wheat_usd_bu']:.2f}/bu | CPO ${now['cpo_usd_t']:,.0f}/t | "
               f"BI rate {now['bi_rate_pct']:.2f}% | inflation {now['inflation_yoy_pct']:.2f}%. "
               f"Base = FY{int(ctx['fin'].iloc[-1]['fiscal_year'])}: COGS mix wheat {COST_MIX['wheat']:.0%}, CPO {COST_MIX['cpo']:.0%}, "
               f"other raw/packaging {COST_MIX['other_raw']:.0%}, overhead {COST_MIX['overhead']:.0%}.")
    left, right = st.columns([1, 2])
    with left:
        fx = st.slider("USD/IDR change (%)", -20.0, 30.0, 0.0, 1.0, key="mx_fx")
        wheat = st.slider("Global wheat price (%)", -30.0, 50.0, 0.0, 1.0, key="mx_wheat")
        cpo = st.slider("CPO price (%)", -30.0, 50.0, 0.0, 1.0, key="mx_cpo")
        bi = st.slider("BI rate change (bps)", -200, 200, 0, 25, key="mx_bi")
        infl = st.slider("Domestic inflation change (pp)", -2.0, 4.0, 0.0, 0.25, key="mx_infl")
        pt = st.slider("Price pass-through of cost change (%)", 0.0, 100.0, 35.0, 5.0, key="mx_pt")
    shocks = dict(fx=fx / 100, wheat=wheat / 100, cpo=cpo / 100, bi_bps=float(bi), infl_pp=infl, pass_through=pt / 100)
    out = macro_impact(mb, **shocks)
    with right:
        m = st.columns(4)
        m[0].metric("COGS change", f"{out['d_cogs_pct']:+.1%}")
        m[1].metric("Gross margin", f"{out['gm_new']:.1%}", f"{(out['gm_new'] - out['gm_base']) * 1e4:+.0f} bps")
        m[2].metric("EBIT change", f"{out['d_ebit_pct']:+.1%}")
        m[3].metric("EPS (IDR)", f"{out['eps_new']:,.0f}", f"{out['d_eps_pct']:+.1%}")
        comp = out["components"]
        labels = ["Base EPS"] + list(comp) + ["Pro forma EPS"]
        vals = [mb["eps"]] + list(comp.values()) + [out["eps_new"]]
        fig = go.Figure(go.Waterfall(x=labels, y=vals, measure=["absolute"] + ["relative"] * len(comp) + ["total"],
                                     increasing=dict(marker=dict(color=TEAL)), decreasing=dict(marker=dict(color=RED)),
                                     totals=dict(marker=dict(color=BLUE)), connector=dict(line=dict(color="#475569"))))
        fig.update_yaxes(title="IDR per share")
        show_chart(style_fig(fig, 340, "EPS Bridge: Base to Pro Forma", unified=False), key="mx_wf")

    a, b = st.columns(2)
    with a:
        factors = [("USD/IDR ±10%", "fx", 0.10), ("Wheat ±20%", "wheat", 0.20), ("CPO ±20%", "cpo", 0.20),
                   ("BI rate ±100bp", "bi_bps", 100.0), ("Inflation ±1pp", "infl_pp", 1.0)]
        rows = []
        for lab, k, sz in factors:
            up = macro_impact(mb, **{**{"pass_through": pt / 100}, k: sz})["d_eps_pct"] * 100
            dn = macro_impact(mb, **{**{"pass_through": pt / 100}, k: -sz})["d_eps_pct"] * 100
            rows.append((lab, up, dn))
        tor = pd.DataFrame(rows, columns=["factor", "up", "down"])
        tor = tor.reindex(tor[["up", "down"]].abs().max(axis=1).sort_values().index)
        fig = go.Figure()
        fig.add_bar(y=tor["factor"], x=tor["up"], orientation="h", name="Shock up", marker_color=RED)
        fig.add_bar(y=tor["factor"], x=tor["down"], orientation="h", name="Shock down", marker_color=TEAL)
        fig.update_layout(barmode="relative")
        fig.update_xaxes(title="EPS change (%)")
        show_chart(style_fig(fig, 340, "Tornado: EPS Sensitivity by Factor", unified=False), key="tornado")
    with b:
        corr = macro_correlation(ctx["data"]["price"], macro)
        fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.index, zmin=-1, zmax=1,
                                   colorscale=[[0, RED], [0.5, "#1F2937"], [1, TEAL]],
                                   text=np.round(corr.values, 2), texttemplate="%{text}"))
        show_chart(style_fig(fig, 340, "Monthly Change Correlations (ICBP vs Macro)", unified=False), key="corr")
    st.caption("The correlation matrix is computed on synthetic series, so it illustrates the method only. The scenario model above uses explicit cost-mix and pass-through assumptions.")

    a, b = st.columns(2)
    with a:
        reb = pd.DataFrame({"date": macro["obs_date"]})
        for name, col in [("USD/IDR", "usdidr"), ("Wheat", "wheat_usd_bu"), ("CPO", "cpo_usd_t")]:
            reb[name] = macro[col] / macro[col].iloc[0] * 100
        fig = go.Figure()
        for name, color in zip(["USD/IDR", "Wheat", "CPO"], [TEAL, AMBER, BLUE]):
            fig.add_trace(go.Scatter(x=reb["date"], y=reb[name], name=name, line=dict(color=color, width=2)))
        show_chart(style_fig(fig, 320, "FX & Commodities (rebased to 100)"), key="mx_hist1")
    with b:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=macro["obs_date"], y=macro["bi_rate_pct"], name="BI rate %", line=dict(color=RED, width=2, shape="hv")), secondary_y=False)
        fig.add_trace(go.Scatter(x=macro["obs_date"], y=macro["inflation_yoy_pct"], name="Inflation YoY %", line=dict(color=TEAL, width=2)), secondary_y=False)
        show_chart(style_fig(fig, 320, "Policy Rate & Inflation"), key="mx_hist2")


# =============================================================================
# 12. UI: TAB 6 - PROVENANCE, VALIDATION, DOCS
# =============================================================================
def render_provenance_tab(ctx: dict) -> None:
    st.subheader("Calculation Audit & Validation Checks")
    checks = run_validation(ctx)
    passed = int(checks["Status"].str.contains("PASS").sum())
    (st.success if passed == len(checks) else st.error)(f"{passed} / {len(checks)} checks passed")
    show_df(checks, hide_index=True)

    st.subheader("Data Lineage")
    st.code(SQL_PIPELINE_DOC, language="sql")
    with st.expander("All view definitions (SQL)"):
        for name, sql in VIEW_SQL.items():
            st.markdown(f"**{name}**")
            st.code(sql, language="sql")

    st.subheader("Exportable Research Note")
    note = build_research_note(ctx)
    a, b = st.columns(2)
    with a:
        st.markdown("**Preview**")
        with st.container(border=True):
            st.markdown(note)
    with b:
        st.markdown("**Copyable markdown**")
        st.code(note, language="markdown")
    st.download_button("⬇ Download research note (.md)", data=note.encode("utf-8"), file_name="ICBP_research_note.md", mime="text/markdown")

    st.subheader("GitHub README.md Template")
    readme = build_readme()
    with st.expander("Preview README", expanded=False):
        st.markdown(readme)
    st.code(readme, language="markdown")
    st.download_button("⬇ Download README.md", data=readme.encode("utf-8"), file_name="README.md", mime="text/markdown")


# =============================================================================
# 13. TAB ROUTER & MAIN
# =============================================================================
def render_tabs(ctx: dict) -> None:
    tabs = st.tabs(["📋 Executive Summary", "📊 Fundamentals", "🧮 DCF Valuation", "⚖️ Peer Comps",
                    "📉 Technicals & Macro", "🧾 Data & Docs"])
    with tabs[0]:
        render_summary_tab(ctx)
    with tabs[1]:
        render_fundamentals_tab(ctx)
    with tabs[2]:
        render_dcf_tab(ctx)
    with tabs[3]:
        render_comps_tab(ctx)
    with tabs[4]:
        render_technical_tab(ctx)
        st.divider()
        render_macro_section(ctx)
    with tabs[5]:
        render_provenance_tab(ctx)


def main() -> None:
    inject_css()
    init_state()
    st.title("📈 ICBP Equity Research Terminal")
    st.caption(f"{COMPANY} (IDX: {TICKER}) | Synthetic data for demonstration | Pricing date {AS_OF:%d %b %Y}")

    data = load_data()
    period, scenario = st.session_state["period"], st.session_state["scenario"]
    assumptions = {s: get_assumptions(s) for s in SCENARIOS}
    fin = compute_financial_ratios(data["income"], data["balance"], data["cashflow"], wacc=assumptions[scenario]["wacc"])
    q = build_quarterly_frame(data["quarterly"])
    last_close = float(data["price"]["close"].iloc[-1])
    base = build_dcf_base(fin)
    dcf = {s: run_dcf_model(base, assumptions[s], last_close) for s in SCENARIOS}
    tp = round(dcf[scenario]["price"] / 50) * 50
    mea = data["geo"][data["geo"]["region"] == "Middle East & Africa"].sort_values("fiscal_year")["share"]

    ctx = dict(data=data, fin=fin, q=q, ltm=ltm_block(q, fin), base=base, dcf=dcf, period=period, scenario=scenario,
               last_close=last_close, tp=tp, rating=rating_from_upside(tp / last_close - 1),
               mea_share=float(mea.iloc[-1]), mea_share_start=float(mea.iloc[0]))
    ctx["comps"] = build_comps(ctx)
    render_sidebar(ctx)
    render_tabs(ctx)


main()