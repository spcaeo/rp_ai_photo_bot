import os
import logging
import asyncio
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

async def bot_runner():
    """Run the Telegram bot."""
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

def run_bot():
    """Run the bot within the existing event loop."""
    loop = asyncio.get_event_loop()
    loop.create_task(bot_runner())  # Schedule the bot_runner coroutine

def run_flask():
    """Run the Flask server."""
    port = int(os.environ.get("PORT", 3000))
    logging.info(f"Starting Flask server on port {port}")
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Run Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the Telegram bot using the existing event loop
    run_bot()

    # Keep the main thread running
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")
