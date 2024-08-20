import re
import asyncio
import os
import sys
import shutil
import subprocess

from git import Repo
from git.exc import InvalidGitRepositoryError

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import plugins_help, prefix, requirements_list
from utils.db import db
from utils.anu import format_exc, restart


def check_command(command):
    return shutil.which(command) is not None


@Client.on_message(filters.command("restart", prefix) & filters.me)
async def restart_cmd(_, message: Message):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "restart",
            "chat_id": message.chat.id,
            "message_id": message.id,
        },
    )

    if "LAVHOST" in os.environ:
        await message.edit("<b>Your lavHost is restarting...</b>")
        os.system("lavhost restart")
        return

    await message.reply("<blockquote>Sedang Merestart...</blockquote>")
    restart()

@Client.on_message(filters.command("update", prefix) & filters.me)
async def update(_, message: Message):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "update",
            "chat_id": message.chat.id,
            "message_id": message.id,
        },
    )

    if "LAVHOST" in os.environ:
        await message.edit("<b>Your lavHost is updating...</b>")
        os.system("lavhost update")
        return

   xx = await message.reply("<blockquote>Wet...<blockquote>\n<blockquote>Sedang Update!</blockquote>")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "pip"])
        subprocess.run(["git", "pull"])
    except Exception as e:
        await xx.reply(format_exc(e))
        db.remove("core.updater", "restart_info")
    else:
        i = await xx.edit("<blockquote>Update: selesai sayang!<blockquote>\n\n<blockquote>Merestart...</blockquote>")
        restart()
        await i.edit("<b>_Sudah Selesai Restartnya sayang_...</b>")

#nganu


plugins_help["updater"] = {
    "update": "Update Userbot Lu. Jika ada update an.",
    "restart": "Restart Userbotnya",
}
