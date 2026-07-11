#========================================================================
# Don't Remove Credit Tg - @TDBotDevZ
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on Telegram https://t.me/TDBotDevZ
#========================================================================

import os
import re
import datetime
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified

try:
    from pyrogram.errors import ListenerTimeout
except ImportError:
    try:
        from pyromod.exceptions import ListenerTimeout
    except ImportError:
        import asyncio
        ListenerTimeout = asyncio.TimeoutError
from helper.database import digital_botz
from config import Config

logger = logging.getLogger(__name__)

# Non-configurable keys in the user document
NON_SETTING_KEYS = {
    "_id", "join_date", "used_limit", "daily", "expiry_time",
    "has_free_trial", "ban_status", "usertype", "uploadlimit"
}

def extract_commands_from_filter(filt):
    commands = []
    if filt is None:
        return commands
    if hasattr(filt, "commands"):
        commands.extend(list(filt.commands))
    if hasattr(filt, "lhs"):
        commands.extend(extract_commands_from_filter(filt.lhs))
    if hasattr(filt, "rhs"):
        commands.extend(extract_commands_from_filter(filt.rhs))
    if hasattr(filt, "base"):
        commands.extend(extract_commands_from_filter(filt.base))
    return commands

def is_admin_filter(filt):
    if filt is None:
        return False
    class_name = filt.__class__.__name__
    if "User" in class_name or "user" in class_name.lower():
        return True
    if hasattr(filt, "lhs"):
        if is_admin_filter(filt.lhs): return True
    if hasattr(filt, "rhs"):
        if is_admin_filter(filt.rhs): return True
    if hasattr(filt, "base"):
        if is_admin_filter(filt.base): return True
    return False

def discover_bot_features(client):
    """
    Dynamically discover all registered commands, callbacks and system settings
    """
    user_cmds = set()
    admin_cmds = set()

    # Traverse through all registered pyrogram message handlers
    for group in client.dispatcher.groups.values():
        for handler in group:
            # We can import MessageHandler dynamically to avoid issues
            from pyrogram.handlers import MessageHandler, CallbackQueryHandler
            if isinstance(handler, MessageHandler):
                cmds = extract_commands_from_filter(handler.filters)
                if cmds:
                    if is_admin_filter(handler.filters):
                        admin_cmds.update(cmds)
                    else:
                        user_cmds.update(cmds)

    return sorted(list(user_cmds)), sorted(list(admin_cmds))

@Client.on_message(filters.private & filters.command("settings"))
async def open_settings_panel(client: Client, message: Message):
    user_id = message.from_user.id
    await show_settings_main(client, message.chat.id, user_id, is_callback=False)

async def show_settings_main(client: Client, chat_id, user_id, is_callback=True, query: CallbackQuery = None):
    # Fetch all keys from the database schema template for users
    default_doc = digital_botz.new_user(user_id)
    user_settings = [k for k in default_doc.keys() if k not in NON_SETTING_KEYS]

    # Get user's current settings from database
    user_data = await digital_botz.get_user_data(user_id)
    if not user_data:
        # If user not in DB, add them
        await digital_botz.add_user(client, query)
        user_data = default_doc

    text = "⚙️ **Dynamic Settings Menu**\n\nConfigure your custom options dynamically below:"

    keyboard = []

    # Generate user settings buttons dynamically
    for key in user_settings:
        val = user_data.get(key, None)
        display_name = key.replace("_", " ").title()

        # Determine value display
        if isinstance(val, bool):
            status = "🟢 ON" if val else "🔴 OFF"
            btn_text = f"{display_name}: {status}"
            cb_data = f"set_toggle#{key}#{'0' if val else '1'}"
        elif key == "file_id":
            # Thumbnail key
            status = "🌌 SET" if val else "❌ NOT SET"
            btn_text = f"Thumbnail: {status}"
            cb_data = f"set_text#{key}"
        else:
            status = f"`{val}`" if val is not None else "❌ NOT SET"
            # Crop very long values for display in buttons
            val_str = str(val)[:15] + "..." if (val and len(str(val)) > 15) else str(val)
            status_display = f" {val_str}" if val is not None else " ❌"
            btn_text = f"{display_name}:{status_display}"
            cb_data = f"set_text#{key}"

        keyboard.append([InlineKeyboardButton(btn_text, callback_data=cb_data)])

    # Check if user is Admin and add Global Settings Option
    if user_id in Config.ADMIN:
        keyboard.append([InlineKeyboardButton("👑 Admin Global Settings", callback_data="settings_admin")])

    # Add System info and Dynamic Features explorer button
    keyboard.append([InlineKeyboardButton("🔍 Auto-Detected Bot Features", callback_data="settings_features")])
    keyboard.append([InlineKeyboardButton("🔒 Close", callback_data="close")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if is_callback and query:
        try:
            await query.message.edit_text(text, reply_markup=reply_markup)
        except MessageNotModified:
            pass
    else:
        await client.send_message(chat_id, text, reply_markup=reply_markup)

@Client.on_callback_query(filters.regex("^set_toggle#"))
async def handle_toggle_settings(client: Client, query: CallbackQuery):
    _, key, next_val = query.data.split("#")
    user_id = query.from_user.id
    bool_val = next_val == "1"

    await digital_botz.set_user_setting(user_id, key, bool_val)
    await query.answer(f"{key.replace('_', ' ').title()} turned {'ON' if bool_val else 'OFF'}", show_alert=True)
    await show_settings_main(client, query.message.chat.id, user_id, is_callback=True, query=query)

@Client.on_callback_query(filters.regex("^set_text#"))
async def handle_text_settings(client: Client, query: CallbackQuery):
    _, key = query.data.split("#")
    user_id = query.from_user.id
    display_name = key.replace("_", " ").title()

    # Provide special guidance based on setting key
    if key == "file_id":
        prompt_text = "🌌 **Please send a photo to set your custom thumbnail.**"
    elif key == "metadata_code":
        prompt_text = (
            "❪ SET CUSTOM METADATA ❫\n\n"
            "☞ For Example:\n\n"
            "`--change-title @TDBotDevZ\n"
            "--change-video-title @TDBotDevZ\n"
            "--change-audio-title @TDBotDevZ\n"
            "--change-subtitle-title @TDBotDevZ\n"
            "--change-author @TDBotDevZ`"
        )
    elif key == "caption":
        prompt_text = (
            "📑 **Please enter your custom caption format.**\n\n"
            "Example:\n`/set_caption 📕 File Name: {filename}\n💾 Size: {filesize}\n⏰ Duration: {duration}`"
        )
    elif key == "file_mode":
        prompt_text = "📝 **Please enter your preferred file mode (e.g., `document`, `video`, `audio`):**"
    elif key == "upload_mode":
        prompt_text = "📝 **Please enter your preferred upload mode (e.g., `video`, `document`, `audio`):**"
    elif key == "rename_format":
        prompt_text = "🖋️ **Please enter your custom rename format template (e.g., `[MyBot] {filename}`):**"
    else:
        prompt_text = f"🖋️ **Please enter the new value for {display_name}:**"

    # We add options to either set a new value or delete current value
    keyboard = [
        [InlineKeyboardButton("❌ Clear / Delete Current Value", callback_data=f"clear_val#{key}")],
        [InlineKeyboardButton("◀️ Back", callback_data="settings_back")]
    ]

    await query.message.edit_text(
        f"{prompt_text}\n\nWaiting for your input (Timeout: 60s)...",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    try:
        # If setting thumbnail, accept a photo. Otherwise accept text.
        filt = filters.photo if key == "file_id" else filters.text
        response = await client.ask(
            chat_id=query.message.chat.id,
            text=f"Please reply with the value or file:",
            filters=filt,
            timeout=60
        )

        # Process the input
        if key == "file_id":
            # Save file ID of photo
            await digital_botz.set_thumbnail(user_id, response.photo.file_id)
            success_text = "🌌 **Custom thumbnail saved successfully!**"
        else:
            await digital_botz.set_user_setting(user_id, key, response.text)
            success_text = f"✅ **{display_name} saved successfully as:**\n`{response.text}`"

        await client.send_message(query.message.chat.id, success_text)

    except ListenerTimeout:
        await client.send_message(
            query.message.chat.id,
            f"⚠️ **Timeout!**\n\nYou did not respond in time to configure {display_name}. Please try again."
        )
    except Exception as e:
        logger.error(f"Error in handle_text_settings: {e}")

    # Return to settings menu
    await show_settings_main(client, query.message.chat.id, user_id, is_callback=False)

@Client.on_callback_query(filters.regex("^clear_val#"))
async def handle_clear_val(client: Client, query: CallbackQuery):
    _, key = query.data.split("#")
    user_id = query.from_user.id
    display_name = key.replace("_", " ").title()

    if key == "file_id":
        await digital_botz.set_thumbnail(user_id, None)
    else:
        await digital_botz.set_user_setting(user_id, key, None)

    await query.answer(f"Cleared {display_name} successfully ✅", show_alert=True)
    await show_settings_main(client, query.message.chat.id, user_id, is_callback=True, query=query)

@Client.on_callback_query(filters.regex("^settings_back$"))
async def handle_back_settings(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    await show_settings_main(client, query.message.chat.id, user_id, is_callback=True, query=query)

@Client.on_callback_query(filters.regex("^settings_features$"))
async def show_detected_features(client: Client, query: CallbackQuery):
    user_cmds, admin_cmds = discover_bot_features(client)

    text = (
        "🔍 **Dynamic Feature Registry (Auto-Detected)**\n\n"
        "Here are all commands and callback interfaces currently detected on this bot:\n\n"
        f"👤 **User Commands ({len(user_cmds)}):**\n"
        + ", ".join([f"`/{c}`" for c in user_cmds]) + "\n\n"
        f"👑 **Admin Commands ({len(admin_cmds)}):**\n"
        + ", ".join([f"`/{c}`" for c in admin_cmds]) + "\n\n"
        "💡 _Any newly added plugins, handlers or parameters will automatically register in this system without any manual code changes!_"
    )

    keyboard = [[InlineKeyboardButton("◀️ Back", callback_data="settings_back")]]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

@Client.on_callback_query(filters.regex("^settings_admin$"))
async def show_admin_settings(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in Config.ADMIN:
        return await query.answer("Access Denied ❌ Only admins can access global configurations.", show_alert=True)

    text = "👑 **Admin Global Settings Panel**\n\nConfigure bot-wide features dynamically stored in memory/database:"

    # Build list of configurable fields in Config dynamically
    global_options = [
        ("Premium Mode Mode", "PREMIUM_MODE", Config.PREMIUM_MODE),
        ("Upload Limit Mode", "UPLOAD_LIMIT_MODE", Config.UPLOAD_LIMIT_MODE)
    ]

    keyboard = []
    for display_name, attr, val in global_options:
        status = "🟢 ON" if val else "🔴 OFF"
        keyboard.append([InlineKeyboardButton(
            f"{display_name}: {status}",
            callback_data=f"toggle_admin_opt#{attr}#{'0' if val else '1'}"
        )])

    keyboard.append([InlineKeyboardButton("◀️ Back", callback_data="settings_back")])
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

@Client.on_callback_query(filters.regex("^toggle_admin_opt#"))
async def handle_toggle_admin_option(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in Config.ADMIN:
        return await query.answer("Access Denied ❌", show_alert=True)

    _, attr, next_val = query.data.split("#")
    bool_val = next_val == "1"

    # Update Config option in memory
    setattr(Config, attr, bool_val)
    # If the Client instance has attributes like premium/uploadlimit, sync them as well
    if attr == "PREMIUM_MODE":
        client.premium = bool_val
    elif attr == "UPLOAD_LIMIT_MODE":
        client.uploadlimit = bool_val

    await query.answer(f"Global {attr} set to {'ON' if bool_val else 'OFF'} ✅", show_alert=True)
    await show_admin_settings(client, query)
