import asyncio
from datetime import datetime, timedelta
import logging

from aiogram import Bot, Dispatcher
import pytz

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
async def send_daily_status_msg():
    tz = pytz.timezone("Europe/Moscow")
    while True:
        now = datetime.now(tz)
        target_time = datetime.combine(
            now.date(), datetime.min.time()) + timedelta(hours=8)  # 8 AM
        target_time = tz.localize(target_time)
        if now >= target_time:
            target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)

        try:
            await bot.send_message(
                chat_id=NOTIF_CHAT_ID,
                text=f"Hey, I'm still running successfully!\nNo need to worry about me."
            )
            logging.info(f"Sent message at {datetime.now(tz)}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")


async def on_startup():
    asyncio.create_task(send_daily_status_msg())


async def main():
    dp.startup.register(on_startup)

    await dp.start_polling(bot, allowed_updates=['chat_member'])


if __name__ == "__main__":
    asyncio.run(main())
