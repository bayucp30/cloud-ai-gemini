import pywhatkit as kit
import time
from datetime import datetime
import requests
import os
import pyautogui
import json

def kirim_wa(nomor, pesan, file_grafik=None):
    if not nomor.startswith("+"):
        nomor = "+" + nomor
# ==========================================
# KONFIGURASI WHATSAPP CLOUD API
# Dapatkan data ini dari: developers.facebook.com -> My Apps -> WhatsApp -> API Setup
# ==========================================

    now = datetime.now()
    jam = now.hour
    menit = now.minute + 2
# Token sementara (berlaku 24 jam) atau Token Permanen (System User)
WA_TOKEN = "MASUKKAN_ACCESS_TOKEN_DARI_META_DISINI"

    if file_grafik and os.path.exists(file_grafik):
        print(f"Menyiapkan WhatsApp untuk {nomor} dengan teks + grafik...")
        kit.sendwhats_image(
            nomor,
            file_grafik,
            caption=pesan,
            wait_time=20,
            tab_close=False,
            close_time=5
        )
        print("Menunggu upload gambar selesai...")
        time.sleep(15)   # <-- INI KUNCI STABIL
# Phone Number ID (Bukan nomor HP, tapi ID angka panjang)
PHONE_ID = "MASUKKAN_PHONE_NUMBER_ID_DISINI" 

        # tekan enter manual
        pyautogui.press("enter")
VERSI_API = "v19.0"

def upload_media(file_path):
    """
    Upload gambar ke server WhatsApp Meta untuk mendapatkan ID Media.
    """
    url = f"https://graph.facebook.com/{VERSI_API}/{PHONE_ID}/media"
    
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}"
    }
    
    if not os.path.exists(file_path):
        print(f"File tidak ditemukan: {file_path}")
        return None

    # Membuka file dalam mode binary
    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'image/png'),
        'type': (None, 'image/png'),
        'messaging_product': (None, 'whatsapp')
    }
    
    try:
        print("Mengupload grafik ke server Meta...")
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        media_id = response.json().get("id")
        print(f"Upload sukses. Media ID: {media_id}")
        return media_id
    except Exception as e:
        print(f"Gagal upload media: {e}")
        if 'response' in locals():
            print(response.text)
        return None

def kirim_wa(nomor, pesan, file_grafik=None):
    """
    Mengirim pesan WA menggunakan Cloud API (Tanpa Browser).
    """
    url = f"https://graph.facebook.com/{VERSI_API}/{PHONE_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Bersihkan format nomor (Meta API biasanya butuh format internasional tanpa + atau dengan + tergantung setting, tapi umumnya angka saja aman)
    nomor_tujuan = nomor.replace("+", "").replace("-", "").strip()
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": nomor_tujuan,
    }

    if file_grafik:
        media_id = upload_media(file_grafik)
        if media_id:
            payload["type"] = "image"
            payload["image"] = {
                "id": media_id,
                "caption": pesan
            }
        else:
            # Fallback jika gambar gagal, kirim teks saja
            payload["type"] = "text"
            payload["text"] = {"body": pesan + "\n\n[Gambar gagal diupload]"}
    else:
        print(f"Menyiapkan WhatsApp untuk {nomor} dengan teks saja...")
        kit.sendwhatmsg(
            nomor,
            pesan,
            jam,
            menit,
            wait_time=20,
            tab_close=False,
            close_time=5
        )
        payload["type"] = "text"
        payload["text"] = {"body": pesan}

    time.sleep(15)
    pyautogui.press("enter")
    print("Pesan berhasil dikirim!")

    # cooldown supaya WA siap untuk file berikutnya
    time.sleep(25)
    try:
        print(f"Mengirim request API ke {nomor_tujuan}...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ Pesan berhasil dikirim via Cloud API!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengirim pesan: {e}")
        if 'response' in locals():
            print("Detail Error Meta:", response.text)