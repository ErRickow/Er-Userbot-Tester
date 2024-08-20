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

@Client.on_message(filters.command("up", prefix) & filters.me)
async def ngapdate(client, message):
  user = message.from_user.id
  pros = await message.reply(
        f"<blockquote> <b>Memeriksa pembaruan resources ..</b></blockquote>"
    )
  out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
  teks = f"<b>❒ Status resources :</b>\n"
  memeg = f"<b>Change logs </b>"
  if "Already up to date." in str(out):
        return await pros.edit(f"<blockquote>{teks}┖ {out}</blockquote>")
  if len(out) > 4096:
          anuk = await pros.edit(
            f"<blockquote> <b>Hasil akan dikirimkan dalam bentuk file ..</b></blockquote>"
        )
  with open("output.txt", "w+") as file:
            file.write(out)

            X = f"<blockquote> <b>Change logs </b></blockquote>"
  await client.send_document(
          message.chat.id,
          "output.txt",
          caption=f"{X}",
          reply_to_message_id=message.id,
          )
  else
  await anuk.delete()
  os.remove("output.txt")
  format_line = [f"┣ {line}" for line in out.splitlines()]
  if format_line:
    format_line[-1] = f"┖ {format_line[-1][2:]}"
    format_output = "\n".join(format_line)

  await pros.edit(f"<blockquote>{memeg}\n\n{teks}{format_output}</blockquote>")
  os.execl(sys.executable, sys.executable, "erbanget.py")