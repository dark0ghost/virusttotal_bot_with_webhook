import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from asyncio import get_event_loop

from aiohttp import web

from lib.virus_total import Virustotal
from mode import config_json
from mode.handler import massage


logging.basicConfig(level=logging.INFO)
loop = get_event_loop()
config = config_json.Config(loop)

#bot = Bot(token=config.get_bot_token)
#dp = Dispatcher(bot)


async def on_startup(web_app: web.Application):
    await bot.set_webhook(config.get_webhook_config["host"])
    massage.rigester_handler(dp, bot, Virustotal(config.virus_total_token))


async def execute(req: web.Request) -> web.Response:
    upds = [types.Update(**(await req.json()))]
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    try:
        await dp.process_updates(upds)
    except Exception as e:
        print(e)
    finally:
        return web.Response()
