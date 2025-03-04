import os
import asyncio
import threading
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from flask_app.services.message_service import responder, start, callback
from flask_app.services.audio_service import handle_audio
from flask_app.services.location_service import receber_localizacao
from flask_app.services.image_service import handle_image
from flask_app.services.arquivo_service import receber_arquivo

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

application = Application.builder().token(TOKEN).build()

# Configuração dos handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
application.add_handler(CallbackQueryHandler(callback))
application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
application.add_handler(MessageHandler(filters.LOCATION, receber_localizacao))
application.add_handler(MessageHandler(filters.PHOTO, handle_image))
application.add_handler(MessageHandler(filters.Document.ALL, receber_arquivo))

async def initialize_bot():
    """Inicializa o Application uma única vez (sem polling, pois usaremos webhook)."""
    await application.initialize()

global_loop = asyncio.new_event_loop()

def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

global_loop.run_until_complete(initialize_bot())

threading.Thread(target=run_loop, args=(global_loop,), daemon=True).start()

def get_loop():
    """Retorna o loop global para uso em outros módulos."""
    return global_loop

async def processar_update(update: Update):
    """Processa a atualização recebida via webhook."""
    await application.process_update(update)
