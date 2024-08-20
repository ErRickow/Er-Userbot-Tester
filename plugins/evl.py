from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import traceback

from utils.misc import plugins_help, prefix
from utils.anu import format_exc

@Client.on_message(
    filters.command(["ev"], prefix) & filters.me
)  # Ganti OWNER_ID dengan ID Anda
async def eval_command(client, message):
    if not message.reply_to_message:
        await message.reply("Silakan balas pesan dengan kode yang ingin dieksekusi.")
        return

    code = message.reply_to_message.text

    # Menambahkan context untuk keamanan
    safe_dict = {
        'client': client,
        'message': message,
        'app': app,
        '__name__': '__main__',
        '__file__': 'eval.py',
        'asyncio': asyncio,
    }

    try:
        exec_code = f"async def func():\n{textwrap.indent(code, '    ')}"
        exec(exec_code, safe_dict)
        
        result = await safe_dict['func']()
        
        if result is None:
            result = "Tidak ada output."
        
        await message.reply(f"Output:\n{result}")
    except Exception as e:
        await message.reply(f"Error:\n{traceback.format_exc()}")