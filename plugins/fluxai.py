import io
import time

import requests
from PIL import Image
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *

from aiohttp import ClientSession
from io import BytesIO

session = ClientSession()

from utils.handler import *
from utils.anu import progress, edit_or_reply
from utils.misc import plugins_help, prefix, ErRick

async def schellwithflux(args):
    API_URL = "https://randydev-ryuzaki-api.hf.space/api/v1/akeno/fluxai"
    payload = {
        "user_id": 1191668125,  # Please don't edit here
        "args": args
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code != 200:
        edit_or_reply(f"Error status {response.status_code}")
        return None
        return response.content

@ErRick(
    filters.command(["fluxai"], prefix)
    & filters.me
    & ~filters.forwarded
)
async def imgfluxai_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("mo apa kontol.")
    try:
        image_bytes = await schellwithflux(question)
        if image_bytes is None:
            return await message.reply_text("gagal dah.")
        pro = await message.reply_text("Generating image, sabar sayang...")
        with open("flux_gen.jpg", "wb") as f:
            f.write(image_bytes)
        ok = await pro.edit_text("Uploading image...")
        await message.reply_photo("flux_gen.jpg", progress=progress, progress_args=(ok, time.time(), "Uploading image..."))
        await ok.delete()
        if os.path.exists("flux_gen.jpg"):
            os.remove("flux_gen.jpg")
    except Exception as e:
        await message.edit(format_exc(e))

