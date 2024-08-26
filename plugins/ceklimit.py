# © rendydev A.k.A @xtdev

import asyncio
import os

from pyrogram import Client
from pyrogram import Client as ren
from pyrogram import *
from pyrogram import filters
from pyrogram.raw import *
from pyrogram.types import *
from pyrogram.types import Message

from utils.handler import *
from utils.misc import plugins_help, prefix

@Client.on_message(filters.command(["limit", "lmt"], prefix) & filters.me)

async def spamban(client: Client, message: Message):
    await client.unblock_user("SpamBot")
    response = await client.invoke(
        raw.functions.messages.StartBot(
            bot=await client.resolve_peer("SpamBot"),
            peer=await client.resolve_peer("SpamBot"),
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    wait_msg = await message.reply_text("<i>Processing . . .</i>")
    await asyncio.sleep(1)
    spambot_msg = response.updates[1].message.id + 1
    status = await client.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await wait_msg.edit_text(f"<blockquote>~ {status.text}</blockquote>")

plugins_help["admintool"] = {
  "limit [prefix]": "get ur limit information",
  "lmt [prefix]": "get ur limit information"
}