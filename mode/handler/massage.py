from typing import Optional

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher.webhook import SendMessage

from lib.virus_total import Virustotal
from mode import text

totaclchecker = None


async def start(message: types.Message):
    return SendMessage(text.TextResponse.START)


async def check_file(message: types.Message):
    totaclchecker


def rigester_handler(db: Dispatcher, bot: Bot, virustotal: Virustotal):
    totaclchecker = virustotal
    db.register_message_handler(callback=start, commands=["start"])
    #db.register_message_handler(check_file, content_types="")
