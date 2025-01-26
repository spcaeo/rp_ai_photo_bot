import os
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your AI Photo Bot. Use /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
"""
    await update.message.reply_text(help_text)

def main():
    app = Application.builder().token("7983659890:AAGBHW3dz0yjpYvnoxrxtlODxPeOFtO4m18").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    print("Starting bot...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()