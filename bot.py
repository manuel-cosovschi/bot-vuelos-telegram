from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler
from scraper import scrape_rango
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# === Configurar dispatcher para manejar comandos ===
dispatcher = Dispatcher(bot, None, use_context=True)

# === Funciones de comando ===
def start(update, context):
    update.message.reply_text("¡Hola! Soy tu bot de vuelos baratos ✈️. Usá /alerta para buscar ofertas.")

def alerta(update, context):
    mensaje = "🔎 Buscando vuelos baratos..."
    update.message.reply_text(mensaje)

    alertas = []

    # JAPÓN: abril/mayo 2026, 21 días
    resultados_japon = scrape_rango("eze", "jp", "2026-04-01", "2026-05-15", 21, 1000)
    for r in resultados_japon:
        alertas.append(f"🇯🇵 JAPÓN\n{r['ida']} → {r['vuelta']}\n💸 ${r['precio']}\n🔗 {r['url']}")

    # ORLANDO: agosto/septiembre 2026, 14 días
    resultados_usa = scrape_rango("eze", "orl", "2026-08-01", "2026-09-20", 14, 300)
    for r in resultados_usa:
        alertas.append(f"🇺🇸 ORLANDO\n{r['ida']} → {r['vuelta']}\n💸 ${r['precio']}\n🔗 {r['url']}")

    if alertas:
        for a in alertas:
            update.message.reply_text(a)
    else:
        update.message.reply_text("😕 No se encontraron vuelos baratos por ahora.")

# === Agregar handlers ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("alerta", alerta))

# === Webhook endpoint ===
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Bot activo!"

# === Ejecutar automáticamente todos los días ===
def tarea_automatica():
    print("🔄 Ejecutando búsqueda automática...")
    class DummyMessage:
        def reply_text(self, msg):
            print("Auto-alerta:", msg)

    dummy = type('dummy', (), {"message": DummyMessage()})()
    alerta(dummy, None)

scheduler = BackgroundScheduler()
scheduler.add_job(tarea_automatica, 'interval', hours=24)
scheduler.start()

# === Iniciar servidor ===
if __name__ == "__main__":
    import requests
    # Configurar el webhook si no está hecho
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TOKEN}"
    r = requests.get(url, params={"url": webhook_url})
    print("Webhook set:", r.json())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

