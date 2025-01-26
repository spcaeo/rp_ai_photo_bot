import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot started!')

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).base_url("https://api.telegram.org/bot").build()
    application.add_handler(CommandHandler("start", start))
    print("Bot starting...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()