# ass-hack
Save telegram self-destruct photos and videos.

## Requirements
0. Linux/Mac/Windows
1. Python 3.8+
   
Tested on Ubuntu 23.04, Python 3.11.

## Getting started
Create and fill in the `.env` file:

```
API_ID=
API_HASH=''
SESSION_NAME='example'
SESSION_STRING=

# The number of recent messages in chats, which will be processed when working by command. Default 20.
LAST_MESSAGES_AMOUNT=20

# The maximum size of files (in bytes) that will be loaded into RAM.
# This speeds up sending files, but increases RAM consumption.
# Default 10 MiB. Always used for photos.
MAX_FILE_SIZE_FOR_IN_MEMORY_DOWNLOADS='10240'

```

1. `api_id` and `api_hash` - get it on my.telegram.org.
2. `session_name` - is any text. But if you will use other userbot, `session_name` must be other too, otherwise you will get an error
3. `session_string` - just leave it as is.

```
git clone https://github.com/Laktionof/ass-hack
cd ass-hack
pip install -r requirements.txt
python main.py
```

Then login into your Telegram account.

Run it before you receive self-destruct photo/video. ~~But if you run it after receiving self-desctruct media, just send message `!ass-hack`/`!ah` to any chat.~~
