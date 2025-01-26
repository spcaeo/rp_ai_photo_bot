# Save this to main.py
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from appwrite.client import Client
from appwrite.services.databases import Databases

load_dotenv()

client = Client()
client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
client.set_key(os.getenv('APPWRITE_API_KEY'))

databases = Databases(client)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot is running! Use /getData to fetch information.')

async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = databases.list_documents(
            database_id=os.getenv('APPWRITE_DATABASE_ID'),
            collection_id=os.getenv('APPWRITE_COLLECTION_ID')
        )
        documents = response['documents']
        message = "Here's your data:\n\n"
        for doc in documents:
            message += f"ID: {doc['$id']}\n"
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getData", get_data))
    application.run_polling()

if __name__ == '__main__':
    main()