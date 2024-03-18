import os

from dotenv import load_dotenv


load_dotenv(override=True)

BOT_TOKEN = os.getenv('BOT_TOKEN')

# You can use whatever channel or group for notifications (even your direct chat with bot)
# Just specify its ID in .env file
# Also make sure the bot can send messages inside group chats if those are chosen
NOTIF_CHAT_ID = os.getenv('NOTIF_CHAT_ID')
