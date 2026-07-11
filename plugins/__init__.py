#========================================================================
# Don't Remove Credit Tg - @TDBotDevZ
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on Telegram https://t.me/TDBotDevZ
#========================================================================
__name__ = "Rename-Bot"
__version__ = "3.1.0"
__license__ = " Apache License, Version 2.0"
__copyright__ = "Copyright (C) 2022-present @TDBotDevZ <https://t.me/TDBotDevZ>"
__programer__ = "<a href=https://t.me/TDBotDevZ>@TDBotDevZ</a>"
__library__ = "<a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>"
__language__ = "<a href=https://www.python.org/>Pyᴛʜᴏɴ 3</a>"
__database__ = "<a href=https://cloud.mongodb.com/>Mᴏɴɢᴏ DB</a>"
__developer__ = "<a href=https://t.me/TDBotDevZ>@TDBotDevZ</a>"
__maindeveloper__ = "<a href=https://t.me/TDBotDevZ>@TDBotDevZ</a>"

# main copyright herders (©️)
# I have been working on this repo since 2022


# main working files 
# - bot.py
# - web_support.py
# - plugins/
# - start_&_cb.py
# - Force_Sub.py
# - admin_panel.py
# - file_rename.py
# - metadata.py
# - prefix_&_suffix.py
# - thumb_&_cap.py
# - config.py
# - utils.py
# - database.py

# bot run files
# - bot.py
# - Procfile
# - Dockerfile
# - requirements.txt
# - runtime.txt

from plugins.force_sub import not_subscribed, forces_sub, handle_banned_user_status
from pyrogram import Client, filters

@Client.on_message(filters.private)
async def _(bot, message):
    await handle_banned_user_status(bot, message)
    
@Client.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub_handler(bot, message):
    await forces_sub(bot, message)
