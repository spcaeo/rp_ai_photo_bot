import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import asyncio
from threading import Thread

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Flask app initialization
app = Flask(__name__)

# Environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Public Render URL

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set in environment variables")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL is not set in environment variables")

# Initialize Telegram bot
application = Application.builder().token(TOKEN).build()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start command from {update.effective_user}")
    await update.message.reply_text("Hello! Bot is running with webhooks!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /help command from {update.effective_user}")
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

# Add command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Flask routes
@app.route('/')
def home():
    """Health check endpoint."""
    return "Bot is running with webhooks!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    """Handle incoming Telegram updates asynchronously."""
    try:
        incoming_data = request.get_json(force=True)
        logging.info(f"Incoming update: {incoming_data}")
        update = Update.de_json(incoming_data, application.bot)
        await application.process_update(update)
        return "OK", 200
    except Exception as e:
        logging.error(f"Error processing webhook update: {e}", exc_info=True)
        return "Internal Server Error", 500

async def setup_webhook():
    """Set up the Telegram webhook."""
    url = f"{WEBHOOK_URL}/{TOKEN}"
    try:
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(url)
        logging.info(f"Webhook set to {url}")
    except Exception as e:
        logging.error(f"Failed to set webhook: {e}", exc_info=True)

def run_flask():
    """Run Flask server."""
    port = int(os.environ.get("PORT", 3000))
    logging.info(f"Starting Flask server on port {port}")
    app.run(host="0.0.0.0", port=port)

def main():
    """Start the bot and Flask app."""
    # Start the Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Set up the webhook asynchronously
    asyncio.run(setup_webhook())

if __name__ == "__main__":
    main()
