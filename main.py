from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified, MessageIdInvalid
from time import sleep, strftime, gmtime, time
from os import remove
from os.path import join
from random import randint
import config

app = Client(config.session_name, config.api_id, config.api_hash)


async def msg_info(msg):
    media_type = ""
    ttl = 0
    if hasattr(msg.photo, "ttl_seconds"):
        if msg.photo.ttl_seconds:
            media_type = "photo"
            ttl = msg.photo.ttl_seconds
    elif hasattr(msg.video, "ttl_seconds"):
        if msg.video.ttl_seconds:
            media_type = "video"
            ttl = msg.video.ttl_seconds

    if media_type:
        full_name = msg.from_user.first_name + (f' {msg.from_user.last_name}'
                                                if msg.from_user.last_name else '')
        sender = f"[{full_name}](tg://user?id={msg.from_user.id})"
        sending_time = f"{strftime('%x %X', gmtime(msg.date))}"
        return sender, media_type, sending_time, ttl
    else:
        return None, None, None, None


async def save_media(msg, sender, media_type, sending_time, ttl):
    try:
        mes = await app.send_message(config.channel_id, f"{sender} sent {media_type}, {sending_time}, {ttl}s"
                                                        f"\n__Uploading...__")
        file_type = ("jpg" if media_type == "photo" else "mp4")
        file_name = f"{msg.from_user.id}{time()*10000000}{randint(1, 10000000)}.{file_type}"
        await app.download_media(msg, file_name)
        mention = f"{sender}, {sending_time}, {ttl}s"
        with open(join("downloads", file_name), "rb") as att:
            if media_type == "photo":
                await app.send_photo(config.channel_id, att, mention)
            elif media_type == "video":
                await app.send_video(config.channel_id, att, mention)
        remove(join("downloads", file_name))
        await mes.delete()
    except FloodWait as e:
        sleep(e.x)
    except MessageIdInvalid:
        pass


@app.on_message(filters.command(["ass-hack", "asshack", "ah"], prefixes="!") & filters.me & ~filters.edited)
async def on_command(_, msg):
    try:
        if msg.text in ("!ass-hack", "!asshack", "!ah"):
            msg = await msg.edit(f"```{msg.text.markdown}```\n**Searching for self-destructing media...**")
            success = False
            my_id = (await app.get_me()).id
            dialogs = await app.get_dialogs()
            for dialog in dialogs:
                if dialog.chat.type == "private" and dialog.chat.id != my_id:
                    for mes in await app.get_history(dialog.chat.id, limit=config.last_messages_amount):
                        sender, media_type, sending_time, ttl = await msg_info(mes)
                        if sender:
                            success = True
                            msg = await msg.edit(f"{msg.text.markdown}\n￫ {sender} sent {media_type}, {sending_time}, {ttl}s")
                            await save_media(mes, sender, media_type, sending_time, ttl)

            if not success:
                await msg.edit(f"{msg.text.markdown}\n**Nobody sent something :c**")
            else:
                await msg.edit(f"{msg.text.markdown}\n**Done!**")

    except FloodWait as e:
        sleep(e.x)
    except MessageIdInvalid:
        pass


@app.on_message(filters.private & ~filters.me & (filters.photo | filters.video))
async def in_background(_, msg):
    try:
        sender, media_type, sending_time, ttl = await msg_info(msg)
        if sender:
            await save_media(msg, sender, media_type, sending_time, ttl)
    except FloodWait as e:
        sleep(e.x)
    except MessageIdInvalid:
        pass


app.run()
