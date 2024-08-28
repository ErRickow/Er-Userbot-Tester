from sys import version_info
from .db import db
import git

import pathlib
from time import perf_counter

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

__all__ = [
    "plugins_help",
    "tolong_anu",
    "requirements_list",
    "python_version",
    "prefix",
    "emopong",
    "gitrepo",
    "userbot_version"
    "ignore_eval",
    "asupan_username",
    "ErRick",
]


plugins_help = {}
tolong_anu = {}
requirements_list = []
ignore_eval = []
ErRick = Client.on_message

app = {}

python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"

asupan_username = db.get("core.main", "asupan_username", " ")
emopong = db.get("core.main", "emopong", "❍")
alive_logo = db.get("core.main", "alive_logo", " ")
alive_text = db.get("core.main", "alive_text", " ")
emoji = db.get("core.main", "emoji", " ")

prefix = db.get("core.main", "prefix", ".")

async def input_user(message: Message) -> str:
    """Get the input from the user"""
    if len(message.command) < 2:
        output = ""
    else:
        try:
            output = message.text.split(" ", 1)[1].strip() or ""
        except IndexError:
            output = ""
    return output


try:
    gitrepo = git.Repo(".")
except git.exc.InvalidGitRepositoryError:
    repo = git.Repo.init()
    origin = repo.create_remote(
        "origin", "https://github.com/ErRickow/Er-Userbot-Tester"
    )
    origin.fetch()
    repo.create_head("main", origin.refs.main)
    repo.heads.main.set_tracking_branch(origin.refs.main)
    repo.heads.main.checkout(True)
    gitrepo = git.Repo(".")

if len(gitrepo.tags) > 0:
    commits_since_tag = list(gitrepo.iter_commits(f"{gitrepo.tags[-1].name}..HEAD"))
else:
    commits_since_tag = []
userbot_version = f"0.1.{len(commits_since_tag)}"
