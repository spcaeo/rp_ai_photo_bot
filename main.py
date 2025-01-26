import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import sys

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your AI Photo Bot. Use /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show this help")

async def main():
    token = "7983659890:AAGBHW3dz0yjpYvnoxrxtlODxPeOFtO4m18"
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    print("Starting bot...")
    await app.initialize()
    await app.start()
    await app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
        sys.exit(0)