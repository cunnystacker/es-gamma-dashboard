# ES Gamma Tracker

Minimal starter Streamlit dashboard for options gamma exposure and simplified Expected Shortfall (ES) monitoring.

## Features (Starter Version)

- Editable positions table (live updates)
- CSV upload for your own position data
- Key risk metrics:
  - Total Gamma Exposure
  - Net Delta Exposure
  - Gross |Gamma|
  - Simplified 1-day Expected Shortfall estimate
- Gamma exposure by strike (Plotly bar chart)
- Approximate P&L curve vs spot move
- Sample data + export

## Quick Start

### 1. Create virtual environment (recommended)

```bash
cd es_gamma_tracker
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run dashboard.py
```

The app will open in your browser at `http://localhost:8501`

## Position CSV Format

Your CSV should contain these columns:

| symbol | type | strike | qty | delta | gamma |
|--------|------|--------|-----|-------|-------|
| SPX 520C | Call | 520 | 25 | 0.52 | 0.042 |

- `qty` can be positive (long) or negative (short)
- `delta` and `gamma` are per-contract values

## Next Steps (Ideas)

- Replace the toy ES calculation with real historical or parametric simulation
- Add live data feed (Polygon, Bloomberg, etc.)
- Add vanna, charm, and higher-order greeks
- Persist positions in a database or file
- Add scenario stress testing

This is intentionally minimal so you can extend it quickly with your real risk logic.

## License

MIT (or whatever you prefer)