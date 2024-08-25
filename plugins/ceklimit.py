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

@Client(
    ~filters.scheduled
    & filters.command(["limit", "limited"], prefix)
    & filters.me
    & ~filters.forwarded
)

