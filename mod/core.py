from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook

from mod import config_json


def set_up():
    config = config_json.Config()
    bot = Bot(config.get_bot_token)
    dp = Dispatcher(bot)

    start_webhook(
        dispatcher=dp,
        webhook_path=config.webhookconfig["host"],
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
