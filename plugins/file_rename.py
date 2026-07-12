#========================================================================
# Don't Remove Credit Tg - @TDBotDevZ
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on Telegram https://t.me/TDBotDevZ
#========================================================================
# pyrogram imports
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

# hachoir imports
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# bots imports
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path
from helper.database import digital_botz
from helper.ffmpeg import change_metadata
from config import Config

# extra imports
from asyncio import sleep
import os, time, asyncio


UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""

app = Client("4gb_FileRenameBot", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION)


@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id  = message.from_user.id
    td_file = getattr(message, message.media.value)
    filename = td_file.file_name
    filesize = humanbytes(td_file.file_size)
    mime_type = td_file.mime_type
    dcid = FileId.decode(td_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    # Fetch user plan and limits dynamically
    plan_type, max_upload_size, expiry_time = await digital_botz.get_premium_plan_and_limit(user_id)
    if not client.premium:
        plan_type = "Free"

    # PREMIUM FEATURES SINGLE FILE SIZE CHECK
    if plan_type == "Pro":
        if td_file.file_size > 2 * 1024 * 1024 * 1024: # 2GB
            return await message.reply_text("⚠ Upgrade to UltraPro for files larger than 2GB.")
    elif plan_type == "UltraPro":
        if td_file.file_size > 4 * 1024 * 1024 * 1024: # 4GB
            return await message.reply_text("⚠ UltraPro supports files up to 4GB.")
    else: # Free user
        if td_file.file_size > 2 * 1024 * 1024 * 1024: # 2GB limit for free
            return await message.reply_text("⚠ Free plan only supports files up to 2GB. Please upgrade to Pro or UltraPro. /plans")

    if client.premium and client.uploadlimit and plan_type != "Free":
        await digital_botz.reset_uploadlimit_access(user_id)
        user_data = await digital_botz.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0) if user_data else max_upload_size
        used = user_data.get('used_limit', 0) if user_data else 0
        remain = int(limit) - int(used)
        used_percentage = (int(used) / int(limit) * 100) if int(limit) > 0 else 0
        if remain < int(td_file.file_size):
            return await message.reply_text(f"{used_percentage:.2f}% Of Daily Upload Limit {humanbytes(limit)}.\n\n Media Size: {filesize}\n Your Used Daily Limit {humanbytes(used)}\n\nYou have only **{humanbytes(remain)}** Data.\nPlease, Buy Premium Plan s.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪪 Uᴘɢʀᴀᴅᴇ", callback_data="plans")]]))
         
    if plan_type != "Free" and client.premium:
        if not Config.STRING_SESSION:
            if td_file.file_size > 2000 * 1024 * 1024:
                 return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ+")

        try:
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )       
            await asyncio.sleep(30)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )
        except Exception as e:
            print(f"Error in rename_start: {e}")
    else:
        try:
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )       
            await asyncio.sleep(30)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text(
                text=f"**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )
        except Exception as e:
            print(f"Error in rename_start (non-premium): {e}")


@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text 
        await message.delete() 
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        await reply_message.delete()

        button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ",callback_data = "upload#document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data = "upload#video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data = "upload#audio")])
        await message.reply(
            text=f"**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )

async def upload_files(bot, sender_id, upload_type, file_path, ph_path, caption, duration, td_processing):
    """
    Unified function to upload files based on type
    - Supports both 2GB and 4GB files
    - Uses same function for all file sizes
    - Handles document, video, and audio files
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"
            
        # Upload document files (2GB & 4GB)
        if upload_type == "document":
            filw = await bot.send_document(
                sender_id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, td_processing, time.time()))
        
        # Upload video files (2GB & 4GB)  
        elif upload_type == "video":
            filw = await bot.send_video(
                sender_id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, td_processing, time.time()))
        
        # Upload audio files (2GB & 4GB)
        elif upload_type == "audio":
            filw = await bot.send_audio(
                sender_id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, td_processing, time.time()))
        else:
            return None, f"Unknown upload type: {upload_type}"
        
        # Return uploaded file object
        return filw, None
        
    except Exception as e:
        # Return error if upload fails
        return None, str(e)


#@Client.on_callback_query(filters.regex("upload"))
async def upload_doc(bot, update):
    td_processing = await update.message.edit("`Processing...`")
    
    # Creating Directory for Metadata
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    user_id = int(update.message.chat.id) 
    new_name = update.message.text
    new_filename_ = new_name.split(":-")[1]
    user_data = await digital_botz.get_user_data(user_id)

    # Apply custom rename format if configured
    rename_format = user_data.get('rename_format', None)
    if rename_format:
        if "{filename}" in rename_format:
            new_filename_ = rename_format.format(filename=new_filename_)
        else:
            new_filename_ = f"{rename_format} {new_filename_}"

    try:
        # adding prefix and suffix
        prefix = user_data.get('prefix', None)
        suffix = user_data.get('suffix', None)
        new_filename = await add_prefix_suffix(new_filename_, prefix, suffix)
    except Exception as e:
        return await td_processing.edit(f"⚠️ Something went wrong can't able to set Prefix or Suffix ☹️ \n\n❄️ Contact My Creator -> @TDBotDevZ\nError: {e}")

    # msg file location 
    file = update.message.reply_to_message
    media = getattr(file, file.media.value)
    
    # File paths for download and metadata
    file_path = f"Renames/{new_filename}"
    metadata_path = f"Metadata/{new_filename}"

    await td_processing.edit("`Try To Download....`")
    if bot.premium and bot.uploadlimit:
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)        
        total_used = int(used) + int(media.file_size)
        await digital_botz.set_used_limit(user_id, total_used)
    
    try:            
        dl_path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(DOWNLOAD_TEXT, td_processing, time.time()))
    except Exception as e:
        if bot.premium and bot.uploadlimit:
            used_remove = int(used) - int(media.file_size)
            await digital_botz.set_used_limit(user_id, used_remove)
        return await td_processing.edit(f"Download Error: {e}")

    metadata_mode = await digital_botz.get_metadata_mode(user_id)
    if metadata_mode:        
        metadata = await digital_botz.get_metadata_code(user_id)
        if metadata:
            await td_processing.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")
            if await change_metadata(dl_path, metadata_path, metadata):            
                await td_processing.edit("Metadata Added.....")
                print("Metadata Added.....")
            else:
                await td_processing.edit("Failed to add metadata, uploading original file...")
                metadata_mode = False
        else:
            await td_processing.edit("No metadata found, uploading original file...")
            metadata_mode = False
    else:
        await td_processing.edit("`Try To Uploading....`")
        
    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata and metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if parser:
            parser.close()
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        pass
        
    ph_path = None
    c_caption = user_data.get('caption', None)
    c_thumb = user_data.get('file_id', None)

    if c_caption:
         try:
             # adding custom caption 
             caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
         except Exception as e:
             if bot.premium and bot.uploadlimit:
                 used_remove = int(used) - int(media.file_size)
                 await digital_botz.set_used_limit(user_id, used_remove)
             return await td_processing.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
         caption = f"**{new_filename}**"
 
    if (media.thumbs or c_thumb):
         # downloading thumbnail path
         try:
             if c_thumb:
                 ph_path = await bot.download_media(c_thumb) 
             else:
                 ph_path = await bot.download_media(media.thumbs[0].file_id)
             
             if ph_path and os.path.exists(ph_path):
                 Image.open(ph_path).convert("RGB").save(ph_path)
                 img = Image.open(ph_path)
                 img.resize((320, 320))
                 img.save(ph_path, "JPEG")
         except Exception as e:
             print(f"Error processing thumbnail: {e}")
             ph_path = None

    upload_type = update.data.split("#")[1]
    # Integrate user-configured upload_mode or file_mode if set
    pref_mode = user_data.get('upload_mode') or user_data.get('file_mode')
    if pref_mode and pref_mode in ["document", "video", "audio"]:
        upload_type = pref_mode
    
    # Use the correct file path based on metadata mode
    final_file_path = metadata_path if metadata_mode and os.path.exists(metadata_path) else file_path
    
    if media.file_size > 2000 * 1024 * 1024:
        # Upload file using unified function for large files
        filw, error = await upload_files(
            app, Config.LOG_CHANNEL, upload_type, final_file_path, 
            ph_path, caption, duration, td_processing
        )

        if error:
            if bot.premium and bot.uploadlimit:
                used_remove = int(used) - int(media.file_size)
                await digital_botz.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await td_processing.edit(f"Upload Error: {error}")

        
        from_chat = filw.chat.id
        mg_id = filw.id
        await asyncio.sleep(2)
        await bot.copy_message(update.from_user.id, from_chat, mg_id)
        await bot.delete_messages(from_chat, mg_id)
        
    else:
        # Upload file using unified function for regular files
        filw, error = await upload_files(
            bot, update.message.chat.id, upload_type, final_file_path, 
            ph_path, caption, duration, td_processing
        )
                   
        if error:
            if bot.premium and bot.uploadlimit:
                used_remove = int(used) - int(media.file_size)
                await digital_botz.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await td_processing.edit(f"Upload Error: {error}")

    # Clean up files
    await remove_path(ph_path, file_path, dl_path, metadata_path)
    return await td_processing.edit("Uploaded Successfully....")



