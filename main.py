import os
import asyncio
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from threading import Thread

# Initialize logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start command from {update.effective_user}")
    await update.message.reply_text("Hello! Bot is running!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /help command from {update.effective_user}")
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

async def run_bot():
    try:
        # Load Telegram token
        token = os.getenv('TELEGRAM_TOKEN')
        if not token:
            raise ValueError("TELEGRAM_TOKEN not set in environment variables")

        # Initialize Telegram bot application
        logging.info("Initializing Telegram bot...")
        application = Application.builder().token(token).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))

        # Start the bot
        logging.info("Starting Telegram bot polling...")
        await application.initialize()
        await application.start()
        logging.info("Telegram bot is running!")
        await application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logging.error(f"Error in bot polling: {e}")
    finally:
        await application.stop()

def run_flask():
    try:
        # Run Flask app for Render
        port = int(os.environ.get("PORT", 3000))
        logging.info(f"Starting Flask server on port {port}")
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        logging.error(f"Error in Flask server: {e}")

if __name__ == "__main__":
    # Run Flask and Telegram bot concurrently
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the Telegram bot
    asyncio.run(run_bot())
