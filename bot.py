from aiohttp import web
from server.server import hello, faviconico
from aiogram.dispatcher.webhook import get_new_configured_app

import module.core

if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=module.core.dp, path=module.core.config.webhook["path"])
    app.add_routes([
        web.get('/', hello),
        web.post('/', hello)
    ])
    app.add_routes([
        web.get('/favicon.ico', faviconico),
        web.post('/favicon.ico', faviconico)
    ])
    app.on_startup.append(module.core.on_startup)
    #app.add_routes([web.post(module.core.config.webhook["path"], module.core.execute)])
    web.run_app(app, port=module.core.config.server["port"], host=module.core.config.server["host"])
