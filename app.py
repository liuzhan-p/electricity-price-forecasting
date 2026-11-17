"""Group C electricity forecasting UI prototype. All data and predictions are synthetic."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Electricity Price Forecasting | Group C", layout="wide")
st.title("Electricity Price Forecasting")
st.caption("Group C prototype • SYNTHETIC DEMO DATA — not actual market prices or trained model outputs")

@st.cache_data
def make_data():
    rng = np.random.default_rng(42)
    index = pd.date_range("2026-10-01", periods=24 * 21, freq="h", tz="Europe/Berlin")
    hour = index.hour.to_numpy()
    weekday = index.dayofweek.to_numpy()
    baseline = 75 + 17 * np.sin(2 * np.pi * (hour - 7) / 24) + 8 * (weekday < 5)
    actual = baseline + rng.normal(0, 8, len(index))
    model_a = baseline + rng.normal(0, 6, len(index))
    model_b = baseline + 4 + rng.normal(0, 10, len(index))
    return pd.DataFrame({"Actual": actual, "Dummy Model A": model_a, "Dummy Model B": model_b}, index=index)

data = make_data()
window = st.sidebar.slider("Days to display", 1, 21, 7)
selected_models = st.sidebar.multiselect("Compare models", ["Dummy Model A", "Dummy Model B"], default=["Dummy Model A", "Dummy Model B"])
view = data.tail(window * 24)

st.subheader("Historical prices and simulated predictions")
fig = go.Figure()
fig.add_trace(go.Scatter(x=view.index, y=view["Actual"], mode="lines", name="Synthetic actual"))
for name in selected_models:
    fig.add_trace(go.Scatter(x=view.index, y=view[name], mode="lines", name=name, line={"dash": "dash"}))
fig.update_layout(xaxis_title="Time (Europe/Berlin)", yaxis_title="Electricity price (EUR/MWh)", hovermode="x unified", legend_title="Series")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Illustrative model comparison")
st.info("Metrics below compare synthetic predictions with synthetic reference values. They do not measure real model performance.")
cols = st.columns(max(1, len(selected_models)))
for col, name in zip(cols, selected_models):
    errors = view[name] - view["Actual"]
    with col:
        st.metric(f"{name} · MAE", f"{errors.abs().mean():.2f} EUR/MWh")
        st.metric(f"{name} · RMSE", f"{np.sqrt((errors ** 2).mean()):.2f} EUR/MWh")

st.subheader("Preview and export")
st.dataframe(view.reset_index(names="timestamp").tail(24), use_container_width=True)
st.download_button("Download synthetic sample CSV", data=view.reset_index(names="timestamp").to_csv(index=False), file_name="synthetic_forecasts.csv", mime="text/csv")
st.caption("Integration next step: replace make_data() with Group A's dataset loader and Group B's prediction adapter.")
