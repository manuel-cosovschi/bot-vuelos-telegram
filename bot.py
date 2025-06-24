from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from scraper import scrape_rango
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Soy tu bot de vuelos baratos ✈️. Usá /alerta para buscar ofertas.")

async def alerta(update, context):
    mensaje = "🔎 Buscando vuelos baratos..."
    await update.message.reply_text(mensaje)

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
        for alerta in alertas:
            await update.message.reply_text(alerta)
    else:
        await update.message.reply_text("😕 No se encontraron vuelos baratos por ahora.")

# === AUTOEJECUCIÓN DIARIA ===
async def tarea_automatica():
    print("🔄 Ejecutando búsqueda automática...")
    class DummyUpdate:
        def __init__(self):
            self.message = type('msg', (object,), {'reply_text': print})

    await alerta(DummyUpdate(), None)

scheduler = BackgroundScheduler()
scheduler.add_job(lambda: asyncio.run(tarea_automatica()), 'interval', hours=24)
scheduler.start()

# Iniciar bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("alerta", alerta))
print("🤖 Bot corriendo...")
app.run_polling()
