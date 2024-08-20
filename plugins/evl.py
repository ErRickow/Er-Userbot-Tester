from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import traceback
import re
import sys
import subprocess

from io import StringIO

from utils.misc import plugins_help, prefix
from utils.anu import format_exc

@Client.on_message(
    filters.command(["ev"], prefix) & filters.me
)  # Ganti OWNER_ID dengan ID Anda
async def evaluate_handler(_, m: Message):
    """ This function is made to execute python codes """

    try:

        if app.long() == 1:
            return await app.send_edit(
                "Give me some text (code) to execute . . .",
                text_type=["mono"],
                delme=4
            )
        text = m.sudo_message.text if getattr(m, "sudo_message", None) else m.text
        cmd = text.split(None, 1)[1]

        msg = await app.send_edit("Executing . . .", text_type=["mono"])

        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        stdout, stderr, exc = None, None, None

        try:
            await app.aexec(cmd)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = exc or stderr or stdout or "Success"
        final_output = f"**• PROGRAM:**\n\n`{cmd}`\n\n**• OUTPUT:**\n\n`{evaluation.strip()}`"

        if len(final_output) > 4096:
            await app.create_file(
                filename="eval_output.txt",
                content=str(final_output),
                caption=f"`{cmd}`"
            )
            await msg.delete()
        else:
            await app.send_edit(final_output)
    except Exception as e:
        await app.error(e)
