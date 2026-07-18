#========================================================================
# Don't Remove Credit Tg - @TDBotDevZ
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on Telegram https://t.me/TDBotDevZ
#========================================================================
import re, os, time
id_pattern = re.compile(r'^\d+$')

class Config(object):
    API_ID = int(os.environ.get("API_ID", "34822566")) # Teligram Api id : https://youtu.be/L5DDah6WhIM
    API_HASH = os.environ.get("API_HASH", "3ab7815d50c6baec0e564742eee75b33") #Teligram Api hash : https://youtu.be/L5DDah6WhIM
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8847134520:AAFc6DAGL0YmTZVTYoRbOhFB5zeth7ERF-E") #Teligram Bot Token: https://youtu.be/tqV2jH5YWFY
    BOT = None

    # premium account string session required 😢 
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    
    # database config
    DB_NAME = os.environ.get("DB_NAME","thilakff007") # Mango db name & db Url: https://youtu.be/Cp_p9DtrWAw
    DB_URL = os.environ.get("DB_URL","mongodb+srv://thilakff007:0U8T4Aiaoqmje2UD@shadow.vetq4tn.mongodb.net/?appName=Shadow")
 
    # other configs
    TD_PIC = os.environ.get("TD_PIC", os.environ.get("START_PIC", "https://files.catbox.moe/hu611s.jpg"))
    START_PIC = TD_PIC
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '7731989008').split()]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003580590124"))

    # upload limits config
    FREE_UPLOAD_LIMIT = 2147483648      # Free Users (2 GiB)
    PRO_UPLOAD_LIMIT = 2147483648       # Pro Users (2 GiB)
    ULTRAPRO_UPLOAD_LIMIT = 4294967296  # UltraPro Users (4 GiB)
    OWNER_UPLOAD_LIMIT = 6442450944     # Owner/Admin (6 GiB)

    BOT_COMMANDS = [
        ("start", "𝖈ʜᴇᴄᴋ 𝖎 𝖆ᴍ ʟɪᴠᴇ."),
        ("plans", "ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ."),
        ("myplan", "ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ʜᴇʀᴇ."),
        ("view_thumb", "𝖙ᴏ 𝖘ᴇᴇ 𝖞ᴏᴜʀ 𝖈ᴜ𝖘ᴛᴏᴍ 𝖙ʜᴜᴍʙɴᴀɪʟ !!"),
        ("del_thumb", "𝖙ᴏ 𝖉ᴇʟᴇᴛᴇ 𝖞ᴏᴜʀ 𝖈ᴜ𝖘ᴛᴏᴍ 𝖙ʜᴜᴍʙɴᴀɪʟ !!"),
        ("set_caption", "Sᴇᴛ A Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ !!"),
        ("see_caption", "Sᴇᴇ Yᴏᴜʀ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ !!"),
        ("del_caption", "Dᴇʟᴇᴛᴇ Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ !!"),
        ("metadata", "Tᴏ Sᴇᴛ & Cʜᴀɴɢᴇ ʏᴏᴜʀ ᴍᴇᴛᴀᴅᴀᴛᴀ ᴄᴏᴅᴇ"),
        ("set_prefix", "Tᴏ Sᴇᴛ Yᴏᴜʀ Pʀᴇғɪx !!"),
        ("see_prefix", "Tᴏ Sᴇᴇ Yᴏᴜʀ Pʀᴇғɪx !!"),
        ("del_prefix", "Dᴇʟᴇᴛᴇ Yᴏᴜʀ Pʀᴇғɪx !!"),
        ("set_suffix", "Tᴏ Sᴇᴛ Yᴏᴜʀ Sᴜғғɪx !!"),
        ("see_suffix", "Tᴏ Sᴇᴇ Yᴏᴜʀ Sᴜғғɪx !!"),
        ("del_suffix", "Dᴇʟᴇᴛᴇ Yᴏᴜʀ Sᴜғғɪx !!"),
        ("restart", "ᴛᴏ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴀʟʟ ᴅʙ ᴜsᴇʀs (Aᴅᴍɪɴ Oɴʟʏ)"),
        ("addpremium", "ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ (Aᴅᴍɪɴ Oɴʟʏ)"),
        ("remove_premium", "ʀᴇᴍᴏᴠᴇ ᴘʀᴇᴍɪᴜᴍ (Aᴅᴍɪɴ Oɴʟʏ)"),
        ("ban", "ban members using command (admin only)"),
        ("unban", "unban members using command (admin only)"),
        ("banned_users", "check bot all ban users using command (admin only)"),
        ("logs", "ᴄʜᴇᴄᴋ ʙᴏᴛ ʟᴏɢs (Aᴅᴍɪɴ Oɴʟʏ)"),
        ("status", "Cʜᴇᴄᴋ Bᴏᴛ Sᴛᴀᴛᴜs (Aᴅᴍɪɴ Oɴʟʏ)"),
        ("broadcast", "Sᴇɴᴅ Mᴇssᴀɢᴇ Tᴏ Aʟʟ Usᴇʀs (Aᴅᴍɪɴ Oɴʟʏ)")
    ]

    # premium mode feature ✅
    UPLOAD_LIMIT_MODE = True 
    PREMIUM_MODE = True 
    
    #force subs
    try:
        FORCE_SUB = int(os.environ.get("FORCE_SUB", "")) 
    except:
        FORCE_SUB = os.environ.get("FORCE_SUB", "TDBotDevZ")
        
    # wes response configuration     
    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()

class TD(object):
    # part of text configuration
    START_TXT = """<b>Ｈ𝙰𝙸, {}👋

𝚃ʜɪs 𝙸s 𝙰ɴ 𝙰ᴅᴠᴀᴄᴇᴅ 𝙰ɴᴅ 𝚈ᴇᴛ 𝙿ᴏᴡᴇʀғᴜʟ 𝚁ᴇɴᴀᴍᴇ 𝙱ᴏᴛ
𝚄sɪɴɢ 𝚃ʜɪs 𝙱ᴏᴛ 𝚈ᴏᴜ 𝙲ᴀɴ 𝚁ᴇɴᴀᴍᴇ & 𝙲ʜᴀɴɢᴇ 𝚃ʜᴜᴍʙɴᴀɪʟ 𝙾ғ 𝚈ᴏᴜʀ 𝙵ɪʟᴇ 
𝚈ᴏᴜ 𝙲ᴀɴ 𝙰ʟsᴏ 𝙲ᴏɴᴠᴇʀᴛ 𝚅ɪᴅᴇᴏ 𝚃ᴏ 𝙵ɪʟᴇ & 𝙵ɪʟᴇ 𝚃ᴏ 𝚅ɪᴅᴇᴏ
𝚃𝙷𝙸𝚂 𝙱𝙾𝚃 𝙰𝙻𝚂𝙾 𝚂𝚄𝙿𝙿𝙾𝚁𝚃𝚂 𝙲𝚄𝚂𝚃𝙾𝙼 𝚃𝙷𝚄𝙼𝙱𝙽𝙰𝙸𝙻 𝙰𝙽𝙳 𝙲𝚄𝚂𝚃𝙾𝙼 𝙲𝙰𝙿𝚃𝙸𝙾𝙽

Tʜɪs Bᴏᴛ Wᴀs Cʀᴇᴀᴛᴇᴅ Bʏ : @TDBotDevZ 💞</b>"""

    ABOUT_TXT = """<b>╭───────────⍟
├🤖 ᴍy ɴᴀᴍᴇ : {}
├🖥️ Dᴇᴠᴇʟᴏᴩᴇʀꜱ : {}
├👨‍💻 Pʀᴏɢʀᴀᴍᴇʀ : {}
├📕 Lɪʙʀᴀʀy : {}
├✏️ Lᴀɴɢᴜᴀɢᴇ: {}
├💾 Dᴀᴛᴀ Bᴀꜱᴇ: {}
├📊 ᴠᴇʀsɪᴏɴ: <a href=https://t.me/TDBotDevZ>{}</a></b>
╰───────────────⍟ """

    HELP_TXT = """
<b>•></b> /start Tʜᴇ Bᴏᴛ.

✏️ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
<b>•></b> Sᴇɴᴅ Aɴy Fɪʟᴇ Aɴᴅ Tyᴩᴇ Nᴇᴡ Fɪʟᴇ Nɴᴀᴍᴇ \nAɴᴅ Aᴇʟᴇᴄᴛ Tʜᴇ Fᴏʀᴍᴀᴛ [ document, video, audio ].           
ℹ️ 𝗔𝗻𝘆 𝗢𝘁𝗵𝗲𝗿 𝗛𝗲𝗹𝗽 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 :- <a href=https://t.me/TDBotDevZ>𝑺𝑼𝑷𝑷𝑶𝑹𝑻 𝑮𝑹𝑶𝑼𝑷</a>
"""

    UPGRADE_PREMIUM= """
•⪼ ★𝘗𝘭𝘢𝘯𝘴    -  ⏳𝘋𝘢𝘵𝘦 - 💸𝘗𝘳𝘪𝘤𝘦 
•⪼ 🥉𝘉𝘳𝘰𝘯𝘻𝘦  -   3𝘥𝘢𝘺𝘴 -   39
•⪼ 🥈𝘚𝘪𝘭𝘷𝘦𝘳   -   7𝘥𝘢𝘺𝘴 -   59
•⪼ 🥇𝘎𝘰𝘭𝘥    -  15𝘥𝘢𝘺𝘴 -  99
•⪼ 🏆𝘗𝘭𝘢𝘵𝘪𝘯𝘶𝘮 -  1𝘮𝘰𝘯𝘵𝘩 -  179
•⪼ 💎𝘋𝘪𝘢𝘮𝘰𝘯𝘥 -  2𝘮𝘰𝘯𝘵𝘩 -  339

- 𝘋𝘢𝘪𝘭𝘺 𝘜𝘱𝘭𝘰𝘢𝘥 𝘓𝘪𝘮𝘪𝘵 𝘜𝘯𝘭𝘪𝘮𝘪𝘵𝘦𝘥
- 𝘋𝘪𝘴𝘤𝘰𝘶𝘯𝘵 𝘈𝘭𝘭 𝘗𝘭𝘢𝘯 𝘙𝘴.9
    """
    
    UPGRADE_PLAN= """
𝘗𝘭𝘢𝘯: 𝘗𝘳𝘰
𝘋𝘢𝘵𝘦: 1 𝘮𝘰𝘯𝘵𝘩 
𝘗𝘳𝘪𝘤𝘦: 179
𝘓𝘪𝘮𝘪𝘵: 100 𝘎𝘉

𝘗𝘭𝘢𝘯: 𝘜𝘭𝘵𝘢 𝘗𝘳𝘰 
𝘋𝘢𝘵𝘦: 1 𝘮𝘰𝘯𝘵𝘩 
𝘗𝘳𝘪𝘤𝘦: 199
𝘓𝘪𝘮𝘪𝘵: 1000 𝘎𝘉

- 𝘋𝘪𝘴𝘤𝘰𝘶𝘯𝘵 𝘈𝘭𝘭 𝘗𝘭𝘢𝘯 𝘙𝘴.9
    """
    
    THUMBNAIL = """
🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>

<b>•></b> Sᴇɴᴅ Aɴy Pʜᴏᴛᴏ Tᴏ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟy Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /del_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Oʟᴅ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /view_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴɪʟᴇ.
"""
    CAPTION= """
📑 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>

<b>•></b> /set_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴛ ᴀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /see_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /del_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ

Exᴀᴍᴩʟᴇ:- `/set_caption 📕 Fɪʟᴇ Nᴀᴍᴇ: {filename}
💾 Sɪᴢᴇ: {filesize}
⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}`
"""
    BOT_STATUS = """
⚡️ ʙᴏᴛ sᴛᴀᴛᴜs ⚡️

⌚️ ʙᴏᴛ ᴜᴩᴛɪᴍᴇ: `{}`
👭 ᴛᴏᴛᴀʟ ᴜsᴇʀꜱ: `{}`
💸 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs: `{}`
֍ ᴜᴘʟᴏᴀᴅ: `{}`
⊙ ᴅᴏᴡɴʟᴏᴀᴅ: `{}`
"""
    LIVE_STATUS = """
⚡ ʟɪᴠᴇ sᴇʀᴠᴇʀ sᴛᴀᴛᴜs ⚡

ᴜᴘᴛɪᴍᴇ: `{}`
ᴄᴘᴜ: `{}%`
ʀᴀᴍ: `{}%` 
ᴛᴏᴛᴀʟ ᴅɪsᴋ: `{}`
ᴜsᴇᴅ sᴘᴀᴄᴇ: `{} {}%`
ғʀᴇᴇ sᴘᴀᴄᴇ: `{}`
ᴜᴘʟᴏᴀᴅ: `{}`
ᴅᴏᴡɴʟᴏᴀᴅ: `{}`
V𝟹.𝟶.𝟶 [STABLE]
"""
    DIGITAL_METADATA = """
❪ SET CUSTOM METADATA ❫

- /metadata - Tᴏ Sᴇᴛ & Cʜᴀɴɢᴇ ʏᴏᴜʀ ᴍᴇᴛᴀᴅᴀᴛᴀ ᴄᴏᴅᴇ

☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

`--change-title @TDBotDevZ
--change-video-title @TDBotDevZ
--change-audio-title @TDBotDevZ
--change-subtitle-title @TDBotDevZ
--change-author @TDBotDevZ`

📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛ. @TDBotDevZ
"""
    
    CUSTOM_FILE_NAME = """
<u>🖋️ Custom File Name</u>

you can pre-add a prefix and suffix along with your new filename

➢ /set_prefix - To add a prefix along with your _filename.
➢ /see_prefix - Tᴏ Sᴇᴇ Yᴏᴜʀ Pʀᴇғɪx !!
➢ /del_prefix - Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Pʀᴇғɪx !!
➢ /set_suffix - To add a suffix along with your filename_.
➢ /see_suffix - Tᴏ Sᴇᴇ Yᴏᴜʀ Sᴜғғɪx !!
➢ /del_suffix - Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Sᴜғғɪx !!

Exᴀᴍᴩʟᴇ:- `/set_suffix @TDBotDevZ`
Exᴀᴍᴩʟᴇ:- `/set_prefix @TDBotDevZ`
"""
    
    DEV_TXT = """<b><u>Sᴩᴇᴄɪᴀʟ Tʜᴀɴᴋꜱ & Dᴇᴠᴇʟᴏᴩᴇʀꜱ</b></u>
    
» 𝗦𝗢𝗨𝗥𝗖𝗘 𝗖𝗢𝗗𝗘 : <a href=https://t.me/TDBotDevZ>@TDBotDevZ</a>

• ❣️ <a href=https://t.me/TDBotDevZ>@TDBotDevZ</a> """

    SEND_METADATA = """
❪ SET CUSTOM METADATA ❫

☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

`--change-title @TDBotDevZ
--change-video-title @TDBotDevZ
--change-audio-title @TDBotDevZ
--change-subtitle-title @TDBotDevZ
--change-author @TDBotDevZ`

📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛ. @TDBotDevZ
"""
    
    TD_PROGRESS = """<b>
╭━━━━━━━━◉🚀◉━━━━━━━━╮
┃   𝗧𝗗 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚...❱━➣
┣━━━━━━━━━━━━━━━━━━━━╯
┣⪼ 📦 𝗦𝗜𝗭𝗘: {1} | {2}
┣⪼ 📊 𝗗𝗢𝗡𝗘: {0}%
┣⪼ 🚀 𝗦𝗣𝗘𝗘𝗗: {3}/s
┣⪼ ⏰ 𝗘𝗧𝗔: {4}
╰━━━━━━━━◉🔥◉━━━━━━━━╯</b>"""
    FILE_PROGRESS = TD_PROGRESS

td = TD()

#========================================================================
# Don't Remove Credit Tg - @TDBotDev
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on telegram https://t.me/TDBotDev
#========================================================================
