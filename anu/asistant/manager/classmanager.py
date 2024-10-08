import time
import logging
import platform

from requests.exceptions import ConnectionError
from main import Config
from telegraph import Telegraph
from pyrogram import __version__ as pyrogram_version
from anu.asistant.auah import Methods



class ClassManager(Config, Methods):
    # versions /
    python_version = str(platform.python_version())
    pyrogram_version = str(pyrogram_version)

    # assistant /
    assistant_name = "Chi"
    assistant_version = "v.0.0.0"

    # userbot /
    userbot_name = "Er"
    userbot_version = "v.0.0.1"

    # containers /
    CMD_HELP = {}

    # owner details /
    owner_name = "Er"
    owner_id = #1790546938
    owner_username = "@chakszzz"

    # other /
    message_ids = {}
    PIC = "https://telegra.ph/file/38eec8a079706b8c19eae.mp4"
    Repo = "https://pornhub.com"
    StartTime = time.time()
    utube_object = object
    callback_user = None
    whisper_ids = {}

    # debugging /


    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.session.internals.msg_id").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.dispatcher").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.connection.connection").setLevel(logging.WARNING)
    log = logging.getLogger()

    # telegraph /
    try:
        telegraph = Telegraph()
        telegraph.create_account(short_name=Config.TL_NAME or "Er Userbot")
    except (ConnectionError, AttributeError):
        telegraph = None

