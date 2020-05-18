import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from asyncio import get_event_loop

from aiohttp import web

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

    def add_app(self, app: web.Application):
        app.on_startup.append(self.on_startup)
        app.add_routes([web.post(self.config.webhook["path"], self.execute)])

    async def on_startup(self):
        await self.bot.set_webhook(self.config.get_webhook_config["host"])
        massage.rigester_handler(self.dp, self.bot, Virustotal(self.config.virus_total_token))

    async def on_shutdown(self):
        logging.warning('Shutting down..')
        await self.bot.delete_webhook()
        await self.dp.storage.close()
        await self.dp.storage.wait_closed()

        logging.warning('Bye!')

    async def execute(self, req: web.Request) -> web.Response:
        upds = [types.Update(**(await req.json()))]
        Bot.set_current(self.dp.bot)
        Dispatcher.set_current(self.dp)
        try:
            await self.dp.process_updates(upds)
        except Exception as e:
            print(e)
        finally:
            return web.Response()
