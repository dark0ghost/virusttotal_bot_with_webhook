import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from asyncio import get_event_loop

from lib.virus_total import Virustotal
from mod import config_json
from mod.handler import massage


class BotStart:
    def __init__(self):
        self.loop = get_event_loop()
        self.config = config_json.Config(loop=self.loop)
        self.bot = Bot(self.config.get_bot_token)
        self.dp = Dispatcher(self.bot)
        logging.basicConfig(level=logging.INFO)
        self.dp.middleware.setup(LoggingMiddleware())
        massage.rigester_handler(self.dp, self.bot, Virustotal(self.config.virus_total_token))

    def start(self, *args, **kwargs):
        start_webhook(
            dispatcher=self.dp,
            webhook_path=self.config.get_webhook_config["host"],
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
            skip_updates=True,
            host=self.config.get_webhook_config["host"],
            port=self.config.get_server["port"],
        )

    async def on_startup(self):
        await self.bot.set_webhook(self.config.get_webhook_config["host"])

    async def on_shutdown(self):
        logging.warning('Shutting down..')
        await self.bot.delete_webhook()
        await self.dp.storage.close()
        await self.dp.storage.wait_closed()

        logging.warning('Bye!')
