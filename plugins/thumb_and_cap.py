#========================================================================
# Don't Remove Credit Tg - @TDBotDevZ
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on Telegram https://t.me/TDBotDevZ
#========================================================================
# imports
from pyrogram import Client, filters 
from helper.database import digital_botz

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    td = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    if len(message.command) == 1:
       return await td.edit("**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__\n\nExᴀᴍᴩʟᴇ:- `/set_caption {filename}\n\n💾 Sɪᴢᴇ: {filesize}\n\n⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}\n\bBy: @TDBotDevZ`**")
    caption = message.text.split(" ", 1)[1]
    await digital_botz.set_caption(message.from_user.id, caption=caption)
    await td.edit("__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__")
   
@Client.on_message(filters.private & filters.command(['del_caption', 'delete_caption', 'delcaption']))
async def delete_caption(client, message):
    td = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if not caption:
       return await td.edit("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")
    await digital_botz.set_caption(message.from_user.id, caption=None)
    await td.edit("__**❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ**__")
                                       
@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    td = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if caption:
       await td.edit(f"**Yᴏᴜ'ʀᴇ Cᴀᴩᴛɪᴏɴ:-**\n\n`{caption}`")
    else:
       await td.edit("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):
    td = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
        await td.delete()
    else:
        await td.edit("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__")
		
@Client.on_message(filters.private & filters.command(['del_thumb', 'delete_thumb', 'delthumb']))
async def removethumb(client, message):
    td = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await digital_botz.set_thumbnail(message.from_user.id, file_id=None)
        await td.edit("❌️ __**Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ**__")
        return
    await td.edit("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__")


@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    td = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    await digital_botz.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await td.edit("✅️ __**Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ**__")

