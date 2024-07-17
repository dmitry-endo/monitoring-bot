import os

from dotenv import load_dotenv


load_dotenv(override=True)

BOT_TOKEN = os.getenv('BOT_TOKEN')

# You can use whatever channel or group for notifications (even your direct chat with bot)
# Just specify its ID in .env file
# Also make sure the bot can send messages inside group chats if those are chosen
NOTIF_CHAT_ID = os.getenv('NOTIF_CHAT_ID')

# Name of the file with message IDs
MESSAGE_IDS_FILE = 'message_ids.json'

# Path to the MESSAGE_IDS_FILE
# Created via Dockerfile and Python itself for more robust approach
MESSAGE_IDS_FILE_PATH = '/var/lib/monitoring-bot'

# Local timezone
LOCAL_TZ = 'Europe/Moscow'
