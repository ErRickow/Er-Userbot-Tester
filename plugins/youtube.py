# code by @xtdevs
# without cookies

import os
import time

import requests
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from pyrogram import Client, filters

from utils.db import db
from utils.driver import YoutubeDriver
from utils.formatter import secs_to_mins
from utils.misc import plugins_help, prefix, ErRick, input_user
from utils.anu import progress
from utils.config import *


@Client.on_message(filters.command(["ytlink"], prefix) & filters.me)
async def ytlink(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give something to search on youtube.")
    query = await input_user(message)
    pro = await message.reply_text("Searching ...")
    try:
        results = YoutubeDriver(query, 7).to_dict()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Error:** `{e}`")
    if not results:
        return await pro.edit_text("No results found.")
    text = f"**🔎 𝖳𝗈𝗍𝖺𝗅 𝖱𝖾𝗌𝗎𝗅𝗍𝗌 𝖥𝗈𝗎𝗇𝖽:** `{len(results)}`\n\n"
    for result in results:
        text += f"**𝖳𝗂𝗍𝗅𝖾:** `{result['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{result['channel']}`\n**𝖵𝗂𝖾𝗐𝗌:** `{result['views']}`\n**𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{result['duration']}`\n**𝖫𝗂𝗇𝗄:** `https://youtube.com{result['url_suffix']}`\n\n"
    await pro.edit_text(text, disable_web_page_preview=True)
