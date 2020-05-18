import asyncio

from aiohttp import web

import mod.core
from server.server import hello,faviconico

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = web.Application()
    app.add_routes([web.get('/', hello)])
    app.add_routes([web.get('/favicon.ico', faviconico)])
    Bot = mod.core.BotStart(loop)
    loop.run_until_complete(Bot.on_startup())
    Bot.add_app(app=app)
    web.run_app(app, port=Bot.config.server["port"], host=Bot.config.server["host"])
    web.run_app(app, port=5051, host="localhost")

