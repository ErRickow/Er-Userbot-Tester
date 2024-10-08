#  Moon-Userbot - telegram userbot
#  Copyright (C) 2020-present Moon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio

import requests
from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import plugins_help, prefix
from utils.anu import format_exc


def get_neko_media(query):
    return requests.get(f"https://nekos.life/api/v2/img/{query}").json()["url"]


@Client.on_message(filters.command("neko", prefix) & filters.me)
async def neko(_, message: Message):
    if len(message.command) == 1:
        await message.reply(
            "<b>Neko type isn't provided\n"
            f"lu bisa dapatkan neko yang tersedia, contoh; <code>{prefix}neko_types</code></b>"
        )

    query = message.command[1]
    await message.reply("<b>Loading...</b>")
    try:
        await message.reply(f"{get_neko_media(query)}", disable_web_page_preview=False)
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command(["nekotypes", "neko_types"], prefix) & filters.me)
async def neko_types_func(_, message: Message):
    neko_types = """hug kiss tickle lewd neko pat lizard 8ball cat chat fact smug woof gasm goose cuddle avatar slap gecg feed fox_girl meow wallpaper spank waifu ngif name owoify spoiler why"""
    await message.edit(" ".join(f"<code>{n}</code>" for n in neko_types.split()))


@Client.on_message(filters.command(["nekospam", "neko_spam"], prefix) & filters.me)
async def neko_spam(client: Client, message: Message):
    query = message.command[1]
    amount = int(message.command[2])

    await message.delete()

    for _ in range(amount):
        if message.reply_to_message:
            await message.reply_to_message.reply(get_neko_media(query))
        else:
            await client.send_message(message.chat.id, get_neko_media(query))
        await asyncio.sleep(0.1)


plugins_help["neko"] = {
    "neko [type]*": "Get neko media",
    "neko_types": "Available neko types",
    "neko_spam [type]* [amount]*": "Start spam with neko media",
}
