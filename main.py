from pyrogram import Client, filters
from time import sleep, strftime, gmtime, time
from os import remove
from os.path import join
from config import *

app = Client(session_name, api_id, api_hash)


@app.on_message(filters.private & ~filters.me & (filters.photo | filters.video))
def ttl_download(_, msg):
    att_type = 2  # 0 - photo, 1 - video
    filetype = ("jpg", "mp4")
    if hasattr(msg.photo, "ttl_seconds"):
        if msg.photo.ttl_seconds:
            att_type = 0
    elif hasattr(msg.video, "ttl_seconds"):
        if msg.video.ttl_seconds:
            att_type = 1

    if att_type != 2:
        full_name = msg.from_user.first_name
        if msg.from_user.last_name:
            full_name += " " + msg.from_user.last_name

        file_name = f"{time()}.{filetype[att_type]}"
        app.download_media(msg, file_name)
        mention = f"[{full_name}](tg://user?id={msg.from_user.id}), " \
                  f"{strftime('%d.%m.%Y %H:%M:%S', gmtime(msg.date))}, {msg.photo.ttl_seconds}s"
        with open(join("downloads", file_name), "rb") as att:
            if att_type == 0:
                app.send_photo(channel_id, att, mention)
            elif att_type == 1:
                app.send_video(channel_id, att, mention)
        remove(join("downloads", file_name))


app.run()
