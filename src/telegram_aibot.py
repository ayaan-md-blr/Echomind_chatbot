from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import logging
import Mongoclient
import gemini
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: Final = os.getenv('TELEGRAM_BOT_USERNAME')

#processes the start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("start : start_command function.")
    try:
        await update.message.reply_text("Hello! This is the Echo Mind bot. Thanks for chatting with me!")
        user = Mongoclient.find_user(update.message.chat.id)
        if user is None:
            await update.message.reply_text("Please register")
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text("An error occurred while processing the command. Please try again.")
     
#processes the register command     
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("start : register_command function.")
    try:
        user = Mongoclient.find_user(update.message.chat.id)
        if user is None:
            user_data = {
                "first_name": update.message.chat.first_name,
                "chat_id": update.message.chat.id
            }
            try:
                Mongoclient.add_user(user_data)
                await update.message.reply_text("You have been registered successfully!")
            except Exception as e:
                logger.error(f"Error inserting into MongoDB: {e}")
                await update.message.reply_text("An error occurred while registering. Please try again.")
        else:
            await update.message.reply_text("User already registered")
    except Exception as e:
        logger.error(f"Error in register_command: {e}")
        await update.message.reply_text("An error occurred while processing the command. Please try again.")

#processes the message from chatbot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("start : handle_message function.")
    try:
        user_input: str = update.message.text
        logger.debug(f"I have received this message: {user_input}")
        response = gemini.generateResponse(user_input)
        Mongoclient.add_chat_history(update.message.chat.id, user_input, response)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await update.message.reply_text("An error occurred while processing the message. Please try again.")

#processes the file from chatbot
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("start : handle_file function.")
    try:    
        
        if update.message.photo:
            # Get the file ID of the highest resolution photo
            file_id = update.message.photo[-1].file_id

            # Get file info using Telegram's getFile API
            file_info = await context.bot.get_file(file_id)
            file_path = file_info.file_path  # URL to download the file

            # Define a local path to save the image
            local_filename = f"downloaded_image.jpg"

            # Download the file
            response = requests.get(file_path)
            if response.status_code == 200:
                with open(local_filename, 'wb') as f:
                    f.write(response.content)
                logger.debug("Photo downloaded successfully!")
                image_description = gemini.analyse_file("downloaded_image.jpg")
                await update.message.reply_text(image_description[0:500])
                Mongoclient.add_file_details(file_path, image_description[0:500])
            else:
                logger.debug("Failed to download the photo.")
                await update.message.reply_text("Sorry unable to analyze the file")
    except Exception as e:
        logger.error(f"Error in handle_file: {e}")
        await update.message.reply_text("An error occurred while processing the file. Please try again.")
        
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('register', register_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, handle_file))

    print('Currently Polling...')
    app.run_polling(poll_interval=3)
