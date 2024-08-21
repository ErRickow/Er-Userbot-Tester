from pyrogram import Client, filters
from pyrogram.types import Message

from telegraph import exceptions, upload_file
from utils.db import db
from utils.misc import plugins_help, prefix, emo
from utils.anu import edit_or_reply
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

@Client.on_message(
    filters.command(["semo", "setemoji", "Eremo"], prefix) & filters.me
)
async def setemoji(client: Client, message: Message):
  try:
      import utils.db as puh
  except AttributeError:
      await message.reply("Running on Non-DB mode!")
      return

  emoji = (message.text.split(None, 1)[1]
          if len(message.command) != 1
          else None)
  eri = await edit_or_reply(message, "<i>Processing...</i>")
  if not emoji:
    return await edit_or_reply(message, "Berikan Sebuah Emoji")
  puh.db.set("emo", emoji)
  await eri.reply(f"Berhasil Mengcustom EMOJI ALIVE Menjadi {emoji}")
  restart()

  #  else:
     #   await message.reply("<blockquote>Emoji gaboleh kosong kontol!</blockquote>")

@Client.on_message(
    filters.command(["delmo", "delemoji", "Erdelemo"], prefix) & filters.me
)
async def emoji(_, message: Message):
    #if len(message.command) > 1:
        await message.db.remove("core-main", "emo")
        await message.reply(f"emoji telah di hapus!")
        restart()
        
@Client.on_message(
    filters.command(["getmo", "getemoji", "Ergemo"], prefix) & filters.me
)
async def emoji(_, message: Message):
    if len(message.command) > 1:
        em = message.command[1]
        db.get("core.main", "emo", em)
        await message.reply(f"<blockquote>emojinya [ <code>{em}</code> ] !</blockquote>")
        restart()
    else:
        await message.reply("<blockquote>Emoji gaboleh kosong kontol!</blockquote>")




plugins_help["prefix"] = {
    "setprefix [prefix]": "Set custom prefix",
    "Erprefix [prefix]": "Set custom prefix",
}
