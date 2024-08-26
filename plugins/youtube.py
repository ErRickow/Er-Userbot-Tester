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

@Client.on_message(filters.command(["ytv"], prefix) & filters.me)
async def ytvideo(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube link to download video."
        )
    query = await input_user(message)
    pro = await message.reply_text("Checking ...")
    status, url = YoutubeDriver.check_url(query)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text("🎼 __Downloading video ...__")
    try:
        with YoutubeDL(YoutubeDriver.video_options()) as ytdl:
            yt_data = ytdl.extract_info(url, True)
            yt_file = yt_data["id"]

        upload_text = f"<b>⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...</b>\n\n<b>𝖳𝗂𝗍𝗅𝖾:</b> `{yt_data['title'][:50]}`\n<b>𝖢𝗁𝖺𝗇𝗇𝖾𝗅:</b> <i>{yt_data['channel']}</b>"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        await message.reply_video(
            f"{yt_file}.mp4",
            caption=f"<b>🎧 𝖳𝗂𝗍𝗅𝖾:</b> {yt_data['title']} \n\n<b>👀 𝖵𝗂𝖾𝗐𝗌:</b> <i>{yt_data['view_count']}</i> \n<b>⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:</b> <i>{secs_to_mins(int(yt_data['duration']))}</b>",
            duration=int(yt_data["duration"]),
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text,
            ),
        )
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"<b>🍀 Video not Downloaded:</b> <i>{e}</b>")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp4")
    except:
        pass

@Client.on_message(filters.command(["yta"], prefix) & filters.me)
async def youtube_audio(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube link to download audio."
        )
    query = await input_user(message)
    pro = await message.reply_text("Checking ...")
    status, url = YoutubeDriver.check_url(query)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text("🎼 <i>Downloading audio ...</b>")
    try:
        with YoutubeDL(YoutubeDriver.song_options()) as ytdl:
            yt_data = ytdl.extract_info(url, False)
            yt_file = ytdl.prepare_filename(yt_data)
            ytdl.process_info(yt_data)
        upload_text = f"<b>⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...</b> \n\n<b>𝖳𝗂𝗍𝗅𝖾:</b> `{yt_data['title'][:50]}`\n<b>𝖢𝗁𝖺𝗇𝗇𝖾𝗅:</b> <code>{yt_data['channel']}</code>"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        await message.reply_audio(
            f"{yt_file}.mp3",
            caption=f"<b>🎧 𝖳𝗂𝗍𝗅𝖾:</b> {yt_data['title']} \n\n<b>👀 𝖵𝗂𝖾𝗐𝗌:</b> <code>{yt_data['view_count']}</code> \n<b>⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:</b> <code>{secs_to_mins(int(yt_data['duration']))}</code>",
            duration=int(yt_data["duration"]),
            performer="[Akeno UB]",
            title=yt_data["title"],
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text,
            ),
        )
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"<b>🍀 Audio not Downloaded:</b> <code>{e}</code>")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp3")
    except:
        pass

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
