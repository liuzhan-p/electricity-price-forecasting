# Electricity Price Forecasting — Group C Prototype

This is an interactive Streamlit prototype with entirely synthetic data and dummy model predictions. It is **not** a validated electricity-price forecasting model.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Features: adjustable time window, two dummy model series, MAE/RMSE against synthetic reference values, table and CSV export.

## Integration plan

- Replace `make_data()` with a loader for Group A's cleaned dataset.
- Agree with Group B on a common prediction interface: timestamp, actual (if available), model_name, predicted_price_eur_mwh.
- Agree on timezone, forecast horizon, and day-ahead vs intraday target before integrating.
- Compute metrics only on held-out timestamps with known actual prices.
