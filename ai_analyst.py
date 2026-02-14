import sys
import pandas as pd
import os
import shutil
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from send_whatsapp import kirim_wa

# folder cloud_ai_gemini
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# root project (parent)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

# masukkan ke python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from business_guard import detect_anomaly, predict_tomorrow

# ======================
# LOAD ENV
# ======================
load_dotenv()
OWNER_NUMBER = os.getenv("OWNER_NUMBER")

# Gemini client
client = genai.Client()

# ======================
# PATH CONFIG (SHARED)
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "output")

INBOX_FOLDER = r"G:\My Drive\Client_Upload"
PROCESSED_FOLDER = os.path.join(DATA_DIR, "processed")
GRAPH_FOLDER = os.path.join(OUTPUT_DIR, "grafik")

os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)

# ======================
# AMBIL FILE TERBARU
# ======================
# ======================
# TERIMA FILE DARI WATCHER
# ======================
if len(sys.argv) < 2:
    print("Tidak ada file dikirim dari watcher")
    exit()

file_path = sys.argv[1]

if not os.path.exists(file_path):
    print("File tidak ditemukan:", file_path)
    exit()

print(f"Membaca file: {file_path}")


df = pd.read_csv(file_path, sep=None, engine="python", encoding="utf-8-sig")

# rapikan nama kolom
df.columns = df.columns.str.strip().str.lower()

# ======================
# BUSINESS LOGIC (REAL WORLD)
# ======================

# pastikan tipe data
df["tanggal"] = pd.to_datetime(df["tanggal"])
df["jumlah"] = pd.to_numeric(df["jumlah"])
df["harga"] = pd.to_numeric(df["harga"])

# revenue
df["revenue"] = df["jumlah"] * df["harga"]
df["bulan"] = df["tanggal"].dt.to_period("M").astype(str)

# ---------- kompatibilitas lama ----------
total = df.groupby("produk")["jumlah"].sum().sort_values(ascending=False)

terlaris = total.index[0]
terlambat = total.index[-1]

avg_sales = total.mean()
restock = total[total > avg_sales].index.tolist()
kurangi = total[total < avg_sales].index.tolist()

# ---------- analisis baru ----------
# performa cabang
branch_perf = df.groupby("cabang")["revenue"].sum().sort_values(ascending=False)
best_branch = branch_perf.index[0]

# warna favorit
fav_color = df.groupby("warna")["jumlah"].sum().idxmax()

# trend bulanan
monthly = df.groupby("bulan")["revenue"].sum().sort_index()
trend = "NAIK" if monthly.iloc[-1] > monthly.iloc[0] else "TURUN"

# anomali produk (z-score sederhana)
prod_rev = df.groupby("produk")["revenue"].sum()
z = (prod_rev - prod_rev.mean()) / prod_rev.std()

overperform = z[z > 1].index.tolist()
underperform = z[z < -1].index.tolist()

# ======================
# BUSINESS GUARD
# ======================
status, today, avg = detect_anomaly(df)
forecast = predict_tomorrow(df)

# ======================
# GEMINI AI NARASI
# ======================
def generate_report_text(
    terlaris, terlambat, restock, kurangi,
    best_branch, fav_color, trend, overperform, underperform
):

    prompt = f"""
Kamu adalah AI Business Analyst untuk pemilik toko bunga.

Buat insight profesional, natural, dan mudah dipahami.
Maksimal 7 kalimat.

DATA BISNIS:
Produk terlaris: {terlaris}
Produk terlambat: {terlambat}
Perlu restock: {', '.join(restock)}
Kurangi stok: {', '.join(kurangi)}
Cabang performa terbaik: {best_branch}
Warna bunga favorit pelanggan: {fav_color}
Trend penjualan: {trend}
Produk performa sangat tinggi: {', '.join(overperform)}
Produk performa sangat rendah: {', '.join(underperform)}

Fokus analisis:
1. Kondisi toko saat ini
2. Perilaku pelanggan
3. Risiko stok
4. Rekomendasi tindakan owner

Jangan tampilkan angka.
Jangan bullet point.
Bahasa santai profesional.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text

narasi = generate_report_text(
    terlaris, terlambat, restock, kurangi,
    best_branch, fav_color, trend, overperform, underperform
)

alert_text = ""
if status:
    alert_text = f"\n🚨 ALERT BISNIS: Penjualan {status}!\nHari ini: {int(today):,}\nRata-rata: {int(avg):,}\n"

forecast_text = "\n🔮 Prediksi Besok (Kemungkinan Laku):\n"
for p, v in forecast.items():
    forecast_text += f"- {p} (~{int(v)} pcs)\n"
# ======================
# LAPORAN FINAL
# ======================
laporan = f"""
🌸 *LAPORAN BISNIS HARIAN*
*TOKO BUNGA BERJAYA SELALU*
Tanggal : {datetime.now().strftime('%d-%m-%Y')}

📊 RINGKASAN OPERASIONAL
Produk Terlaris  : {terlaris}
Produk Lambat    : {terlambat}
Cabang Terbaik   : {best_branch}
Warna Favorit    : {fav_color}
Trend Penjualan  : {trend}

📦 MANAJEMEN STOK
Restock          : {', '.join(restock)}
Kurangi Stok     : {', '.join(kurangi)}

🧠 ANALISIS AI
{narasi}
"""
laporan = laporan + alert_text + forecast_text
print(laporan)

# ======================
# DASHBOARD GRAFIK
# ======================
GRAPH_FILE = os.path.join(GRAPH_FOLDER, "dashboard_penjualan.png")

fig, axs = plt.subplots(2,2, figsize=(12,8))

# 1 trend bulanan
monthly.plot(ax=axs[0,0], marker="o")
axs[0,0].set_title("Trend Revenue Bulanan")

# 2 performa cabang
branch_perf.plot(kind="bar", ax=axs[0,1])
axs[0,1].set_title("Revenue per Cabang")

# 3 warna favorit
df.groupby("warna")["jumlah"].sum().plot(kind="bar", ax=axs[1,0])
axs[1,0].set_title("Warna Bunga Favorit")

# 4 produk terlaris
total.head(10).plot(kind="barh", ax=axs[1,1])
axs[1,1].set_title("Top Produk")

plt.tight_layout()
plt.savefig(GRAPH_FILE, dpi=200)
plt.close()

GRAPH_FILE = os.path.abspath(GRAPH_FILE)
print(f"Grafik disimpan: {GRAPH_FILE}")

# ======================
# KIRIM WA
# ======================
kirim_wa(OWNER_NUMBER, laporan, file_grafik=GRAPH_FILE)

# ======================
# MAIN EXECUTION WRAPPER
# ======================
def main():
    global file_path
    global df

    # semua kode kamu tetap jalan karena sudah di atas
    pass


if __name__ == "__main__":
    try:
        # kode kamu SUDAH TERJALAN di atas
        shutil.move(file_path, os.path.join(PROCESSED_FOLDER, os.path.basename(file_path)))
        print("File dipindahkan ke processed.")
        sys.exit(0)

    except Exception as e:
        print("TERJADI ERROR:", e)
        sys.exit(1)