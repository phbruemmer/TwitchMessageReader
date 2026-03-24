import time

from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch

import threading
import asyncio
import cfg
import check


# constants
APP_ID = cfg.CLIENT_ID
APP_SECRET = cfg.CLIENT_SECRET
TARGET_CHANNEL = cfg.TARGET
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MANAGE_BROADCAST]


# Listen for chat messages
async def on_message(msg: ChatMessage):
    print(f'{msg.user.display_name}: {msg.text}')
    check.extract(msg.text)


async def on_ready(ready_event: EventData):
    await ready_event.chat.join_room(TARGET_CHANNEL)
    print("Connected.")

    # Other tasks
    asyncio.create_task(periodic_message(ready_event.chat))


async def periodic_message(chat: Chat):
    while True:
        await asyncio.sleep(8 * 60)
        random_num = check.check_numbers()
        print(f"[info] checking number {random_num}.")
        await chat.send_message(TARGET_CHANNEL, f"!safe {random_num}")


async def run_bot():
    bot = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(bot, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await bot.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(bot)

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)

    chat.start()

    try:
        input('Press ENTER to stop\n')
    finally:
        chat.stop()
        await bot.close()


asyncio.run(run_bot())
