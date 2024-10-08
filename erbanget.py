import os
import logging

import sqlite3
import platform
import subprocess
from pathlib import Path

from pyrogram import Client, idle, errors
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.raw.functions.account import GetAuthorizations, DeleteAccount

from utils import config
from utils.db import db
from utils.misc import gitrepo, userbot_version
from utils.anu import restart, load_module

script_path = os.path.dirname(os.path.realpath(__file__))
if script_path != os.getcwd():
    os.chdir(script_path)

common_params = {
    "api_id": config.api_id,
    "api_hash": config.api_hash,
    "hide_password": True,
    "workdir": script_path,
    "app_version": userbot_version,
    "device_model": f"ErUserbotBeta@ {gitrepo.head.commit.hexsha[:7]}",
    "system_version": platform.version() + " " + platform.machine(),
    "sleep_threshold": 30,
    "test_mode": config.test_server,
    "parse_mode": ParseMode.HTML,
}

if config.STRINGSESSION:
    common_params["session_string"] = config.STRINGSESSION

app = Client("akun_ku", **common_params)


async def erbanget():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("moonlogs.txt"), logging.StreamHandler()],
        level=logging.INFO,
        )
    DeleteAccount.__new__ = None

    try:
        await app.start()
    except sqlite3.OperationalError as e:
        if str(e) == "database is locked" and os.name == "posix":
            logging.warning(
                "Session file is locked. Trying to kill blocking process..."
            )
            subprocess.run(["fuser", "-k", "akun_ku.session"], check=True)
            restart()
        raise
    except (errors.NotAcceptable, errors.Unauthorized) as e:
        logging.error(
            f"{e.__class__.__name__}: {e}\nMoving session file to akun_ku.session-old..."
            )
        os.rename("./akun_ku.session", "./akun_ku.session-old")
        restart()

    success_modules = 0
    failed_modules = 0

    for path in Path("plugins").rglob("*.py"):
        try:
            await load_module(
                path.stem, app, core="custom_plugins" not in path.parent.parts
            )
        except Exception:
            logging.warning("Kaga bisa import %s", path.stem, exc_info=True)
            failed_modules += 1
        else:
            success_modules += 1

    logging.info("Imported %s plugins", success_modules)
    if failed_modules:
        logging.warning("Gagal untuk import %s plugins", failed_modules)

    if info := db.get("core.updater", "restart_info"):
        text = {
            "restart": "<blockquote>Restart Selesai Sayangkuh!</blockquote>",
            "update": "<blockquote>Proses Update Sukses Sayangku!</blockquote>",
        }[info["type"]]
        try:
            await app.edit_message_text(
                info["chat_id"], info["message_id"], text
            )
        except errors.RPCError:
            pass
        db.remove("core.updater", "restart_info")

    # required for sessionkiller module
    if db.get("core.sessionkiller", "enabled", False):
        db.set(
            "core.sessionkiller",
            "auths_hashes",
            [
                auth.hash
                for auth in (
                    await app.invoke(GetAuthorizations())
                ).authorizations
            ],
        )

    logging.info("Er Userbot Beta started!")

    await idle()

    await app.stop()


if __name__ == "__main__":
    app.run(erbanget())
