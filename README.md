# ass-hack
Save telegram self-destruct photos and videos

## Requirements
0. Linux/Mac/Windows
1. Python 3.6+
2. Modules: `pip install pyrogram tgcrypto` (or `pip3 install pyrogram tgcrypto`)
   
Tested on Ubuntu 21.04, Python 3.9.5 and PyPy 7.3.5 with GCC 10.3.0 (Python 3.7)
   
## Starting
### 1. Create private channel
You can edit it what you would like
### 2. Get channel id
Just send invite link _t.me/joinchat/..._ to [@username_to_id_bot](https://t.me/username_to_id_bot) and get id starts with -100
### 3. API id and API hash
Login at my.telegram.org, choose "API development tool" and get your `api_id` and `api_hash`
### 4. Config
Fill in the `config.py`:
1. `session_name` is any text. But if you will use other userbot, `session_name` must be other too, otherwise you will get an error
2. `api_id` and `api_hash` - you already have it
3. `channel_id` - id of channel-storage for media, starts with -100
4. `last_message_amount` - after command `!ass-hack` script will check the last X messages in the last 100 private chats, looking for self-destruct media
### 5. Run!
```
cd /path/to/script/ass-hack
python3 main.py
```
Run it before you receive self-destruct photo/video, and script will post it to your private channel automatically. But if you run it after receiving self-desctruct media, just send message `!ass-hack` to any chat
