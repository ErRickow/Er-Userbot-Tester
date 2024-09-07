import time
import pytz

from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.anu import time_formatter
from utils.misc import plugins_help, prefix, emopong

StartTime = time.time()

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
async def anu(client, message):
    start = time.time()
    uptime = get_readable_time((time.time() - StartTime))
    nganu = time.time() - start
    await message.reply(f"<blockquote>{emopong}<b>PONG!!</b> - {nganu * 1000:.3f}ms\n<b>├• Aktif!!</b> - <code>{uptime}</code>\n<b>├• Owner</b> - {client.me.mention}\n<b>╰• </b><i>Ξr 𖨆♡𖨆 lop u yek</i></blockquote>")

@Client.on_message(filters.command(["kping", "kp"], prefix) & filters.me)
async def custom_ping_handler(client: Client, message: Message):
    uptime = get_readable_time((time.time() - StartTime))
    start = dt.now()
    lol = await message.reply_text("**Pong!!**")
    await asyncio.sleep(1.5)
    end = dt.now()
    duration = (end - start).microseconds / 1000
    await lol.edit_text(
        f" **Pong !!** " f"`%sms` \n" f" **Uptime** - " f"`{uptime}` " % (duration)
    )


plugins_help["ping"] = {
    "ping": "Check ping to Telegram servers",
}
