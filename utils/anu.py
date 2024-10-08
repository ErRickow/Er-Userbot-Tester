import asyncio
import importlib
import math
import os
import re
import shlex
import subprocess
import sys
import time
import traceback
from io import BytesIO
from types import ModuleType
from typing import Dict, List, Optional, Tuple, Union

from PIL import Image
import psutil
from pyrogram import Client, errors, enums
from pyrogram.errors import FloodWait, MessageNotModified
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from pyrogram.types import Chat, Message, User

from utils.db import db

from .misc import plugins_help, prefix, requirements_list

META_COMMENTS = re.compile(r"^ *# *meta +(\S+) *: *(.*?)\s*$", re.MULTILINE)
interact_with_to_delete = []


def time_formatter(milliseconds: int) -> str:
    """Time Formatter"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " hari, ") if days else "")
        + ((str(hours) + " jam, ") if hours else "")
        + ((str(minutes) + " menit, ") if minutes else "")
        + ((str(seconds) + " detik, ") if seconds else "")
        + ((str(milliseconds) + " perdetik, ") if milliseconds else "")
    )
    return tmp[:-2]


def humanbytes(size):
    """Convert Bytes To Bytes So That Human Can Read It"""
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def edit_or_send_as_file(
    tex: str,
    message: Message,
    client: Client,
    caption: str = "<code>Result!</code>",
    file_name: str = "result",
):
    """Send As File If Len Of Text Exceeds Tg Limit Else Edit Message"""
    if not tex:
        await message.edit("<code>Wait, What?</code>")
        return
    if len(tex) > 1024:
        await message.edit("<code>OutPut is Too Large, Sending As File!</code>")
        file_names = f"{file_name}.txt"
        with open(file_names, "w") as fn:
            fn.write(tex)
        await client.send_document(message.chat.id, file_names, caption=caption)
        await message.delete()
        if os.path.exists(file_names):
            os.remove(file_names)
        return
    return await message.edit(tex)

async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]

async def dpaste(code: str):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        data = {"content": code, "lexer": "python", "expires": "never"}
        async with session.post("https://dpaste.org/api/", data=data) as resp:
            if resp.status != 200:
                return "Pasting failed!"
            else:
                return (await resp.text()).replace('"', "")

async def paste_neko(code: str):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(
                "https://nekobin.com/api/documents",
                json={"content": code},
            ) as paste:
                paste.raise_for_status()
                result = await paste.json()
    except Exception:
        return await dpaste(code=code)
    else:
        return f"nekobin.com/{result['result']['key']}.py"

def get_args_raw(message: Union[Message, str], use_reply: bool = None) -> str:
    """Returns text after command.

    Args:
        message (Union[Message, str]): Message or text.

        use_reply (bool, optional): Try to get args from reply message if no args in message. Defaults to None.

    Returns:
        str: Text after command or empty string.
    """
    if isinstance(message, Message):
        text = message.text or message.caption
        args = text.split(maxsplit=1)[1] if len(text.split()) > 1 else ""

        if use_reply and not args:
            args = message.reply_to_message.text or message.reply_to_message.caption

    elif not isinstance(message, str):
        return ""

    return args or ""


def get_args(
    message: Union[Message, str], use_reply: bool = None
) -> Tuple[List[str], Dict[str, str]]:
    """Returns list of common args and a dictionary with named args.

    Args:
        message (Union[Message, str]): Message or text.

        use_reply (bool, optional): Try to get args from reply message if no args in message. Defaults to None.

    Returns:
        List[str]: List of args.
    """
    raw_args = get_args_raw(message, use_reply)

    try:
        args = list(filter(lambda x: len(x) > 0, shlex.split(raw_args)))
    except ValueError:
        return [raw_args], {}

    common_args = []
    named_args = {}

    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("-"):
            if i + 1 < len(args) and (
                not args[i + 1].startswith("-") or len(args[i + 1].split()) > 1
            ):
                named_args[arg] = args[i + 1]
                i += 2
            else:
                i += 1
        else:
            i += 1
        common_args.append(arg)
    return common_args, named_args


class ScheduleJob:
    def __init__(
        self,
        func: callable,
        trigger: Optional[Union[CronTrigger, IntervalTrigger]] = IntervalTrigger(seconds=3600),
        *args,
        **kwargs,
    ):
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.id = func.__name__
        self.trigger = trigger


def get_ram_usage() -> float:
    """Returns current process tree memory usage in MB"""
    try:
        import psutil

        current_process = psutil.Process(os.getpid())
        mem = current_process.memory_info()[0] / 2.0**20
        for child in current_process.children(recursive=True):
            mem += child.memory_info()[0] / 2.0**20

        return round(mem, 1)
    except Exception:
        return 0


def get_cpu_usage() -> float:
    """Returns current process tree CPU usage in %"""
    try:
        import psutil

        current_process = psutil.Process(os.getpid())
        cpu = current_process.cpu_percent()
        for child in current_process.children(recursive=True):
            cpu += child.cpu_percent()

        return round(cpu, 1)
    except Exception:
        return 0


def get_full_name(obj: Union[User, Chat]) -> str:
    if isinstance(obj, Chat):
        if obj.type == ChatType.PRIVATE:
            return f"{obj.first_name} {obj.last_name}" if obj.last_name else obj.first_name
        return obj.title
    elif isinstance(obj, User):
        return f"{obj.first_name} {obj.last_name}" if obj.last_name else obj.first_name
    else:
        raise TypeError("obj must be User or Chat")

def with_reply(func):
    async def wrapped(client: Client, message: Message):
        if not message.reply_to_message:
            await message.reply("<b>Reply Ke pesan</b>")
        else:
            return await func(client, message)

    return wrapped

def with_args(text: str):
    def decorator(func):
        async def wrapped(client: Client, message: Message):
            if message.text and len(message.text.split()) == 1:
                await message.edit(text)
            else:
                return await func(client, message)

        return wrapped

    return decorator

def with_premium(func):
    async def wrapped(client: Client, message: Message):
        if not (await client.get_me()).is_premium:
            await message.reply("<b>Lo Bukan Pake Akun Premimum</b>")
        else:
            return await func(client, message)

    return wrapped


def get_text(message: Message) -> None | str:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


async def progress(current, total, message, start, type_of_ps, file_name=None):
    """Progress Bar For Showing Progress While Uploading / Downloading File - Normal"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = f"{''.join(['▰' for i in range(math.floor(percentage / 10))])}"
        progress_str += (
            f"{''.join(['▱' for i in range(10 - math.floor(percentage / 10))])}"
            )
        progress_str += f"{round(percentage, 2)}%\n"
        tmp = f"{progress_str}{humanbytes(current)} of {humanbytes(total)}\n"
        tmp += f"ETA: {time_formatter(estimated_total_time)}"
        if file_name:
            try:
                await message.edit(
                    f"{type_of_ps}\n**File Name:** `{file_name}`\n{tmp}",
                    parse_mode=enums.ParseMode.MARKDOWN,
                    )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit(
                    f"{type_of_ps}\n{tmp}", parse_mode=enums.ParseMode.MARKDOWN
                    )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


async def run_cmd(prefix: str) -> Tuple[str, str, int, int]:
    """Run Commands"""
    args = shlex.split(prefix)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
        )


def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m


async def edit_or_reply(message, txt):
    """Edit Message If Its From Self, Else Reply To Message"""
    if not message:
        return await message.reply(txt)
    if not message.from_user:
        return await message.reply(txt)
    return await message.reply(txt)


def text(message: Message) -> str:
    """Find text in `Message` object"""
    return message.text if message.text else message.caption


def restart() -> None:
    music_bot_pid = db.get("custom.musicbot", "music_bot_pid", None)
    if music_bot_pid is not None:
        try:
            music_bot_process = psutil.Process(music_bot_pid)
            music_bot_process.terminate()
        except psutil.NoSuchProcess:
            print("Music bot is not running.")
    os.execvp(sys.executable, [sys.executable, "erbanget.py"])


def format_exc(e: Exception, suffix="") -> str:
    traceback.print_exc()
    err = traceback.format_exc()
    if isinstance(e, errors.RPCError):
        return (
            f"<blockquote><b>Telegram API error!</b>\n"
            f"<code>[{e.CODE} {e.ID or e.NAME}] — {e.MESSAGE.format(value=e.value)}</code>\n\n<b>{suffix}</b></blockquote>"
            )
    return f"<blockquote><b>Error!</b>\n" f"<code>{err}</code></blockquote>"


def with_reply(func):
    async def wrapped(client: Client, message: Message):
        if not message.reply_to_message:
            await message.reply("<b>Reply to message is required</b>")
        else:
            return await func(client, message)

    return wrapped


async def interact_with(message: Message) -> Message:
    """
    Check history with bot and return bot's response

    Example:
    .. code-block:: python
        bot_msg = await interact_with(await bot.send_message("@BotFather", "/start"))
    :param message: already sent message to bot
    :return: bot's response
    """

    await asyncio.sleep(1)
    # noinspection PyProtectedMember
    response = [
        msg async for msg in message._client.get_chat_history(message.chat.id, limit=1)
        ]
    seconds_waiting = 0

    while response[0].from_user.is_self:
        seconds_waiting += 1
        if seconds_waiting >= 5:
            raise RuntimeError("bot didn't answer in 5 seconds")

        await asyncio.sleep(1)
        # noinspection PyProtectedMember
        response = [
            msg
            async for msg in message._client.get_chat_history(message.chat.id, limit=1)
        ]

    interact_with_to_delete.append(message.id)
    interact_with_to_delete.append(response[0].id)

    return response[0]


def split_list(input_list, n):
    """
    Takes a list and splits it into smaller lists of n elements each.
    :param input_list:
    :param n:
    :return:
    """
    n = max(1, n)
    return [input_list[i : i + n] for i in range(0, len(input_list), n)]

def format_module_help(module_name: str, full=True):
    commands = plugins_help[module_name]

    help_text = (
        f"<b>Bantuan untuk |{module_name}|\n\nPenggunaan:</b>\n" if full else "<b>Penggunaan:</b>\n"
        )

    for command, desc in commands.items():
        cmd = command.split(maxsplit=1)
        args = " <code>" + cmd[1] + "</code>" if len(cmd) > 1 else ""
        help_text += f"<code>{prefix}{cmd[0]}</code>{args} — <i>{desc}</i>\n"

    return help_text


def format_small_module_help(module_name: str, full=True):
    commands = plugins_help[module_name]

    help_text = (
        f"<b>Help for</b> |{module_name}|\n\nCommands list:\n"
        if full
        else "<b>Commands list:</b>\n"
        )
    for command, _desc in commands.items():
        cmd = command.split(maxsplit=1)
        args = " <code>" + cmd[1] + "</code>" if len(cmd) > 1 else ""
        help_text += f"<code>{prefix}{cmd[0]}</code>{args}\n"
    help_text += f"\n<b>Get full usage: <code>{prefix}help {module_name}</code></b>"

    return help_text


def import_library(library_name: str, package_name: str = None):
    """
    Loads a library, or installs it in ImportError case
    :param library_name: library name (import example...)
    :param package_name: package name in PyPi (pip install example)
    :return: loaded module
    """
    if package_name is None:
        package_name = library_name
    requirements_list.append(package_name)

    try:
        return importlib.import_module(library_name)
    except ImportError as exc:
        completed = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", package_name], check=True)
        if completed.returncode != 0:
            raise AssertionError(
                f"Failed to install library {package_name} (pip exited with code {completed.returncode})"
                ) from exc
        return importlib.import_module(library_name)


def uninstall_library(package_name: str):
    """
    Uninstalls a library
    :param package_name: package name in PyPi (pip uninstall example)
    """
    completed = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", package_name], check=True)
    if completed.returncode != 0:
        raise AssertionError(
            f"Failed to uninstall library {package_name} (pip exited with code {completed.returncode})"
        )


def resize_image(
    input_img, output=None, img_type="PNG", size: int = 512, size2: int = None
):
    if output is None:
        output = BytesIO()
        output.name = f"sticker.{img_type.lower()}"

    with Image.open(input_img) as img:
        # We used to use thumbnail(size) here, but it returns with a *max* dimension of 512,512
        # rather than making one side exactly 512, so we have to calculate dimensions manually :(
        if size2 is not None:
            size = (size, size2)
        elif img.width == img.height:
            size = (size, size)
        elif img.width < img.height:
            size = (max(size * img.width // img.height, 1), size)
        else:
            size = (size, max(size * img.height // img.width, 1))

        img.resize(size).save(output, img_type)

    return output


def resize_new_image(image_path, output_path, desired_width=None, desired_height=None):
    """
    Resize an image to the desired dimensions while maintaining the aspect ratio.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the resized image.
        desired_width (int, optional): Desired width in pixels. If not provided, the aspect ratio will be maintained.
        desired_height (int, optional): Desired height in pixels. If not provided, the aspect ratio will be maintained.
    """
    image = Image.open(image_path)

    width, height = image.size

    aspect_ratio = width / height

    if desired_width and desired_height:
        new_width, new_height = desired_width, desired_height
    elif desired_height:
        new_width, new_height = int(desired_height * aspect_ratio), desired_height
    else:
        new_width, new_height = 150, 150

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    resized_image.save(output_path)
    if os.path.exists(image_path):
        os.remove(image_path)


async def load_module(
    module_name: str,
    client: Client,
    message: Message = None,
    core=False,
) -> ModuleType:
    if module_name in plugins_help and not core:
        await unload_module(module_name, client)

    path = f"plugins.{'custom_module.' if not core else ''}{module_name}"

    with open(f"{path.replace('.', '/')}.py", encoding="utf-8") as f:
        code = f.read()
    meta = parse_meta_comments(code)

    packages = meta.get("requires", "").split()
    requirements_list.extend(packages)

    try:
        module = importlib.import_module(path)
    except ImportError as e:
        if core:
            # Core modules shouldn't raise ImportError
            raise

        if not packages:
            raise

        if message:
            await message.edit(f"<b>Installing requirements: {' '.join(packages)}</b>")

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            *packages,
        )
        try:
            await asyncio.wait_for(proc.wait(), timeout=120)
        except asyncio.TimeoutError:
            if message:
                await message.edit(
                    "<b>Timeout while installed requirements."
                    + "Try to install them manually</b>"
                    )
            raise TimeoutError("timeout while installing requirements") from e

        if proc.returncode != 0:
            if message:
                await message.edit(
                    f"<b>Failed to install requirements (pip exited with code {proc.returncode}). "
                    f"Check logs for futher info</b>",
                    )
            raise RuntimeError("failed to install requirements") from e

        module = importlib.import_plugins(path)

    for _name, obj in vars(module).items():
        if isinstance(getattr(obj, "handlers", []), list):
            for handler, group in getattr(obj, "handlers", []):
                client.add_handler(handler, group)

    module.__meta__ = meta

    return module


async def unload_module(module_name: str, client: Client) -> bool:
    path = "modules.custom_plugins." + module_name
    if path not in sys.modules:
        return False

    module = importlib.import_module(path)

    for _name, obj in vars(module).items():
        for handler, group in getattr(obj, "handlers", []):
            client.remove_handler(handler, group)

    del plugins_help[module_name]
    del sys.modules[path]

    return True


def parse_meta_comments(code: str) -> Dict[str, str]:
    try:
        groups = META_COMMENTS.search(code).groups()
    except AttributeError:
        return {}

    return {groups[i]: groups[i + 1] for i in range(0, len(groups), 2)}


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id
