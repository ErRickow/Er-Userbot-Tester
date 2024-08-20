import time
import pytz

from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.anu import time_formatter
from utils.misc import plugins_help, prefix

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


@Client.on_message(filters.command(["ping", "p"], prefix) & filters.me)
async def get_readable_time(_, message: Message):
    start = time.time()
    nganu = time.time() - start
    uptime = time_formatter(time.time())
    await message.reply(f"<blockquote>❏ POMG!!🏓 {nganu * 1000:.3f}ms\n├• Uptime {uptime}</blockquote>Owner")


plugins_help["ping"] = {
    "ping": "Check ping to Telegram servers",
}
