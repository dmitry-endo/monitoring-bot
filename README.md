# Monitoring Bot

## Used technology
* Python 3.10;
* aiogram 3.x (Telegram Bot framework);
* python-dotenv 1.0 (Environment variables).

## Installation

1. Clone the repo;

2. Move to the cloned directory and create `venv` (Python virtual enviroment) `python3.10 -m venv venv`;

3. Activate the venv `source venv/bin/activate` and install all dependencies from requirements file `pip install -r requirements.txt`;

4. Rename `env_example` file to `.env` and replace `BOT_TOKEN` and `NOTIF_CHAT_ID` with your own values (don't forget to save the file);

5. Start the bot inside the venv by: `python bot.py`.
