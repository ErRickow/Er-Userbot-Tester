from pyrogram import Client
from pyrogram import Client as ren
from pyrogram import *
from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.types import Message

from utils.handler import *
from utils.misc import plugins_help, prefix

@Client.on_message(
    filters.command(["shinratensei", "zombies", "tsukoyomi"], prefix) & filters.me
)

async def akundeak(client: Client, message: Message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await message.reply("Finding ghosts...")

    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except ChatAdminRequired:
                await m.edit_text("i not admin required")
                return
            banned_users += 1
        await m.edit_text(f"Banned {banned_users} Deleted Accounts")
    else:
        await m.edit_text("There are no deleted accounts in this chat")
