import asyncio

from aiohttp import web

import mode.core
from server.server import hello, faviconico

if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get('/', hello),
        web.post('/', hello)
    ])
    app.add_routes([
        web.get('/favicon.ico', faviconico),
        web.post('/favicon.ico', faviconico)
    ])
    app.on_startup.append(mode.core.on_startup)
    app.add_routes([web.post(mode.core.config.webhook["path"], mode.core.execute)])
    web.run_app(app, port=mode.core.config.server["port"], host=mode.core.config.server["host"])
