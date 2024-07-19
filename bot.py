import asyncio
import logging
import json
import os

from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from pytz import timezone

from handlers import event_monitoring
from config import BOT_TOKEN, NOTIF_CHAT_ID, MESSAGE_IDS_FILE, MESSAGE_IDS_FILE_PATH, LOCAL_TZ


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Setup the local timezone
local_tz = timezone(LOCAL_TZ)
# Combines the path and the file name for easier configuration
full_file_path = os.path.join(MESSAGE_IDS_FILE_PATH, MESSAGE_IDS_FILE)
# Init Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Connect monitoring router
dp.include_router(event_monitoring.router)


# Reads the list of message IDs from a JSON file if exists
def load_message_ids():
    # Creates the directory if it somehow doesn't exist in container
    if not os.path.exists(MESSAGE_IDS_FILE_PATH):
        os.makedirs(MESSAGE_IDS_FILE_PATH)

    if os.path.exists(full_file_path):
        with open(full_file_path, 'r') as file:
            return json.load(file)
    return []


# Writes the list of message IDs to a JSON file
def save_message_ids(message_ids):
    with open(full_file_path, 'w') as file:
        json.dump(message_ids, file)


# Func for bot status messages every morning to make sure it's still running
async def daily_status_messages():
    # Load IDs that have been stored
    message_ids = load_message_ids()

    while True:
        now = datetime.now(local_tz)
        target_time = datetime.combine(
            now.date(), datetime.min.time()) + timedelta(hours=8)  # 8 AM
        target_time = local_tz.localize(target_time)
        if now >= target_time:
            target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)

        # Checking if there's any messages for deletion before sending new one
        if message_ids:
            for msg_id in message_ids:
                try:
                    await bot.delete_message(
                        chat_id=NOTIF_CHAT_ID,
                        message_id=msg_id
                    )
                    logging.info(
                        f"Deleted status message with ID {msg_id} at {datetime.now(local_tz)}")

                    # message_ids.remove(msg_id)
                except Exception as e:
                    logging.error(
                        f"Failed to delete status message with ID {msg_id}: {e}")

            message_ids.clear()
            save_message_ids(message_ids)

        # Sending new status message
        try:
            message = await bot.send_message(
                chat_id=NOTIF_CHAT_ID,
                # text='Status: Running!'
                text="✅ Info 💛 bot is still running!"
            )
            logging.info(
                f"Sent status message with ID {message.message_id} at {datetime.now(local_tz)}")

            # Store newest message ID
            message_ids.append(message.message_id)
            save_message_ids(message_ids)

            # Setup the delay for message deletion
            # delete_msg_delay = timedelta(hours=23, minutes=55)

            # # Schedule the message for deletion after delete_msg_delay value in seconds
            # await asyncio.sleep(delete_msg_delay.total_seconds())
            # await bot.delete_message(
            #     chat_id=NOTIF_CHAT_ID,
            #     message_id=msg_id
            # )
            # logging.info(
            #     f"Deleted status message with ID {msg_id} at {datetime.now(local_tz)}")

            # # Remove message ID from the list
            # message_ids.remove(msg_id)
            # save_message_ids(message_ids)
        except Exception as e:
            logging.error(
                f"Failed to send status message: {e}")


# Clears all old status messages and sends new startup status message
async def startup_routine():
    message_ids = load_message_ids()

    for msg_id in message_ids:
        try:
            # TN: A message can only be deleted if it was sent less than 48 hours ago
            await bot.delete_message(
                chat_id=NOTIF_CHAT_ID,
                message_id=msg_id
            )
            logging.info(
                f"Deleted old status message with ID {msg_id} at {datetime.now(local_tz)}")
        except Exception as e:
            logging.error(
                f"Failed to delete old status message with ID {msg_id}: {e}")

    # Clear the list of message IDs
    message_ids.clear()

    # Send new startup status message after restart
    try:
        message = await bot.send_message(
            chat_id=NOTIF_CHAT_ID,
            # text='Status: Restarted!'
            text="✅ Info 💛 bot has been restarted!"
        )
        logging.info(
            f"Sent startup status message with ID {message.message_id} at {datetime.now(local_tz)}")

        message_ids.append(message.message_id)
    except Exception as e:
        logging.error(f"Failed to send startup status message: {e}")

    save_message_ids(message_ids)


# Awaits startup_routine() and schedules the daily_status_messages() task
async def on_startup():
    await startup_routine()
    asyncio.create_task(daily_status_messages())


async def main():
    dp.startup.register(on_startup)

    await dp.start_polling(bot, allowed_updates=['chat_member'])


if __name__ == "__main__":
    asyncio.run(main())
