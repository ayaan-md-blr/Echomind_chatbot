README.txt

Project: Telegram AI Bot

Description:
This project is a Telegram bot that uses AI to interact with users. It integrates with MongoDB for data storage and uses the Gemini model for generating responses.

Prerequisites:
1. Python 3.8 or higher
2. MongoDB 4.4 or higher
3. Telegram Bot API
4. Gemini AI API

Setup Instructions:

1. Clone the repository:git clone https://github.com/your-repo/telegram_aibot.git cd telegram_aibot

2. Create and activate a virtual environment:
python -m venv venv venv\Scripts\activate # On Windows source venv/bin/activate # On macOS/Linux

3. Install the required packages:
pip install -r requirements.txt

4. Set up environment variables:
Create a `.env` file in the project root directory and add the following:
TELEGRAM_BOT_TOKEN=your_telegram_bot_token TELEGRAM_BOT_USERNAME=your_telegram_bot_username GEMINI_API_KEY=your_gemini_api_key


5. Configure MongoDB:
Ensure MongoDB is running and accessible. Update the MongoDB connection string in `Mongoclient.py` if necessary.

6. Run the bot:
python telegram_aibot.py


File Descriptions:

1. `telegram_aibot.py`:
- Main file for the Telegram bot.
- Handles commands and messages from users.
- Integrates with MongoDB and Gemini AI.

2. `Mongoclient.py`:
- Contains functions for interacting with MongoDB.
- Functions include adding chat history and file details.

3. `gemini.py`:
- Contains functions for interacting with the Gemini AI model.
- Functions include generating responses and analyzing files.

Dependencies:
- python-telegram-bot==13.7
- pymongo==3.11.4
- requests==2.25.1
- genai==1.0.0

Logging:
- Logging is configured to log at the INFO level.
- Logs are printed to the console.

Contact:
For any issues or questions, please contact [your-email@example.com].
