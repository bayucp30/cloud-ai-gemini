import pandas as pd
from datetime import datetime, timedelta

# ======================
# ANOMALY DETECTOR
# ======================
def detect_anomaly(df):
    df["revenue"] = df["jumlah"] * df["harga"]

    daily = df.groupby("tanggal")["revenue"].sum()

    mean = daily.mean()
    std = daily.std()

    today_value = daily.iloc[-1]

    if today_value < mean - 2*std:
        return "TURUN_DRASTIS", today_value, mean
    elif today_value > mean + 2*std:
        return "NAIK_TIDAK_NORMAL", today_value, mean
    else:
        return None, today_value, mean


# ======================
# FORECAST PRODUK
# ======================
def predict_tomorrow(df):
    df["tanggal"] = pd.to_datetime(df["tanggal"])

    last_days = df[df["tanggal"] >= df["tanggal"].max() - timedelta(days=3)]

    pred = (
        last_days.groupby("produk")["jumlah"]
        .mean()
        .sort_values(ascending=False)
    )

    return pred.head(3)