import subprocess
import time
import os
import sys

# 📁 RUTA EXACTA DE TUS BOTS
BOT_DIR = r"C:\Users\olive\Desktop\aviso_a_telegran rompimiento_5"

# 📜 LISTA DE BOTS
bots = [
    "avisador_telegran1_AUDCAD.py",
    "avisador_telegran1_AUDJPY.py",
    "avisador_telegran1_EURGBP.py",
    "avisador_telegran1_EURJPY.py",
    "avisador_telegran1_EURUSD.py",
    "avisador_telegran1_GBPJPY.py",
    "avisador_telegran1_GBPUSD.py",
    "avisador_telegran1_USDCHF.py",
    "avisador_telegran1_USDJPY.py",


]




# ⏱️ ESPERA ENTRE BOTS
DELAY_ENTRE_BOTS = 60

print("🚀 Lanzando bots de trading de forma segura...\n")

python_exe = sys.executable  # usa el python correcto

for bot in bots:
    ruta_bot = os.path.join(BOT_DIR, bot)

    if not os.path.exists(ruta_bot):
        print(f"❌ No encontrado: {ruta_bot}")
        continue

    print(f"▶️ Ejecutando {bot}")

    subprocess.Popen(
        [python_exe, ruta_bot],
        cwd=BOT_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print(f"⏳ Esperando {DELAY_ENTRE_BOTS} segundos...\n")
    time.sleep(DELAY_ENTRE_BOTS)

print("✅ Todos los bots fueron lanzados correctamente.")
