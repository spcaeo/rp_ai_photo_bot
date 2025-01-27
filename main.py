import os
import logging
from flask import Flask, request
from telegram import Update, BotCommand, BotCommandScopeAllGroupChats
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import asyncio
from threading import Thread

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Flask app initialization
app = Flask(__name__)

# Environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Public Render URL
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID"))  # Fetch Group ID from .env

if not TOKEN or not WEBHOOK_URL or not ALLOWED_GROUP_ID:
    raise ValueError("Required environment variables (TELEGRAM_TOKEN, WEBHOOK_URL, ALLOWED_GROUP_ID) are missing")

# Initialize Telegram bot
application = Application.builder().token(TOKEN).build()


# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler."""
    logging.info(f"Received /start command from user {update.effective_user} in chat {update.effective_chat}")
    if update.effective_chat.type == "private":
        logging.warning(f"Unauthorized private chat attempt from user {update.effective_user.id}")
        await update.message.reply_text("Access denied. This bot is restricted to a specific group.")
        return
    if update.effective_chat.id != ALLOWED_GROUP_ID:
        logging.warning(f"Unauthorized access attempt from chat ID: {update.effective_chat.id}")
        await update.message.reply_text("Access denied. This bot is restricted to a specific group.")
        return
    await update.message.reply_text("Hello! Bot is running with webhooks!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler."""
    logging.info(f"Received /help command from user {update.effective_user} in chat {update.effective_chat}")
    if update.effective_chat.type == "private":
        logging.warning(f"Unauthorized private chat attempt from user {update.effective_user.id}")
        await update.message.reply_text("Access denied. This bot is restricted to a specific group.")
        return
    if update.effective_chat.id != ALLOWED_GROUP_ID:
        logging.warning(f"Unauthorized access attempt from chat ID: {update.effective_chat.id}")
        await update.message.reply_text("Access denied. This bot is restricted to a specific group.")
        return
    await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Show help\n/about - Learn about the bot.\n/menu - Access the main menu")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About command handler."""
    logging.info(f"Received /about command from user {update.effective_user} in chat {update.effective_chat}")
    if update.effective_chat.type == "private":
        logging.warning(f"Unauthorized private chat attempt from user {update.effective_user.id}")
        await update.message.reply_text("Access denied. This bot is restricted to a specific group.")
        return
    if update.effective_chat.id != ALLOWED_GROUP_ID:
        logging.warning(f"Unauthorized access attempt from chat ID: {update.effective_chat.id}")
        await update.message.reply_text("Access denied. This bot is restricted to a specific group.")
        return
    await update.message.reply_text("This bot demonstrates private group use and webhooks integration with Telegram.")

# Add command handlers to the bot
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("about", about_command))

@app.route('/')
def home():
    """Health check endpoint."""
    logging.info("Health check endpoint accessed.")
    return "Bot is running with webhooks!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    """Handle incoming Telegram updates asynchronously."""
    try:
        incoming_data = request.get_json(force=True)
        logging.info(f"Incoming update: {incoming_data}")

        # Parse the update
        update = Update.de_json(incoming_data, application.bot)

        # Restrict private chat and unauthorized group access
        if update.effective_chat.type == "private" or update.effective_chat.id != ALLOWED_GROUP_ID:
            logging.warning(f"Unauthorized access from chat ID: {update.effective_chat.id}")
            if update.message:
                await update.message.reply_text("Access denied. This bot is restricted to a specific group.")
            return "Access Denied", 403

        # Process the update
        await application.process_update(update)

        return "OK", 200
    except Exception as e:
        logging.error(f"Error processing webhook update: {e}", exc_info=True)
        return {"error": str(e)}, 500

async def setup_bot_commands():
    """Set up the bot's persistent menu for group chats only."""
    commands = [
        BotCommand("start", "Start interacting with the bot"),
        BotCommand("help", "Get help information"),
        BotCommand("about", "Learn more about the bot"),
    ]
    try:
        await application.bot.set_my_commands(commands, scope=BotCommandScopeAllGroupChats())
        logging.info("Bot commands successfully registered for group chats.")
    except Exception as e:
        logging.error(f"Failed to register bot commands: {e}", exc_info=True)

async def setup_webhook():
    """Set up Telegram webhook and bot commands."""
    url = f"{WEBHOOK_URL}/{TOKEN}"
    try:
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(url)
        await setup_bot_commands()
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
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Use the current event loop for bot operations
    asyncio.run(setup_webhook())

if __name__ == "__main__":
    main()
