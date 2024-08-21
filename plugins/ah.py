from prettytable import PrettyTable
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from utils.misc import plugins_help, prefix, tolong_anu
from utils.anu import edit_or_reply, split_list

@Client.on_message(filters.command(["tolong", "t"], prefix) & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        ac = PrettyTable()
        ac.header = False
        ac.title = "PyroMan-UserBot Modules"
        ac.align = "l"
        for x in split_list(sorted(tolong_anu.keys()), 2):
            ac.add_row([x[0], x[1] if len(x) >= 2 else None])
        await edit_or_reply(
            message, f"```{str(ac)}```\n• @Lunatic0de × @SharingUserbot •"
        )
        await message.reply(
            f"**Contoh Ketik** `{CMD_HANDLER}help afk` **Untuk Melihat Informasi Module**"
        )

    if help_arg:
        if help_arg in tolong_anu:
            commands: dict = tolong_anu[help_arg]
            this_command = f"──「 **Help For {str(help_arg).upper()}** 」──\n\n"
            for x in commands:
                this_command += f"  •  **Command:** `{CMD_HANDLER}{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
            this_command += "© @Lunatic0de"
            await edit_or_reply(
                message, this_command, parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await edit_or_reply(
                message,
                f"`{help_arg}` **Bukan Nama Modul yang Valid.**",
            )


def add_command_help(module_name, commands):
    if module_name in tolong_anu.keys():
        command_dict = tolong_anu[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    tolong_anu[module_name] = command_dict
