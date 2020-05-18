from aiohttp import web
import aiofiles


async def hello(request):
    return web.Response(text="Hello, world")


async def faviconico(request):
    async with aiofiles.open("server/ico.png", "rb") as f:
        return web.Response(body=await f.read())
