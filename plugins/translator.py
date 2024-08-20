# TODO
# WARNING! IT COMMENTED FULLY SINCE INSTALL PACKAGES FROM THIS MODULE WILL
# BROKE ALL FUCKING Moon, NOT JUST THIS MODULE
# THIS MODULE IS INCOMPATIBLE WITH LAST Moon VERSION
# SINCE IT USE OUTDATED PACKAGE WITH BROKEN DEPENDENCIES
# IT NEEDS TO BE REWRITEN

from utils.scripts import format_small_module_help, import_library
from utils.misc import plugins_help, prefix
from pyrogram import Client, filters

googletrans = import_library("googletrans", "googletrans-py")
from googletrans import Translator

trl = Translator()

@Client.on_message(filters.command(["trans", "tr"], prefix) & filters.me)
async def translatedl(_client, message):
    try:
        if len(message.command) > 1:
            dtarget = message.text.split(None, 2)[1]
        else:
            dtarget = 'id'
        if len(message.command) > 2:
            dtext = message.text.split(None, 2)[2]
        elif message.reply_to_message:
            dtext = message.reply_to_message.text
        else:
         ed = message.reply(format_small_module_help("translator"))
        await ed.edit("<b>Translating</b>")
        dtekstr = trl.translate(dtext, dest=dtarget)
        await ed.edit_text(f"<b>Translated</b> to <code>{dtarget}</code> :\n\n" + "{}".format(dtekstr.text))
    except ValueError as err:
        await message.reply("Error: <code>{}</code>".format(str(err)))
        return


plugins_help["translator"] = {
    "tr": "[lang]* [text/reply]* translate message",
    "trans": "[lang]* [text/reply]* translate message \n If lang not given it'll use default(en)",
}
