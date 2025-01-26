import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Telegram bot
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set your public Render URL here

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start command from {update.effective_user}")
    await update.message.reply_text("Hello! Bot is running with webhooks!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /help command from {update.effective_user}")
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

# Initialize Telegram Application
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

@app.route('/')
def home():
    return "Bot is running with webhooks!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    """Handle incoming Telegram updates."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK", 200

def setup_webhook():
    """Set up Telegram webhook."""
    url = f"{WEBHOOK_URL}/{TOKEN}"
    application.bot.set_webhook(url)
    logging.info(f"Webhook set to {url}")

if __name__ == "__main__":
    # Set the webhook
    setup_webhook()

    # Run Flask server
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
