from aiogram import types
from aiogram.dispatcher.webhook import SendMessage


async def echo(message: types.Message):
    return SendMessage()
