import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from anu.alat import get_arg
from utils.misc import plugins_help, prefix

@Client.on_message(
    filters.command(["q"], prefix) & filters.me
    )
async def quotly(client: Client, message: Message):
    args = get_arg(message)
    if not message.reply_to_message and not args:
        return await message.reply("<b>Mohon Balas ke Pesan</b>")
    bot = "QuotLyBot"
    if message.reply_to_message:
        await message.edit("<i>Making a Quote . . .</i>")
        await client.unblock_user(bot)
        if args:
            await client.send_message(bot, f"/qcolor {args}")
            await asyncio.sleep(1)
        else:
            pass
        await message.reply_to_message.forward(bot)
        await asyncio.sleep(5)
        async for quotly in client.search_messages(bot, limit=1):
            if quotly:
                await message.delete()
                await message.reply_sticker(
                    sticker=quotly.sticker.file_id,
                    reply_to_message_id=message.reply_to_message.id
                    if message.reply_to_message
                    else None,
                )
            else:
                return await message.edit("**Gagal Membuat Sticker Quotly**")
                
plugins_help["Quotes"] = {
  "q : buat sticker quotes dari teks reply",
}
