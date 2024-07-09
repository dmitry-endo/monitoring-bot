import asyncio
import logging
import json
import os

from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from pytz import timezone

from handlers import event_monitoring
from config import BOT_TOKEN, NOTIF_CHAT_ID


# Corresponding path to the file is created via Dockerfile
MESSAGE_IDS_FILE = '/var/lib/monitoring-bot/message_ids.json'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Init Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Connect monitoring router
dp.include_router(event_monitoring.router)


# Reads the list of message IDs from a JSON file if exists
def load_message_ids():
    if os.path.exists(MESSAGE_IDS_FILE):
        with open(MESSAGE_IDS_FILE, 'r') as file:
            return json.load(file)
    return []


# Writes the list of message IDs to a JSON file
def save_message_ids(message_ids):
    with open(MESSAGE_IDS_FILE, 'w') as file:
        json.dump(message_ids, file)


# Func for bot status messages every morning to make sure it's still running
async def daily_status_messages():
    # load ids that have been stored
    message_ids = load_message_ids()
    # setup the local timezone
    local_tz = timezone("Europe/Moscow")

    while True:
        now = datetime.now(local_tz)
        target_time = datetime.combine(
            now.date(), datetime.min.time()) + timedelta(hours=8)  # 8 AM
        target_time = local_tz.localize(target_time)
        if now >= target_time:
            target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)

        try:
            # Clear old status messages before sending the new one
            await delete_old_messages()

            message = await bot.send_message(
                chat_id=NOTIF_CHAT_ID,
                text="Status: OK!"
            )
            logging.info(f"Sent message at {datetime.now(local_tz)}")

            # Message ID var
            msg_id = message.message_id

            # Store newest message ID
            message_ids.append(msg_id)
            save_message_ids(message_ids)

            # Schedule the message for deletion after 24 hours
            await asyncio.sleep(86400)  # 24 hours in seconds
            await bot.delete_message(
                chat_id=NOTIF_CHAT_ID,
                message_id=msg_id
            )
            logging.info(f"Deleted message at {datetime.now(local_tz)}")

            # Remove message ID from the list
            message_ids.remove(msg_id)
            save_message_ids(message_ids)
        except Exception as e:
            logging.error(f"Failed to send or delete message: {e}")


async def delete_old_messages():
    message_ids = load_message_ids()
    for msg_id in message_ids:
        try:
            await bot.delete_message(
                chat_id=NOTIF_CHAT_ID,
                message_id=msg_id
            )
            logging.info(f"Deleted message with ID {msg_id}")
        except Exception as e:
            logging.error(f"Failed to delete message with ID {msg_id}: {e}")

    # Clear the list of message IDs
    message_ids.clear()
    save_message_ids(message_ids)


# Deletes all stored messages and starts the daily_status_messages() task
async def on_startup():
    # await delete_old_messages()
    asyncio.create_task(daily_status_messages())


async def main():
    dp.startup.register(on_startup)

    await dp.start_polling(bot, allowed_updates=['chat_member'])


if __name__ == "__main__":
    asyncio.run(main())
