#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from common import create_short_url, get_long_url, get_user_redirects, get_user_urls

bot = AsyncTeleBot('6486089059:AAGfjUSWVwqLRWTglf7A5czFP2W3YQwHhQw')


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(commands=['create'])
async def create_short(message: Message):
    long_url = message.text.replace("/create ", "")
    user_id = message.from_user.id
    short_url = await create_short_url(long_url, user_id=user_id)
    await bot.reply_to(message, short_url)


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


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message: Message):
    long_url = await get_long_url(message.text)
    await bot.reply_to(message, long_url)


import asyncio

asyncio.run(bot.polling())