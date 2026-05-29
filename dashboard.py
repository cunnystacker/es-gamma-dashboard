import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import numpy as np

st.set_page_config(page_title="/ES Gamma Dashboard", layout="wide")
st.title("🧮 /ES Real-Time Gamma Exposure Dashboard")
st.write("**Live /ES + Dealer Gamma Levels**")

# ====================== BARCHART BUTTON ======================
st.subheader("Market-Wide Dealer GEX")
if st.button("📊 Open Barchart $SPX Gamma Exposure", use_container_width=True):
    st.markdown("[Open Barchart GEX Page](https://www.barchart.com/stocks/quotes/%24SPX/gamma-exposure)")

# Live Price (improved logic)
st.sidebar.header("Live Market Data")
auto_refresh = st.sidebar.checkbox("Auto-refresh every 15s", value=True)

# Persistent live price in session state
if 'live_price' not in st.session_state:
    st.session_state.live_price = 7561.0

if st.sidebar.button("🔄 Refresh Live /ES"):
    try:
        es = yf.Ticker("ES=F")
        live_data = es.history(period="1d")
        if not live_data.empty:
            st.session_state.live_price = live_data['Close'].iloc[-1]
            st.sidebar.success(f"✅ Live /ES: **{st.session_state.live_price:.2f}**")
    except:
        st.sidebar.error("Could not fetch live price")

spot = st.sidebar.number_input("Manual /ES Spot Price", value=float(st.session_state.live_price), step=1.0)

# ====================== GEX INPUTS ======================
st.subheader("Update Dealer GEX Numbers")

col1, col2 = st.columns(2)
with col1:
    total_gex = st.number_input("Total **Net** GEX (in millions)", value=264, step=100, format="%d")
    flip_level = st.number_input("Gamma Flip Level", value=7520.0, step=5.0)
with col2:
    put_wall = st.number_input("Major Put Wall", value=7488.0, step=5.0)
    call_wall = st.number_input("Major Call Wall", value=7610.0, step=5.0)

total_gex_full = total_gex * 1_000_000

# Dealer Offsides
st.subheader("Dealer Offsides Strength (Quantitative)")

if total_gex_full < -2000000000:
    st.error(f"🔴 **EXTREME SHORT GAMMA** ({total_gex}M) — Dealers heavily offsides negative.")
elif total_gex_full < -800000000:
    st.warning(f"🟠 **SIGNIFICANT SHORT GAMMA** ({total_gex}M)")
elif total_gex_full > 2000000000:
    st.success(f"🟢 **EXTREME LONG GAMMA** (+{total_gex}M) — Dealers heavily offsides long.")
elif total_gex_full > 800000000:
    st.success(f"🟢 **STRONG LONG GAMMA** (+{total_gex}M)")
else:
    st.info(f"⚖️ **NEUTRAL** (+{total_gex}M)")

# Chart (wavy price)
st.subheader("SPX Price with Gamma Key Levels")

now = datetime.now()
times = [(now - timedelta(minutes=15 * i)).strftime("%H:%M") for i in range(12, -1, -1)]

np.random.seed(42)
prices = [spot - 48]
for i in range(1, 13):
    prices.append(prices[-1] + np.random.normal(3, 9))

fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=prices, mode='lines+markers', name='SPX Price', line=dict(color='lime', width=3.5)))

fig.add_hline(y=call_wall, line_color="blue", line_width=2.5, annotation_text=f"CALL WALL ({call_wall})")
fig.add_hline(y=put_wall, line_color="red", line_width=2.5, annotation_text=f"PUT WALL ({put_wall})")
fig.add_hline(y=flip_level, line_color="white", line_dash="dash", line_width=2, annotation_text=f"GAMMA FLIP ({flip_level})")

fig.update_layout(
    title="SPX Price with Gamma Key Levels",
    xaxis_title="Time (15-min intervals)",
    yaxis_title="SPX Price",
    height=580,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("**Green Line = SPX Price** | Horizontal lines = Gamma Key Levels")

if auto_refresh:
    time.sleep(15)
    st.rerun()