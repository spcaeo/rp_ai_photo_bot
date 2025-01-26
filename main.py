import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from threading import Thread

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

async def run_bot():
    # Initialize Telegram bot
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_TOKEN not set in environment variables")
    
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Start the bot
    await application.initialize()
    await application.start()
    print("Telegram bot is running!")
    await application.run_polling(drop_pending_updates=True)

def run_flask():
    # Run Flask app for Render health check
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Run Flask and Telegram bot concurrently
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    asyncio.run(run_bot())
