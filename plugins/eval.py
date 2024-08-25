import asyncio
import io
import os
import re
import subprocess
import sys
import traceback
from asyncio import sleep
from contextlib import suppress
from io import BytesIO, StringIO
from random import randint
from typing import Optional

from pyrogram import Client
from pyrogram import Client as app
from pyrogram import Client as ren
from pyrogram import *
from pyrogram.raw import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.raw.functions.phone import CreateGroupCall as call
from pyrogram.raw.functions.phone import DiscardGroupCall
from pyrogram.raw.types import *
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import *

from utils.handler import *
from utils.tools import *
from utils.misc import plugins_help, prefix

@Client.on_message(filters.command("ev", prefix) & filters.me)