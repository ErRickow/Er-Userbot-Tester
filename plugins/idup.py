# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import os
import time
from platform import python_version

from pyrogram import Client
from pyrogram import __version__ as versipyro
from pyrogram import filters
from pyrogram.types import Message
from telegraph import exceptions, upload_file

from utils.misc import useruserbot_versionsion
from config import GROUP
from utils.misc import plugins_help, prefix
from utils.anu import edit_or_reply, ReplyCheck
from utils.db import database
from anu.alat import convert_to_image
from utils.anu import restart

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

modules = prefix
alive_logo = (
    gvarstatus("ALIVE_LOGO") or "https://telegra.ph/file/9dc4e335feaaf6a214818.jpg"
)
emoji = gvarstatus("ALIVE_EMOJI") or "⚡️"
alive_text = gvarstatus("ALIVE_TEKS_CUSTOM") or "Hey, I am alive."


@Client.on_message(filters.command(["alive", "awake"], cmd) & filters.me)
async def alive(client: Client, message: Message):
    xx = await edit_or_reply(message, "⚡️")
    await asyncio.sleep(2)
    send = client.send_video if alive_logo.endswith(".mp4") else client.send_photo
    uptime = await get_readable_time((time.time() - StartTime))
    man = (
        f"**[PyroMan-Userbot](https://github.com/mrismanaziz/PyroMan-Userbot) is Up and Running.**\n\n"
        f"<b>{alive_text}</b>\n\n"
        f"{emoji} <b>Master :</b> {client.me.mention} \n"
        f"{emoji} <b>Modules :</b> <code>{len(modules)} Modules</code> \n"
        f"{emoji} <b>Bot Version :</b> <code>{userbot_version}</code> \n"
        f"{emoji} <b>Python Version :</b> <code>{python_version()}</code> \n"
        f"{emoji} <b>Pyrogram Version :</b> <code>{versipyro}</code> \n"
        f"{emoji} <b>Bot Uptime :</b> <code>{uptime}</code> \n\n"
        #f"    **[𝗦𝘂𝗽𝗽𝗼𝗿𝘁](https://t.me/{GROUP})** | **[𝗖𝗵𝗮𝗻𝗻𝗲𝗹](https://t.me/{CHANNEL})** | **[𝗢𝘄𝗻𝗲𝗿](tg://user?id={client.me.id})**"
    )
    try:
        await asyncio.gather(
            xx.delete(),
            send(
                message.chat.id,
                alive_logo,
                caption=man,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    except BaseException:
        await xx.edit(man, disable_web_page_preview=True)


@Client.on_message(filters.command("setalivelogo", cmd) & filters.me)
async def setalivelogo(client: Client, message: Message):
    try:
        import ProjectMan.helpers.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    Man = await edit_or_reply(message, "`Processing...`")
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await Man.edit(f"**ERROR:** `{exc}`")
            os.remove(m_d)
            return
        link = f"https://telegra.ph/{media_url[0]}"
        os.remove(m_d)
    sql.addgvar("ALIVE_LOGO", link)
    await Man.edit(
        f"**Berhasil Mengcustom ALIVE LOGO Menjadi {link}**",
        disable_web_page_preview=True,
    )
    restart()


@Client.on_message(filters.command("setalivetext", cmd) & filters.me)
async def setalivetext(client: Client, message: Message):
    try:
        import ProjectMan.helpers.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    Man = await edit_or_reply(message, "`Processing...`")
    if not text:
        return await edit_or_reply(
            message, "**Berikan Sebuah Text atau Reply ke text**"
        )
    sql.addgvar("ALIVE_TEKS_CUSTOM", text)
    await Man.edit(f"**Berhasil Mengcustom ALIVE TEXT Menjadi** `{text}`")
    restart()


@Client.on_message(filters.command("setemoji", cmd) & filters.me)
async def setemoji(client: Client, message: Message):
    try:
        import ProjectMan.helpers.SQL.globals as sql
    except AttributeError:
        await message.edit("**Running on Non-SQL mode!**")
        return
    emoji = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    Man = await edit_or_reply(message, "`Processing...`")
    if not emoji:
        return await edit_or_reply(message, "**Berikan Sebuah Emoji**")
    sql.addgvar("ALIVE_EMOJI", emoji)
    await Man.edit(f"**Berhasil Mengcustom EMOJI ALIVE Menjadi** {emoji}")
    restart()