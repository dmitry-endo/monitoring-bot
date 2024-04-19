# Monitoring Bot

## Used technology
* Python 3.10;
* aiogram 3.x (Telegram Bot framework);
* python-dotenv 1.0 (Environment variables).

## Installation

- Clone the repo

- Move to the cloned directory and create `venv` (Python virtual enviroment) by:
   ```
   python3.10 -m venv venv
   ```

- Activate the venv by:
   ```
   source venv/bin/activate
   ```
   
- Install all dependencies from requirements file by:
   ```
   pip install -r requirements.txt
   ```
   
- Rename `env_example` file to `.env` and replace `BOT_TOKEN` and `NOTIF_CHAT_ID` inside the file with your own values (don't forget to save the file)

- Start the bot inside the venv by:
  ```
  python bot.py
  ```

## Usage

1. Add this bot as an Admin to the specified chat, which ID you used in `.env` file, and make sure it `has access to messages` rights or simply ignore this if you chose direct chat with bot.

2. Add this bot as an Admin to the chats you need to monitor and make sure it `has access to messages` rights.
