from pyrogram import Client, filters
import time
import os
from config import session_name, api_id, api_hash, channel_id

app = Client(session_name, api_id, api_hash)


@app.on_message((filters.photo | filters.video) & filters.private & ~filters.me)
def ttl_download(_, msg):
    full_name = msg.from_user.first_name
    if msg.from_user.last_name:
        full_name += " " + msg.from_user.last_name

    if hasattr(msg.photo, "ttl_seconds"):
        if msg.photo.ttl_seconds:
            app.download_media(msg, "photo.jpg")
            mention = f"[{full_name}](tg://user?id={msg.from_user.id}), " \
                      f"{time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(msg.date))}, {msg.photo.ttl_seconds}s"
            with open("downloads/photo.jpg", "rb") as photo:
                app.send_photo(channel_id, photo, mention)
            os.remove(os.path.join("downloads", "photo.jpg"))

    if hasattr(msg.video, "ttl_seconds"):
        if msg.video.ttl_seconds:
            app.download_media(msg, "video.mp4")
            mention = f"[{full_name}](tg://user?id={msg.from_user.id}), " \
                      f"{time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(msg.date))}, {msg.video.ttl_seconds}s"
            with open("downloads/video.mp4", "rb") as video:
                app.send_video(channel_id, video, mention)
            os.remove(os.path.join("downloads", "video.mp4"))


app.run()
