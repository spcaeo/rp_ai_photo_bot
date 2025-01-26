import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
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

# Check if required environment variables are set
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

# Add command handlers to the bot
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Flask routes
@app.route('/')
def home():
    """Health check endpoint."""
    return "Bot is running with webhooks!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Handle incoming Telegram updates synchronously."""
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        # Use asyncio.run to execute the async process_update method
        asyncio.run(application.process_update(update))
        return "OK", 200
    except Exception as e:
        logging.error(f"Error processing webhook update: {e}")
        return "Internal Server Error", 500

async def setup_webhook():
    """Set up Telegram webhook asynchronously."""
    url = f"{WEBHOOK_URL}/{TOKEN}"
    try:
        await application.bot.set_webhook(url)
        logging.info(f"Webhook set to {url}")
    except Exception as e:
        logging.error(f"Failed to set webhook: {e}")

def run_flask():
    """Run Flask server."""
    port = int(os.environ.get("PORT", 3000))
    logging.info(f"Starting Flask server on port {port}")
    app.run(host="0.0.0.0", port=port)

def main():
    """Run Flask and Telegram bot."""
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Use asyncio to set up webhook
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_webhook())

if __name__ == "__main__":
    main()
