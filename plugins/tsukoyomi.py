from pyrogram import Client
from pyrogram import Client as ren
from pyrogram import *
from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.types import Message

from utils.handler import *
from utils.misc import plugins_help, prefix

@Client.on_message(
    filters.command(["shinratensei", "zombies", "tsukoyomi"], prefix) & filters.me
)
