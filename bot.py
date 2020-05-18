import asyncio

from aiohttp import web

import mod.core

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = web.Application()
    Bot = mod.core.BotStart(loop)
    loop.run_until_complete(Bot.on_startup())
    Bot.add_app(app=app)
    web.run_app(app, port=Bot.config.server["port"], host=Bot.config.server["host"])

