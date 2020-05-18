from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher.webhook import SendMessage

from lib.virus_total import Virustotal
from mod import text


async def echo(message: types.Message):
    return SendMessage(text.TextResponse.START)



def rigester_handler(db: Dispatcher, bot: Bot,virusttotal: Virustotal):
