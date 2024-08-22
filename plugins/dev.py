import sys
from contextlib import redirect_stdout
from io import StringIO

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

    await message.reply("<blockquote>Wet...</blockquote>")

    try:
        with redirect_stdout(stdout):
            exec(code)
        text = (
            "<blockquote>Codenya:</blockquote>\n"
            f"<code>{code}</code>\n\n"
            "<blockquote>Hasilnya</blockquote>:\n"
            f"<code>{stdout.getvalue()}</code>"
        )
        if message.command[0] == "exnoedit":
            await message.reply(text)
        else:
            await message.edit(text)
    except Exception as e:
        await message.reply(format_exc(e))


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

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = exc or stderr or stdout or _parse_eval(value) #or "Success"
        await message.reply(
            "<b>Expression:</b>\n"
            f"<code>{code}</code>\n\n"
            "<b>Result</b>:\n"
            f"<code>{result}</code>"
        )
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
