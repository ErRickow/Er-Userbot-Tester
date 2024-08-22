import inspect
import sys
import traceback
from io import BytesIO, StringIO
from os import remove
from pprint import pprint

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import plugins_help, prefix, ignore_eval

from utils.anu import edit_or_reply

def _parse_eval(value=None):
    if not value:
        return value
    if hasattr(value, "stringify"):
        try:
            return value.stringify()
        except TypeError:
            passm
    elif isinstance(value, dict):
        try:
            return json_parser(value, indent=1)
        except BaseException:
            pass
    elif isinstance(value, list):
        newlist = "["
        for index, child in enumerate(value):
            newlist += "\n  " + str(_parse_eval(child))
            if index < len(value) - 1:
                newlist += ","
        newlist += "\n]"
        return newlist
    return str(value)
    
edit_or_reply = edit_or_reply

@Client.on_message(filters.command(["v", "pyth"], prefix) & filters.me)
async def tai(_, message: Message):
    try:
        cmd = message.text.split(maxsplit=1)[1]
    except IndexError:
        return await message.edit_or_reply("ha?", time=5)
    xx = None
    mode = ""
    spli = cmd.split()

   # async def get():
    #    try:
   #         cm = cmd.split(maxsplit=1)[1]
    #    except IndexError:
     #       await m.edit_or_reply("->> Wrong Format <<-")
       #     cm = None
       # return cm

    if spli[0] in ["-s", "--silent"]:
        await m.delete()
        mode = "silent"
    elif spli[0] in ["-n", "-noedit"]:
        mode = "no-edit"
        xx = await m.reply(get_string("com_1"))
    elif spli[0] in ["-gs", "--source"]:
        mode = "gsource"
    elif spli[0] in ["-ga", "--args"]:
        mode = "g-args"
    if mode:
        cmd = await get()
    if not cmd:
        return
    if not mode == "silent" and not xx:
        xx = await message.reply('sabar anjing!')
    #if black:
     #   try:
    #        cmd = black.format_str(cmd, mode=black.Mode())
      #  except BaseException:
            # Consider it as Code Error, and move on to be shown ahead.
        #    pass
    reply_to_id = message
    #if any(item in cmd for item in KEEP_SAFE().All) and (
       # not (m.out or m.sender_id == eruser_bot.uid)
 #   ):
        #warning = await m.forward_to(udB.get_key("LOG_CHANNEL"))
    await message.reply(
            f"Malicious Activities suspected by {(await message.get_sender())}"
            )
            
            ignore_eval.append(message.sender_id)
            return await xx.edit(
            "`Malicious Activities suspected⚠️!\nReported to owner. Aborted this request!`"
        )
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc, timeg = None, None, None, None
    tima = time.time()
    try:
        value = await aexec(cmd, message)
    except Exception:
        value = None
        exc = traceback.format_exc()
    tima = time.time() - tima
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    if value:
        try:
            if mode == "gsource":
                exc = inspect.getsource(value)
            elif mode == "g-args":
                args = inspect.signature(value).parameters.values()
                name = ""
                if hasattr(value, "__name__"):
                    name = value.__name__
                exc = f"**{name}**\n\n" + "\n ".join([str(arg) for arg in args])
        except Exception:
            exc = traceback.format_exc()
    evaluation = exc or stderr or stdout or _parse_eval(value)
    if mode == "silent":
        if exc:
            msg = f"• <b>EVAL ERROR\n\n• CHAT:</b> <code>(m.chat)</code> [<code>{m.chat_id}</code>]"
            msg += f"\n\n∆ <b>CODE:</b>\n<code>{cmd}</code>\n\n∆ <b>ERROR:</b>\n<code>{exc}</code>"
            log_chat = m.reply
            if len(msg) > 4000:
                with BytesIO(msg.encode()) as out_file:
                    out_file.name = "Eval-Error.txt"
                return await m.client.send_message(
                    log_chat, f"`{cmd}`", file=out_file
                )
            await message.client.send_message(log_chat, msg, parse_mode="html")
        return
    tmt = tima * 1000
    timef = time_formatter(tmt)
    timeform = timef if not timef == "0s" else f"{tmt:.3f}ms"
    final_output = "__►__ **EVAL** (__in {}__)\n```{}``` \n\n __►__ **OUTPUT**: \n```{}``` \n".format(
        timeform,
        cmd,
        evaluation,
    )
    if len(final_output) > 4096:
        final_output = evaluation
        with BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await m.client.send_file(
                m.chat_id,
                out_file,
                force_document=True,
                #thumb=ULTConfig.thumb,
                allow_cache=False,
                caption=f"```{cmd}```" if len(cmd) < 998 else None,
                reply_to=m
            )
        return await xx.delete()
    await xx.reply(final_output)


def _stringify(text=None, *args, **kwargs):
    if text:
        u._ = text
        text = _parse_eval(text)
    return print(text, *args, **kwargs)


