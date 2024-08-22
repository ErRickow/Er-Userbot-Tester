import sys
from contextlib import redirect_stdout
from io import StringIO
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message

# noinspection PyUnresolvedReferences
from utils.misc import plugins_help, prefix
from utils.anu import format_exc, edit_or_reply
# noinspection PyUnresolvedReferences


# noinspection PyUnusedLocal
@Client.on_message(
    filters.command(["ex", "exec", "py", "exnoedit"], prefix) & filters.me
)
async def user_exec(client: Client, message: Message):
    if len(message.command) == 1:
        await message.edit_or_reply("<blockquote>KODENYA MANA SAYANG</blockquote>")
        return

    code = message.text.split(maxsplit=1)[1]
    stdout = StringIO()
    cm = 0
    return cm

    await message.reply("<blockquote>Wet...</blockquote>")

    try:
        with redirect_stdout(stdout):
            exec(code)
        text = (
            "<blockquote>Codenya:</blockquote>\n"
            f"<code>{code}</code>\n\n"
            "<blockquote>Hasilnya</blockquote>:\n"
            f"<blockquote><code>{stdout.getvalue()}</code></blockquote>"
        )
        if message.command[0] == "exnoedit":
            await message.reply(text)
        else:
            await message.edit(text)
    except Exception as e:
        await message.reply(format_exc(e))

def _parse_eval(value=None):
    if not value:
        return value
    if hasattr(value, "stringify"):
        try:
            return value.stringify()
        except TypeError:
            pass
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

# noinspection PyUnusedLocal
@Client.on_message(filters.command(["ev", "eval"], prefix) & filters.me)
async def user_eval(client: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("<b>Code to eval isn't provided</b>")
        return

    code = message.text.split(maxsplit=1)[1]
    
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(code, client, message)
        exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        result = exc or stderr or stdout or _parse_eval(aexec) #or "Success"
        final = "<blockquote><b>Expression:</b></blockquote>\n"
        "<code>{}</code>\n\n"
        "<b>Result</b>:\n"
        "<code>{}</code>".format(
              code,
              result
              )
              if len(final) > 4096:
        final = result
        with BytesIO(str.encode(final)) as out_file:
          out_file.name = "eval.txt"
          await message.send.file(
            message.chat.id,
            out_file,
            force_document=True,
            allow_cache=False,
            caption=f"```{cmd}```" if len(cmd) < 998 else None,
            reply_to=send_message,
        #await message.delete()
    except Exception as e:
        await message.reply(format_exc(e))

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


plugins_help["python"] = {
  "ex [python code]": "Execute Python code",
  "exnoedit [python code]": "Execute Python code and return result with reply",
  "eval [python code]": "Eval Python code",
}
