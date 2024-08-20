from pyrogram import Client, filters
from pyrogram.types import Message

from utils.db import db
from utils.misc import plugins_help, prefix
from utils.anu import restart


@Client.on_message(
    filters.command(["sp", "setprefix", "Ersetprefix"], prefix) & filters.me
)
async def setprefix(_, message: Message):
    if len(message.command) > 1:
        pref = message.command[1]
        db.set("core.main", "prefix", pref)
        await message.reply(f"<blockquote>Prefix [ <code>{pref}</code> ] telah di set!</blockquote>")
        restart()
    else:
        await message.reply("<blockquote>Prefix gaboleh kosong kontol!</blockquote>")


plugins_help["prefix"] = {
    "setprefix [prefix]": "Set custom prefix",
    "Erprefix [prefix]": "Set custom prefix",
}
