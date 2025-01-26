import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is running!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

def main():
    application = Application.builder().token("7983659890:AAGBHW3dz0yjpYvnoxrxtlODxPeOFtO4m18").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    print("Starting bot...")
    main()