import os
import time
from datetime import datetime
from typing import Optional

import pywhatkit as kit


def kirim_wa(nomor: str, pesan: str, file_grafik: Optional[str] = None) -> bool:
    """Kirim pesan via WhatsApp Web menggunakan pywhatkit."""
    if not nomor:
        print("Nomor tujuan kosong.")
        return False

    if not nomor.startswith("+"):
        nomor = "+" + nomor

    now = datetime.now()
    jam = now.hour
    menit = (now.minute + 2) % 60
    if now.minute >= 58:
        jam = (jam + 1) % 24

    try:
        if isinstance(file_grafik, str) and os.path.exists(file_grafik):
            print(f"Menyiapkan WhatsApp Web untuk {nomor} (teks + grafik)...")
            kit.sendwhats_image(
                receiver=nomor,
                img_path=file_grafik,
                caption=pesan,
                wait_time=20,
                tab_close=False,
                close_time=5,
            )
        else:
            print(f"Menyiapkan WhatsApp Web untuk {nomor} (teks saja)...")
            kit.sendwhatmsg(
                phone_no=nomor,
                message=pesan,
                time_hour=jam,
                time_min=menit,
                wait_time=20,
                tab_close=False,
                close_time=5,
            )

        time.sleep(10)
        print("Pesan berhasil dikirim via WhatsApp Web.")
        return True
    except Exception as e:
        print(f"Gagal mengirim via WhatsApp Web: {e}")
        return False
