import asyncio
import logging
import os
from asyncio import get_event_loop

import aiofiles
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.types import ContentTypes
from aiohttp import web

from lib.virus_total import Virustotal
from module import config_json, text, buttons

logging.basicConfig(level=logging.INFO)
loop = get_event_loop()
config = config_json.Config(loop)
print(config.webook_url)
bot = Bot(token=config.get_bot_token)
dp = Dispatcher(bot)
virustotal = Virustotal(config.get_virus_total_token)
texts = text.TextResponse()
button = buttons.Button()


async def on_startup(web_app: web.Application):
    await virustotal.new_session()
    await bot.delete_webhook()
    await bot.set_webhook(config.get_webhook_url)


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


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    return await bot.send_message(message.chat.id, text=texts.START)


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def check_file(message: types.Message):
    try:
        file_b = await bot.download_file_by_id(file_id=message.document.file_id)
        async with aiofiles.open(f"file/{message.document.file_name}", "wb") as file:
            await file.write(file_b.read())
            response = await virustotal.file_scan(file=file, name_file=message.document.file_name)
            await message.answer(f"""scan_id  - `{response['scan_id']}`""",
                                 parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=button.link_buttons(link=[response["permalink"]],
                                                                  text=[message.document.file_name]))
            os.remove(f"file/{message.document.file_name}")
    except Exception as e:
        await message.reply(f"error: {e}")


@dp.message_handler(content_types=ContentTypes.TEXT)
async def check(message: types.Message):
    arg = message.text
    print(arg)
    response = await virustotal.file_report(arg)
    print(response['response_code'] == -2)
    print(response)
    try:
        await bot.send_message(chat_id=message.chat.id, text=f"{response['positives']} is {response['total']}")
    except:
        await message.reply("wait or scan_id not waled")
