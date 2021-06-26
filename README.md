# ass-hack
Save telegram self-destruct photos and videos

## Requirements
1. Python 3.x
2. Modules:
   ```pip3 install pyrogram tgcrypto```
   
## Starting
### 1. Create private channel
You can edit it what you would like
### 2. Get channel id
Just send invite link _t.me/joinchat/..._ to [@username_to_id_bot](t.me/username_to_id_bot) and get id starts with -100
### 3. API id and hash
Login at www.my.telegram.org, choose "API development tool" and get your ```api_id``` and ```api_hash```
### 4. Config
Create ```config.py``` in the same directory as the ```main.py``` with text:
```
session_name = "example"
api_id = 1234567
api_hash = "example000example000"
channel_id = -1001234567890
```
Where ```session_name``` is any text. But if you will use other userbot, ```session_name``` must be other too, otherwise you wil get an error
### 5. Run!
Run ```main.py``` before you receive self-destruct photo/video and script will post it to your private channel automatically
