import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

async def run_bot():
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    await application.initialize()
    await application.start()
    await application.run_polling(drop_pending_updates=True)

def run_flask():
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(run_bot())