from iqoptionapi.stable_api import IQ_Option
import time
import pandas as pd
import requests

# ==============================
# 🔐 CREDENCIALES
# ==============================
EMAIL = "@gmail.com"
PASSWORD = "contraseña@"

# ==============================
# ⚙️ CONFIGURACIÓN
# ==============================
ACTIVO = "AUDJPY"

MAX_OPERACIONES_DIA = 1
operaciones_hoy = 0
dia_actual = time.strftime("%Y-%m-%d")

ultimo_soporte = None
tolerancia = 0.00002

# 🔥 MARTINGALA PERSONALIZADA
secuencia_martingala = [1]
indice_mg = 0

# ==============================
# 📩 TELEGRAM
# ==============================
TELEGRAM_TOKEN = "TOKEN_BOT"
CHAT_ID = "ID"

def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": mensaje}
        requests.post(url, data=data)
    except Exception as e:
        print("Error Telegram:", e)

# ==============================
# 🔌 CONEXIÓN
# ==============================
Iq = IQ_Option(EMAIL, PASSWORD)
Iq.connect()

if Iq.check_connect():
    print("✅ Conectado")
    enviar_telegram("🤖 BOT CONECTADO — Modo Señales (sin operar)")
else:
    print("❌ Error conexión")
    enviar_telegram("❌ ERROR AL CONECTAR BOT")
    exit()

Iq.change_balance("REAL")
print("🤖 BOT PATRÓN INICIADO — Modo Señales (sin operar)")

# ==============================
# 🔍 PATRÓN (4 velas históricas)
# ==============================
def es_patron_4velas(df):
    """
    Evalúa el patrón con las 4 velas históricas cerradas.
    La quinta vela (actual/en curso) se evalúa por separado en el loop.

    Patrón:
      Vela 1: Roja (bajista)
      Vela 2: Verde (alcista)
      Vela 3: Verde (alcista)
      Vela 4: Roja (bajista) — pero sin romper el mínimo de la vela 1
    """
    primera_roja  = df.iloc[0]['close'] < df.iloc[0]['open']
    segunda_verde = df.iloc[1]['close'] > df.iloc[1]['open']
    tercera_verde = df.iloc[2]['close'] > df.iloc[2]['open']
    cuarta_roja   = df.iloc[3]['close'] < df.iloc[3]['open']

    minimo_primera = df.iloc[0]['min']

    # La cuarta vela NO debe haber roto el mínimo de la primera
    cuarta_no_rompe = df.iloc[3]['min'] > minimo_primera

    if all([primera_roja, segunda_verde, tercera_verde, cuarta_roja, cuarta_no_rompe]):
        return True, minimo_primera

    return False, None

# ==============================
# 📉 FILTRO TENDENCIA BAJISTA
# ==============================
def tendencia_bajista(df):
    """
    Verifica que las últimas 3 velas cierren por debajo de la EMA 50.
    """
    ema = df['close'].ewm(span=50).mean()
    ultimas_velas = df.tail(3)

    for i in range(len(ultimas_velas)):
        precio = ultimas_velas.iloc[i]['close']
        ema_valor = ema.iloc[-len(ultimas_velas) + i]
        if precio >= ema_valor:
            return False

    return True

# ==============================
# 🔄 LOOP PRINCIPAL
# ==============================
while True:
    try:
        # Reset diario
        nuevo_dia = time.strftime("%Y-%m-%d")
        if nuevo_dia != dia_actual:
            dia_actual = nuevo_dia
            operaciones_hoy = 0
            print("🔄 Nuevo día — contador reiniciado")
            enviar_telegram("🔄 Nuevo día, contador reiniciado")

        # Límite diario alcanzado
        if operaciones_hoy >= MAX_OPERACIONES_DIA:
            print("🚫 Límite diario de señales alcanzado")
            time.sleep(10)
            continue

        segundos = int(time.strftime("%S"))

        # ✅ Solo actuar en los PRIMEROS 30 SEGUNDOS de la vela
        if segundos > 30:
            time.sleep(0.3)
            continue

        # Pedimos 6 velas: 4 para el patrón + 1 quinta vela en curso + 1 extra de margen
        velas = Iq.get_candles(ACTIVO, 60, 6, time.time())
        df = pd.DataFrame(velas)

        if len(df) < 5:
            print("⚠️ No hay suficientes velas")
            time.sleep(1)
            continue

        # Las 4 primeras velas son el patrón histórico (cerradas)
        df_patron = df.iloc[:4].reset_index(drop=True)

        # La quinta vela es la que está en curso (puede estar incompleta)
        vela_quinta = df.iloc[4]

        print(f"⏱ Seg: {segundos} | Chequeando patrón...")

        patron, soporte = es_patron_4velas(df_patron)

        if patron and tendencia_bajista(df):

            min_quinta = vela_quinta['min']
            print(f"🎯 Patrón detectado | Soporte: {soporte} | Min 5ta vela: {min_quinta}")

            # ✅ La quinta vela debe tocar o romper la mecha de la primera vela roja
            toca_soporte = min_quinta <= (soporte + tolerancia)

            if not toca_soporte:
                print("⏳ La quinta vela aún no toca el soporte")
                time.sleep(0.5)
                continue

            # Evitar señal duplicada en el mismo soporte
            if soporte == ultimo_soporte:
                print("⚠️ Soporte ya señalizado anteriormente, ignorando")
                time.sleep(1)
                continue

            # =====================
            # 📣 ENVIAR SEÑAL POR TELEGRAM (sin operar)
            # =====================
            monto_sugerido = secuencia_martingala[indice_mg]

            print(f"📣 SEÑAL DETECTADA — Enviando a Telegram | Monto sugerido: ${monto_sugerido} | Nivel MG: {indice_mg}")

            enviar_telegram(
                f"📣 SEÑAL DETECTADA\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🪙 Activo:          {ACTIVO}\n"
                f"📉 Dirección:       PUT 🔻\n"
                f"📌 Soporte:         {soporte:.5f}\n"
                f"💰 Monto sugerido: ${monto_sugerido}\n"
                f"🔁 Nivel MG:        {indice_mg}\n"
                f"⏰ Hora:            {time.strftime('%H:%M:%S')}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⚠️ Esta es solo una señal. Opera bajo tu propio criterio."
            )

            operaciones_hoy += 1
            ultimo_soporte = soporte

            print(f"✅ Señal enviada | Señales hoy: {operaciones_hoy}/{MAX_OPERACIONES_DIA}")

            # Pausa para no re-detectar la misma vela
            time.sleep(10)

        else:
            print(f"⏳ Sin patrón válido | Seg: {segundos}")

        time.sleep(0.5)

    except Exception as e:
        print(f"❌ Error en loop: {e}")
        enviar_telegram(f"❌ Error en bot: {e}")
        time.sleep(1)