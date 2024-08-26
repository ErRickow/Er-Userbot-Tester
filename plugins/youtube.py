# code by @xtdevs
# without cookies

import os
import time

import requests
from pyrogram.types import Message
from yt_dlp import YoutubeDL


@ErRick(
    ~filters.scheduled
    & filters.command(["yta"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def youtube_download(link: str, only_audio=False):
    url = "https://randydev-ryuzaki-api.hf.space/akeno/youtube"
    payload = {
        "link": link,
        "only_audio": only_audio
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return None
    response_data = response.json()
    request_check = response_data["randydev"]["video_data"] or response_data["randydev"]["audio_data"]
    title = response_data["randydev"]["title"]
    views = response_data["randydev"]["views"]
    # ....
    return request_check, title, views 

# TODO
video, title, views = youtube_download(link)
if not video:
    #return
# .....
  video_bytes.name = "video.mp4"
  await message.reply_video(
    video_bytes,
    caption="example json",
    duration="example json",
    thumb="example json",
    progress=progress, # need progress
    progress_args=(
        "processing",
        "example json",
        "uploading video",
    ),
)
