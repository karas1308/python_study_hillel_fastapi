#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from common import create_short_url, get_long_url, get_user_redirects, get_user_urls
from config import TELEBOT_TOKEN

bot = AsyncTeleBot(TELEBOT_TOKEN)

commands = {
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',
    'create': 'Creates short url',
    'get_all': 'Shows all users urls',
    'get_redirects': 'Shows users redirects statistics'
}


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(commands=['create'])
async def create_short(message: Message):
    long_url = message.text.replace("/create", "").strip()
    if long_url:
        user_id = message.from_user.id
        short_url = await create_short_url(long_url, user_id=user_id)
        await bot.reply_to(message, short_url)
    else:
        await bot.reply_to(message, "Provide url")


@bot.message_handler(commands=['get_all'])
async def get_all_user_urls(message: Message):
    user_id = message.from_user.id
    user_urls_data = await get_user_urls(user_id=user_id)
    result = [f"{data['long_url']} -> {data['short_url']}" for data in user_urls_data]
    await bot.send_message(message.chat.id,
                           "\r\n".join(result) if result else f"User {user_id} has not created any urls")


@bot.message_handler(commands=['get_redirects'])
async def get_all_user_urls(message: Message):
    user_id = message.from_user.id
    redirects = await get_user_redirects(user_id)
    await bot.send_message(message.chat.id, redirects)


# help page
@bot.message_handler(commands=['help'])
async def command_help(message):
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    await bot.send_message(message.chat.id, help_text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message: Message):
    long_url = await get_long_url(message.text)
    await bot.reply_to(message, long_url)


import asyncio

asyncio.run(bot.polling())
