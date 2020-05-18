from aiohttp import web

import mod.core

if __name__ == "__main__":
    app = web.Application()
    Bot = mod.core.BotStart()
    Bot.on_startup()
    Bot.add_app(app=app)
    web.run_app(app, port=Bot.config.server["port"], host=Bot.config.server["host"])

