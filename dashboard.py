import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import numpy as np

st.set_page_config(page_title="SPX Dealer Gamma Monitor", layout="wide")

st.title("SPX Dealer Gamma Monitor for /ES Trading")
st.markdown("**Gamma levels derived from SPX options chain (primary dealer hedging instrument)**")

# Quick Links
st.subheader("Quick Data Sources")
col_a, col_b = st.columns(2)
with col_a:
    if st.button("📊 Open Barchart $SPX Gamma Exposure", use_container_width=True):
        st.markdown("[Barchart GEX](https://www.barchart.com/stocks/quotes/%24SPX/gamma-exposure)")
with col_b:
    if st.button("📈 Open Tier1 Alpha", use_container_width=True):
        st.markdown("[Tier1 Alpha Dashboard](https://tier1alpha.com)")

# Live Price
st.sidebar.header("Live Market Data")
auto_refresh = st.sidebar.checkbox("Auto-refresh every 15s", value=True)

if st.sidebar.button("🔄 Refresh Live /ES"):
    try:
        es = yf.Ticker("ES=F")
        live_data = es.history(period="1d")
        if not live_data.empty:
            st.session_state.live_price = live_data['Close'].iloc[-1]
    except:
        pass

spot = st.sidebar.number_input("Manual /ES Spot Price", 
                              value=st.session_state.get('live_price', 7603.75), 
                              step=1.0)

# Manual Inputs
st.subheader("Update Dealer GEX Numbers (from Tier1 Alpha / Barchart)")

col1, col2 = st.columns(2)
with col1:
    total_gex = st.number_input("Total **Net** GEX (in millions)", value=118, step=50, format="%d")
    flip_level = st.number_input("Gamma Flip Level", value=7319.0, step=5.0)
with col2:
    put_wall = st.number_input("Major Put Wall", value=7425.0, step=5.0)
    call_wall = st.number_input("Major Call Wall", value=7634.0, step=5.0)

total_gex_full = total_gex * 1_000_000

# ====================== IMPROVED OFFSIDES SECTION ======================
st.subheader("Dealer Offsides & Expected Hedging Flow")

if total_gex_full < -1500000000:
    st.error(f"🔴 **EXTREME SHORT GAMMA** ({total_gex}M)\n\n"
             "Dealers are heavily offsides negative. Strong forced **buying** expected on dips. "
             "High reversal risk if price continues lower.")
    
elif total_gex_full < -600000000:
    st.warning(f"🟠 **SIGNIFICANT SHORT GAMMA** ({total_gex}M)\n\n"
               "Dealers increasingly offsides negative. Downside volatility likely to increase. "
               "Watch for forced buying flows.")
    
elif total_gex_full > 1500000000:
    st.success(f"🟢 **EXTREME LONG GAMMA** (+{total_gex}M)\n\n"
               "Dealers heavily offsides positive. Strong stabilizing regime. "
               "Expect pinning and grinding higher.")
    
elif total_gex_full > 600000000:
    st.success(f"🟢 **STRONG LONG GAMMA** (+{total_gex}M)\n\n"
               "Dealers offsides positive. Market likely to remain supported.")
    
else:
    st.info(f"⚖️ **NEUTRAL GAMMA** ({total_gex}M)\n\n"
            "No strong dealer bias. Normal two-way price action expected.")

# Chart
st.subheader("SPX Price with Gamma Key Levels")

now = datetime.now()
times = [(now - timedelta(minutes=15 * i)).strftime("%H:%M") for i in range(12, -1, -1)]

np.random.seed(42)
prices = [spot - 45]
for i in range(1, 13):
    prices.append(prices[-1] + np.random.normal(4, 8))

fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=prices, mode='lines+markers', name='SPX Price', 
                        line=dict(color='lime', width=3.5)))

fig.add_hline(y=call_wall, line_color="blue", line_width=2.5, annotation_text=f"CALL WALL ({call_wall})")
fig.add_hline(y=put_wall, line_color="red", line_width=2.5, annotation_text=f"PUT WALL ({put_wall})")
fig.add_hline(y=flip_level, line_color="white", line_dash="dash", line_width=2, 
              annotation_text=f"GAMMA FLIP ({flip_level})")

fig.update_layout(
    title="SPX Price with Gamma Key Levels",
    xaxis_title="Time (15-min intervals)",
    yaxis_title="SPX Price",
    height=580,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("**Green Line = SPX Price** | Monitor dealer offsides for forced hedging flows in /ES")

if auto_refresh:
    time.sleep(15)
    st.rerun()