import os

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import plugins_help, prefix
from utils.anu import format_module_help, with_reply

current_page = 0
total_pages = 0

async def send_page(message, module_list, page, total_pages):
    start_index = (page - 1) * 10
    end_index = start_index + 10
    page_modules = module_list[start_index:end_index]
    text = f"<blockquote>Bantuan untuk <a href=https://t.me/Pamerdong>Ubot Anu</a></blockquote>\n"
    text += f"Untuk bantuan menggunakan Userbotnya, ketik <code>{prefix}help [nyari apa]</code>\n\n"
    text += f"Page {page}/{total_pages}\n\n"
    for module_name in page_modules:
        commands = plugins_help[module_name]
        text += f"<blockquote>• {module_name.title()}:</blockquote> {', '.join([f'<code>{prefix + cmd_name.split()[0]}</code>' for cmd_name in commands.keys()])}\n"
    text += f"\n<blockquote>The number of modules in the userbot: {len(plugins_help)}</blockquote>"
    await message.edit(text, disable_web_page_preview=True)


@Client.on_message(filters.command(["help", "h"], prefix) & filters.me)
async def help_cmd(_, message: Message):
    if len(message.command) == 1:
        global current_page, total_pages
        module_list = list(plugins_help.keys())
        total_pages = (len(module_list) + 9) // 10
        current_page = 1
        await send_page(message, module_list, current_page, total_pages)
    elif message.command[1].lower() in plugins_help:
        await message.edit(format_module_help(message.command[1].lower(), prefix))
    else:
        command_name = message.command[1].lower()
        module_found = False
        for module_name, commands in plugins_help.items():
            for command in commands.keys():
                if command.split()[0] == command_name:
                    cmd = command.split(maxsplit=1)
                    cmd_desc = commands[command]
                    module_found = True
                    return await message.reply(
                        f"<blockquote>Help for command <code>{prefix}{command_name}</code></blockquote>\n"
                        f"Module: {module_name} (<code>{prefix}help {module_name}</code>)\n\n"
                        f"<code>{prefix}{cmd[0]}</code>"
                        f"{' <code>' + cmd[1] + '</code>' if len(cmd) > 1 else ''}"
                        f" — <i>{cmd_desc}</i>",
                    )
        if not module_found:
            await message.edit(f"<blockquote>Module or command {command_name} not found</blockquote>")

@Client.on_message(filters.command(["pn", "pp", "pq"], prefix) & filters.me)
@with_reply
async def handle_navigation(_, message: Message):
    if message.reply_to_message:
        global current_page
        if message.command[0].lower() == "pn":
            if current_page < total_pages:
                current_page += 1
                await send_page(message, list(plugins_help.keys()), current_page, total_pages)
                return await message.reply_to_message.delete()
            else:
                await message.edit("No more pages available.")
        elif message.command[0].lower() == "pp":
            if current_page > 1:
                current_page -= 1
                await send_page(message, list(plugins_help.keys()), current_page, total_pages)
                return await message.reply_to_message.delete()
            else:
                return await message.edit("This is the first page.")
        elif message.command[0].lower() == "pq":
            await message.reply_to_message.delete()
            return await message.reply("Help closed.")


plugins_help["help"] = {
    "help [module/command name]": "Get common/module/command help",
    "pn/pp/pq": "Navigate through help pages"
    + " (pn: next page, pp: previous page, pq: quit help)",
    }
