# Monitoring Bot
<a href="https://hub.docker.com/repository/docker/dmitryendo/monitoring-bot/general">Docker Hub Image</a> 

## Used technology
* Python 3.10;
* aiogram 3.x (Telegram Bot framework);
* python-dotenv 1.0 (environment variables);
* Docker (containerization).

## Installation

### Locally

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

### Docker

- Clone the image from Docker Hub by:
  ```
  docker pull dmitryendo/monitoring-bot
  ```
  
- Create your `.env` file with `BOT_TOKEN` and `NOTIF_CHAT_ID`
  
- Start the by:
  ```
  docker run --env-file /path/to/your/file/.env -d -t monitoring-bot
  ```

## Usage

1. Add bot as an Admin to the specified chat for notifications, which ID you used in `.env` file, and make sure it `has access to messages` rights or simply ignore this if you chose direct chat with bot.

2. Add bot as an Admin to the chats you need to monitor and make sure it `has access to messages` rights.
