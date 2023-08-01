from os import getenv, remove
from os.path import join
from time import sleep
from datetime import timedelta
from dotenv import load_dotenv, set_key
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait, MessageIdInvalid

load_dotenv()

SESSION_NAME = getenv('SESSION_NAME')
API_ID = int(getenv('API_ID'))
API_HASH = getenv('API_HASH')
SESSION_STRING = getenv('SESSION_STRING')
LAST_MESSAGES_AMOUNT = int(getenv('LAST_MESSAGES_AMOUNT'))
MAX_FILE_SIZE_FOR_IN_MEMORY_DOWNLOADS = int(getenv('MAX_FILE_SIZE_FOR_IN_MEMORY_DOWNLOADS'))

if SESSION_STRING:
    app = Client(SESSION_NAME, API_ID, API_HASH, session_string=SESSION_STRING)
else:
    app = Client(SESSION_NAME, API_ID, API_HASH, in_memory=True)
    app.start()
    SESSION_STRING = app.export_session_string()
    set_key(".env", "SESSION_STRING", SESSION_STRING)
    app.stop()


def save_secret(msg, command_msg=None):
    work_chat_id = command_msg.chat.id if command_msg else "me"

    sender_name = msg.from_user.first_name + (" " + msg.from_user.last_name if msg.from_user.last_name else "")
    sender_name_link = f"[{sender_name}](tg://user?id={msg.from_user.id})"
    sending_date = msg.date.strftime("%Y-%m-%d %X")

    if msg.media == MessageMediaType.PHOTO:
        ttl = msg.photo.ttl_seconds
        attachment_size_KiB = round(msg.photo.file_size/1024, 2)
        tmp_info_msg = app.send_message(work_chat_id,
                                        f"{sender_name_link} sent a photo, {msg.photo.width}x{msg.photo.height}, " \
                                        f"{attachment_size_KiB} KiB, {ttl} s, {sending_date}\n__Uploading...__")
        
        caption = f"{sender_name_link}, {msg.photo.width}x{msg.photo.height}, {attachment_size_KiB} KiB, {ttl} s, {sending_date}"
        attachment = msg.download(in_memory=True)

        app.send_photo(work_chat_id, attachment, caption)

    elif msg.media == MessageMediaType.VIDEO:
        ttl = msg.video.ttl_seconds
        video_duration = timedelta(seconds=msg.video.duration)
        attachment_size_MiB = round(msg.video.file_size/1024/1024, 2)
        tmp_info_msg = app.send_message(work_chat_id,
                                        f"{sender_name_link} sent a video, {msg.video.width}x{msg.video.height}, " \
                                        f"{attachment_size_MiB} MiB, {video_duration}, {ttl} s, {sending_date} s\n__Uploading...__")

        caption = f"{sender_name_link}, {video_duration}, {msg.video.width}x{msg.video.height}, " \
                  f"{attachment_size_MiB} MiB, {ttl} s, {sending_date}"
        
        if msg.video.file_size <= MAX_FILE_SIZE_FOR_IN_MEMORY_DOWNLOADS:
            attachment = msg.download(in_memory=True)
            app.send_video(work_chat_id, attachment, caption)

        else:
            msg.download(msg.video.file_unique_id)
            with open(join("downloads", msg.video.file_unique_id), "rb") as attachment:
                app.send_video(work_chat_id, attachment, caption)

            remove(join("downloads", msg.video.file_unique_id))

    tmp_info_msg.delete()

    return True


@app.on_message(filters.command("ping", prefixes="!") & filters.me)
def ping_command(_, msg):
    try:
        print(msg.text)
        msg.edit(f"`{msg.text}`\n\n**🏓 pong**")

    except FloodWait as e:
        sleep(e.value)

    except MessageIdInvalid:
        pass


@app.on_message(filters.private & ~filters.me & (filters.photo | filters.video))
def ass_hack_background(_, msg):
    try:
        if msg.media == MessageMediaType.PHOTO:
            if msg.photo.ttl_seconds:
                save_secret(msg)

        elif msg.media == MessageMediaType.VIDEO:
            if msg.video.ttl_seconds:
                save_secret(msg)

    except FloodWait as e:
        sleep(e.value)

    except MessageIdInvalid:
        pass

print("Running!")
app.run()