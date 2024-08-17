import time
import pytz
import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.anu import time_formatter
from utils.misc import plugins_help, prefix

from pytz import timezone
from datetime import datetime

a = timezone("Asia/Jakarta")
sekarang = datetime.now(a)
print(sekarang)

@Client.on_message(filters.command(["ping", "p"], prefix) & filters.me)
async def get_readable_time(_, message: Message):
    start = time.time()
    nganu = time.time() - start
    uptime = time_formatter(datetime.datetime())
    await message.reply(f"<blockquote>❏ POMG!!🏓 {nganu * 1000:.3f}ms\n├• Uptime {uptime}</blockquote>")


plugins_help["ping"] = {
    "ping": "Check ping to Telegram servers",
}
