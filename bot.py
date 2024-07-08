import asyncio
import logging
import json
import os

from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from pytz import timezone

from handlers import event_monitoring
from config import BOT_TOKEN, NOTIF_CHAT_ID


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


# Func for bot status messages every morning to make sure it's still running
async def daily_status_messages():
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
            message = await bot.send_message(
                chat_id=NOTIF_CHAT_ID,
                text="Status: OK!"
            )
            logging.info(f"Sent message at {datetime.now(local_tz)}")

            # Schedule the message for deletion after 24 hours
            await asyncio.sleep(86400)  # 24 hours in seconds
            await bot.delete_message(
                chat_id=NOTIF_CHAT_ID,
                message_id=message.message_id
            )
            logging.info(f"Deleted message at {datetime.now(local_tz)}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")


async def on_startup():
    asyncio.create_task(daily_status_messages())


async def main():
    dp.startup.register(on_startup)

    await dp.start_polling(bot, allowed_updates=['chat_member'])


if __name__ == "__main__":
    asyncio.run(main())
