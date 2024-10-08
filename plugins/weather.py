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

# rewrote the module from @ Fl1yd
from io import BytesIO

import requests
from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.db import db
from utils.misc import plugins_help, prefix
from utils.anu import format_exc


@Client.on_message(filters.command(["cuaca", "w"], prefix) & filters.me)
async def weather(client: Client, message: Message):
    if len(message.command) == 1:
        city = db.get("custom.weather", "city", "Semarang")
    else:
        city = message.command[1]

    await message.edit(f"<blockquote>Sedang memproses kota {city}...</blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        text_resp = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
        text_resp.raise_for_status()
        caption = f"<blockquote>City: {text_resp.text}</blockquote>"

        pic_resp = requests.get(f"http://wttr.in/{city}_2&lang=id.png")
        pic_resp.raise_for_status()
        pic = BytesIO(pic_resp.content)
        pic.name = f"{city}.png"

        await client.send_document(
            chat_id=message.chat.id, document=pic, caption=caption
        )
        await message.delete()
    except Exception as e:
        await message.reply(format_exc(e), parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.command(["set_weather_city", "ckota"], prefix) & filters.me)
async def set_weather_city(_, message: Message):
    if len(message.command) == 1:
        return await message.edit("<b>Masukkan Nama kota lo</b>", parse_mode=enums.ParseMode.HTML)

    db.set("custom.weather", "city", message.command[1])
    await message.reply(f"<blockquote>Kota {message.command[1]} telah di tetapkan!</blockquote>", parse_mode=enums.ParseMode.HTML)


plugins_help["Cuaca"] = {
    "Cuaca [Kota]*": "Dapatkan cuaca di kota lu",
    "set_weather_city [city]*": f"Set Kota nya, contoh: {prefix}cuaca, Semarang sebagai default",
}
