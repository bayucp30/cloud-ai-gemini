import sys
import time
import subprocess
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import ENGINE

# GANTI KE PATH GOOGLE DRIVE KAMU
WATCH_FOLDER = r"G:\My Drive\Client_Upload"
SCRIPT_PATH = r"cloud_ai_gemini\ai_analyst.py"

PROCESSED_FOLDER = "data/processed"
FAILED_FOLDER = "data/failed"

os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(FAILED_FOLDER, exist_ok=True)

if not os.path.exists(WATCH_FOLDER):
    print("ERROR: Folder tidak ditemukan!")
    print(WATCH_FOLDER)
    exit()

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            print(f"\nFile baru terdeteksi: {event.src_path}")
            print("Engine aktif:", ENGINE)
            print("Memproses laporan...\n")

            if ENGINE == "ollama":
                script = "local_ai_ollama/ai_analyst.py"
            elif ENGINE == "gemini":
                script = "cloud_ai_gemini/ai_analyst.py"
            else:
                print("ENGINE tidak dikenal di config.py")
                return

            result = subprocess.run([sys.executable, script, event.src_path])

            if result.returncode == 0:
                print("STATUS: SUCCESS")
            else:
                print("STATUS: FAILED")
                shutil.move(event.src_path, os.path.join(FAILED_FOLDER, os.path.basename(event.src_path)))


def process_existing_files():
    print("Scanning file lama...")

    files = [f for f in os.listdir(WATCH_FOLDER) if f.endswith(".csv")]

    if not files:
        print("Tidak ada backlog file.")
        return

    for file in files:
        full_path = os.path.join(WATCH_FOLDER, file)

        print(f"\nMemproses backlog: {full_path}")

        if ENGINE == "ollama":
            script = "local_ai_ollama/ai_analyst.py"
        elif ENGINE == "gemini":
            script = "cloud_ai_gemini/ai_analyst.py"
        else:
            print("ENGINE tidak dikenal")
            return

        result = subprocess.run([sys.executable, script, full_path])

        if result.returncode == 0:
            print("STATUS: SUCCESS")
        else:
            print("STATUS: FAILED")
            shutil.move(full_path, os.path.join(FAILED_FOLDER, os.path.basename(full_path)))

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(CSVHandler(), WATCH_FOLDER, recursive=False)

    process_existing_files()

    observer.start()

    print("Service berjalan... menunggu file masuk.")
    print("Watching:", WATCH_FOLDER)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()