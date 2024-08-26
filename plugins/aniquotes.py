from random import choice, randint

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import plugins_help, prefix
from utils.anu import format_exc


@Client.on_message(filters.command(['aniq', 'aq'], prefix) & filters.me)
async def aniquotes_handler(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.text:
        query = message.reply_to_message.text[:512]
    elif message.reply_to_message and message.reply_to_message.caption:
        query = message.reply_to_message.caption[:512]
    elif len(message.command) > 1:
        query = message.text.split(maxsplit=1)[1][:512]
    else:
        return await message.reply('<b>[💮 Aniquotes] <i>Kasih teks nya bego.</i></b>', parse_mode=enums.ParseMode.HTML)

    try:
        await message.delete()
        result = await client.get_inline_bot_results('@QuotAfBot', query)
        return await message.reply_inline_bot_result(query_id=result.query_id,
                                                     result_id=result.results[randint(1, 2)].id,
                                                     reply_to_message_id=message.reply_to_message.id if
                                                     message.reply_to_message else None)
    except Exception as e:
        return await message.reply(f'<b>[💮 Aniquotes]</b>\n<code>{format_exc(e)}</code>', parse_mode=enums.ParseMode.HTML)


plugins_help['aniquotes'] = {
    'aq [text]': 'Create animated sticker with text',
}
