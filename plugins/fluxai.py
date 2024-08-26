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
from utils.anu import progress
from utils.misc import plugins_help, prefix

class Post:
    def __init__(self, source: dict, session: ClientSession):
        self._json = source
        self.session = session

    @property
    async def image(self):
        return (
            self.file_url
            if self.file_url
            else self.large_file_url
            if self.large_file_url
            else self.source
            if self.source and "pximg" not in self.source
            else await self.pximg
            if self.source
            else None
        )

    @property
    async def pximg(self):
        async with self.session.get(self.source) as response:
            return BytesIO(await response.read())

    def __getattr__(self, item):
        return self._json.get(item)


async def schellwithflux(args):
    API_URL = "https://randydev-ryuzaki-api.hf.space/api/v1/akeno/fluxai"
    payload = {
        "user_id": 1191668125,  # Please don't edit here
        "args": args
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code != 200:
        #message.reply(f"Error status {response.status_code}")
        #return None
      return response.content

@Client.on_message(filters.command(["fluxai"], prefix) & filters.me)
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

