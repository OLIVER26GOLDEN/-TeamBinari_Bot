<!-- HEADER -->
<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,2,5,30&height=200&section=header&text=TeamBinari%20Bot&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Forex%20Signal%20Bot%20via%20Telegram%20%F0%9F%93%A1&descAlignY=58&descSize=16&descColor=00ff88)

[![Python](https://img.shields.io/badge/Python-3.10+-0d1117?style=for-the-badge&logo=python&logoColor=00ff88)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram_API-Bot-0d1117?style=for-the-badge&logo=telegram&logoColor=00ff88)](https://core.telegram.org/bots)
[![IQ Option](https://img.shields.io/badge/IQ_Option_API-Market_Data-0d1117?style=for-the-badge&logo=chartdotjs&logoColor=00ff88)](#)
[![Status](https://img.shields.io/badge/Status-Active-0d1117?style=for-the-badge&logo=statuspage&logoColor=00ff88)](#)

</div>

---

## 📡 ¿Qué es TeamBinari Bot?

**TeamBinari Bot** es un sistema de señales de trading desarrollado en Python que **monitorea los mercados de Forex en tiempo real** y te envía alertas directamente a Telegram cuando detecta una oportunidad de entrada.

> 💡 **La idea es simple:** no tienes que estar pegado a la pantalla analizando gráficos.  
> El bot analiza el mercado por ti y **te avisa cuando hay una señal — tú decides si operar o no.**

No ejecuta operaciones automáticamente. Es una herramienta de **asistencia y alertas**, no un sistema autónomo.

---

## 🔔 ¿Qué te envía el bot?

Cada vez que detecta una señal válida, te llega un mensaje así por Telegram:

```
📊 SEÑAL DETECTADA
──────────────────
📌 Asset     :  EURUSD
📈 Dirección :  CALL ▲
🔒 Soporte   :  1.0842
💰 Monto     :  $10
🔁 Martingala:  Nivel 1
🕐 Timestamp :  14:32:07 UTC
──────────────────
⚡ Powered by TeamBinari Bot
```

Toda la información que necesitas para tomar tu decisión, en un solo mensaje.

---

## ⚙️ ¿Cómo funciona?

```
┌─────────────────────────────────────────────────────┐
│                  FLUJO DEL BOT                      │
│                                                     │
│  IQ Option API                                      │
│      │                                              │
│      ▼                                              │
│  [ Obtiene velas en tiempo real ]                   │
│      │                                              │
│      ▼                                              │
│  [ Analiza patrón + EMA-50 + niveles ]              │
│      │                                              │
│      ├── Sin señal → Espera siguiente vela          │
│      │                                              │
│      └── Señal detectada                            │
│               │                                     │
│               ▼                                     │
│       [ Telegram API ]                              │
│               │                                     │
│               ▼                                     │
│       📲 Alerta en tu móvil                         │
└─────────────────────────────────────────────────────┘
```

**El bot NO ejecuta trades.** Solo analiza y alerta. Tú tienes el control total.

---

## 🧵 Multi-asset con Threading

El bot monitorea **varios pares de divisas al mismo tiempo** usando `threading` de Python:

```python
assets = ["EURUSD", "GBPUSD", "AUDUSD", "EURJPY", ...]

for asset in assets:
    t = threading.Thread(target=monitor_asset, args=(asset,))
    t.start()
```

Cada asset corre en su propio hilo — si hay señal en EURUSD y GBPUSD al mismo tiempo, recibes ambas alertas.

---

## 🛠️ Stack técnico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.10+ |
| Datos de mercado | IQ Option API |
| Alertas | Telegram Bot API |
| Concurrencia | `threading` |
| Análisis técnico | EMA-50, niveles de soporte, patrones de velas |

---

## 🚀 Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/OLIVER26GOLDEN/-TeamBinari_Bot.git
cd -TeamBinari_Bot

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. Configura tus credenciales en config.py
# - IQ Option: email y contraseña
# - Telegram: BOT_TOKEN y CHAT_ID

# 4. Ejecuta el bot
python bot.py
```

---

## 🔐 Configuración

Crea un archivo `config.py` con tus datos:

```python
# IQ Option
IQ_EMAIL    = "tu_email@gmail.com"
IQ_PASSWORD = "tu_contraseña"

# Telegram
BOT_TOKEN = "123456:ABC-tu_token_aqui"
CHAT_ID   = "tu_chat_id"
```

> ⚠️ **Nunca subas tus credenciales a GitHub.** Añade `config.py` a tu `.gitignore`.

---

## 📁 Estructura del proyecto

```
TeamBinari_Bot/
│
├── bot.py                  # Script principal
├── config.py               # Credenciales (no subir a Git)
├── strategy.py             # Lógica de análisis y señales
├── telegram_alert.py       # Envío de mensajes por Telegram
├── requirements.txt        # Dependencias
└── README.md
```

---

## ⚠️ Disclaimer

Este proyecto es una herramienta de **análisis y alertas** desarrollada con fines educativos y de automatización personal.  
No constituye asesoramiento financiero. Operar en mercados financieros conlleva riesgo. Úsalo bajo tu propia responsabilidad.

---

<!-- FOOTER -->
<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0,2,2,5,30&color=gradient&customColorList=0,2,2,5,30&height=100&section=footer)

**Desarrollado por [Oliver Lugo Jiménez](https://github.com/OLIVER26GOLDEN)**  
`Python · Telegram API · IQ Option · Threading · Madrid 🇪🇸`

[![GitHub](https://img.shields.io/badge/GitHub-@OLIVER26GOLDEN-0d1117?style=flat-square&logo=github&logoColor=00ff88)](https://github.com/OLIVER26GOLDEN)
[![Email](https://img.shields.io/badge/Email-oliveljimenes@gmail.com-0d1117?style=flat-square&logo=gmail&logoColor=00ff88)](mailto:oliveljimenes@gmail.com)

</div>
