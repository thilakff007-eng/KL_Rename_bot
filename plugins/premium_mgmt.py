#========================================================================
# Don't Remove Credit Tg - @TDBotDevZ
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on Telegram https://t.me/TDBotDevZ
#========================================================================

import re
import time
import logging
import asyncio
import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors import ListenerTimeout, MessageNotModified

from config import Config, td
from helper.database import digital_botz
from helper.utils import humanbytes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
PRO_MAX_SIZE = 2147483648       # 2GB
ULTRAPRO_MAX_SIZE = 4294967296  # 4GB

# Default daily limit fallback (100GB for Pro, 1000GB for UltraPro)
PRO_DAILY_LIMIT = 107374182400
ULTRAPRO_DAILY_LIMIT = 1073741824000

# ==========================================
# UTILITY PARSERS
# ==========================================
def parse_duration(duration_str: str):
    """
    Parses dynamic duration strings such as:
    1m, 30m, 1h, 12h, 1d, 7d, 30d, 1mon, 3mon, 6mon, 1y, 2y
    Returns: tuple of (seconds, parsed_formatted_string) or None
    """
    duration_str = duration_str.strip().lower()
    mapping = {
        "m": 60,
        "h": 3600,
        "d": 86400,
        "mon": 86400 * 30,
        "y": 86400 * 365,
    }

    # regex match number + unit
    match = re.match(r"^(\d+)\s*(mon|y|d|h|m)$", duration_str)
    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if value <= 0:
        return None

    seconds = value * mapping[unit]

    # Beautiful display text
    unit_display = {
        "m": "Minute" if value == 1 else "Minutes",
        "h": "Hour" if value == 1 else "Hours",
        "d": "Day" if value == 1 else "Days",
        "mon": "Month" if value == 1 else "Months",
        "y": "Year" if value == 1 else "Years"
    }
    return seconds, f"{value} {unit_display[unit]}"

# ==========================================
# CONVERSATION STATE CONTROLLER
# ==========================================
@Client.on_message(filters.command(["addpremium", "add_premium"]) & filters.user(Config.ADMIN))
async def cmd_add_premium(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("💡 **Usage:** `/addpremium <user_id>`")

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❌ **Invalid User ID format. Please use integers.**")

    await add_premium_flow(client, message, user_id)


async def add_premium_flow(client: Client, message: Message, user_id: int):
    # STEP 1: Ask for Duration
    prompt_msg = await message.reply_text(
        f"👤 **User ID:** `{user_id}`\n\n"
        "⏳ **Enter Premium Duration**\n\n"
        "**Supported Formats:**\n"
        "• `1m` = 1 Minute\n"
        "• `30m` = 30 Minutes\n"
        "• `1h` = 1 Hour\n"
        "• `12h` = 12 Hours\n"
        "• `1d` = 1 Day\n"
        "• `7d` = 7 Days\n"
        "• `30d` = 30 Days\n"
        "• `1mon` = 1 Month\n"
        "• `3mon` = 3 Months\n"
        "• `6mon` = 6 Months\n"
        "• `1y` = 1 Year\n"
        "• `2y` = 2 Years\n\n"
        "**Send duration string now:**",
        reply_markup=ForceReply(True)
    )

    try:
        duration_response = await client.ask(
            chat_id=message.chat.id,
            text="Waiting for valid duration format...",
            filters=filters.text,
            timeout=60
        )
    except ListenerTimeout:
        return await message.reply_text("⏳ **Request timed out.** Re-run /addpremium to try again.")

    parsed = parse_duration(duration_response.text)
    while parsed is None:
        await message.reply_text(
            "❌ **Invalid Duration format!** Please choose a supported option (e.g. `30d` or `1mon`)."
        )
        try:
            duration_response = await client.ask(
                chat_id=message.chat.id,
                text="Please send duration format now:",
                filters=filters.text,
                timeout=60
            )
            parsed = parse_duration(duration_response.text)
        except ListenerTimeout:
            return await message.reply_text("⏳ **Request timed out.**")

    seconds, duration_str = parsed

    # STEP 2: Ask for Plan selection
    plan_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔵 Pro Plan", callback_data=f"addprem_plan#{user_id}#{seconds}#{duration_str}#Pro"),
            InlineKeyboardButton("🟣 UltraPro Plan", callback_data=f"addprem_plan#{user_id}#{seconds}#{duration_str}#UltraPro")
        ],
        [
            InlineKeyboardButton("❌ Cancel", callback_data="close")
        ]
    ])

    await message.reply_text(
        f"⏳ **Duration:** `{duration_str}`\n\n"
        "📦 **Select Premium Plan type:**",
        reply_markup=plan_keyboard
    )


# ==========================================
# CALLBACK HANDLER FOR PLAN SELECTION
# ==========================================
@Client.on_callback_query(filters.regex("^addprem_plan#"))
async def cb_add_premium_save(client: Client, query: CallbackQuery):
    _, user_id_str, seconds_str, duration_str, plan_type = query.data.split("#")
    user_id = int(user_id_str)
    seconds = int(seconds_str)

    # Calculate limits & dates
    start_time = datetime.datetime.now()
    expiry_time = start_time + datetime.timedelta(seconds=seconds)

    if plan_type == "Pro":
        max_upload_size = PRO_MAX_SIZE
        daily_limit = PRO_DAILY_LIMIT
    else:
        max_upload_size = ULTRAPRO_MAX_SIZE
        daily_limit = ULTRAPRO_DAILY_LIMIT

    # Prepare Mongo Record
    premium_data = {
        "id": user_id,
        "plan_type": plan_type,
        "duration": duration_str,
        "start_time": start_time,
        "expiry_time": expiry_time,
        "max_upload_size": max_upload_size,
        "created_by": query.from_user.id
    }

    # Save to MongoDB
    await digital_botz.add_premium(user_id, premium_data, limit=daily_limit, type=plan_type)

    # Format Expire text
    ist = pytz.timezone("Asia/Kolkata")
    expiry_ist = expiry_time.astimezone(ist)
    expiry_str = expiry_ist.strftime("%d %b %Y %H:%M")

    # Send success response to Admin
    try:
        user_mention = (await client.get_users(user_id)).mention
    except Exception:
        user_mention = f"User (`{user_id}`)"

    success_text = (
        "✅ **Premium Added Successfully**\n\n"
        f"👤 **User:** {user_mention}\n"
        f"⚡ **User ID:** `{user_id}`\n"
        f"💎 **Plan:** `{plan_type}`\n"
        f"⏳ **Duration:** `{duration_str}`\n"
        f"📅 **Expires:** `{expiry_str} IST`\n"
        f"📂 **Upload Limit:** `{humanbytes(max_upload_size)}`"
    )

    await query.message.edit_text(success_text)

    # Send Notification to User
    try:
        await client.send_message(
            chat_id=user_id,
            text=(
                "👋 **Hey! Thank you for purchasing premium!** 🎉✨\n\n"
                f"💎 **Plan:** `{plan_type}`\n"
                f"⏳ **Duration:** `{duration_str}`\n"
                f"📅 **Expires:** `{expiry_str} IST`\n"
                f"📂 **Single Upload Size:** `{humanbytes(max_upload_size)}`\n\n"
                "Enjoy premium limits and fast processing! Check with /myplan"
            )
        )
    except Exception as e:
        logger.error(f"Could not notify user {user_id}: {e}")


# ==========================================
# REMOVE PREMIUM CONTROLLER
# ==========================================
@Client.on_message(filters.command(["removepremium", "remove_premium"]) & filters.user(Config.ADMIN))
async def cmd_remove_premium(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("💡 **Usage:** `/removepremium <user_id>`")

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❌ **Invalid User ID format.**")

    await remove_premium_flow(client, message, user_id)


async def remove_premium_flow(client: Client, message: Message, user_id: int):
    # Ask Confirmation
    confirm_kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ YES", callback_data=f"remprem_conf#{user_id}#yes"),
            InlineKeyboardButton("❌ NO", callback_data=f"remprem_conf#{user_id}#no")
        ]
    ])
    await message.reply_text(
        f"⚠️ **Remove Premium for user `{user_id}`?**",
        reply_markup=confirm_kb
    )


@Client.on_callback_query(filters.regex("^remprem_conf#"))
async def cb_remove_premium_confirm(client: Client, query: CallbackQuery):
    _, user_id_str, choice = query.data.split("#")
    user_id = int(user_id_str)

    if choice == "yes":
        if await digital_botz.has_premium_access(user_id):
            await digital_botz.remove_premium(user_id)
            await query.message.edit_text(f"✅ **Premium plan successfully removed for user `{user_id}`.**")
            try:
                await client.send_message(
                    chat_id=user_id,
                    text="<b>👋 Hey, your premium status has been revoked/removed by admin. Check /myplan</b>"
                )
            except Exception:
                pass
        else:
            await query.message.edit_text("❌ **User is not an active premium user.**")
    else:
        await query.message.edit_text("❌ **Premium revocation cancelled.**")


# ==========================================
# PREMIUM INFO & LIST
# ==========================================
@Client.on_message(filters.command("premiuminfo") & filters.user(Config.ADMIN))
async def cmd_premium_info(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("💡 **Usage:** `/premiuminfo <user_id>`")

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❌ **Invalid User ID.**")

    plan, max_upload, expiry = await digital_botz.get_premium_plan_and_limit(user_id)
    if plan == "Free":
        return await message.reply_text("❌ **User does not have an active premium plan.**")

    # Fetch extra start date
    user_data = await digital_botz.get_user(user_id)
    start_date = user_data.get("start_time") if user_data else None

    # Calculate remaining
    remaining_time = "Expired"
    status = "Expired 🔴"
    if expiry:
        delta = expiry - datetime.datetime.now()
        if delta.total_seconds() > 0:
            remaining_time = f"{delta.days}d {delta.seconds // 3600}h"
            status = "Active 🟢"
    else:
        remaining_time = "N/A"
        status = "Active (Lifetime) 🟢"

    start_str = start_date.strftime("%d %b %Y %H:%M") if start_date else "N/A"
    expiry_str = expiry.strftime("%d %b %Y %H:%M") if expiry else "N/A"

    info_text = (
        "👤 **Premium User Profile Info**\n\n"
        f"⚡ **User ID:** `{user_id}`\n"
        f"💎 **Plan:** `{plan}`\n"
        f"📅 **Start Date:** `{start_str}`\n"
        f"📆 **Expiry Date:** `{expiry_str}`\n"
        f"⏳ **Remaining Time:** `{remaining_time}`\n"
        f"📂 **Upload Limit:** `{humanbytes(max_upload)}`\n"
        f"📊 **Premium Status:** {status}"
    )
    await message.reply_text(info_text)


@Client.on_message(filters.command("premiumlist") & filters.user(Config.ADMIN))
async def cmd_premium_list(client: Client, message: Message):
    now = datetime.datetime.now()
    pro_count = await digital_botz.premium.count_documents({"plan_type": "Pro", "expiry_time": {"$gt": now}})
    ultra_count = await digital_botz.premium.count_documents({"plan_type": "UltraPro", "expiry_time": {"$gt": now}})
    expired_count = await digital_botz.premium.count_documents({"expiry_time": {"$lte": now}})
    active_count = await digital_botz.premium.count_documents({"expiry_time": {"$gt": now}})

    list_text = (
        "📊 **Premium Active Users list Summary**\n\n"
        f"🔵 **Total Pro Plan Users:** `{pro_count}`\n"
        f"🟣 **Total UltraPro Users:** `{ultra_count}`\n"
        f"🟢 **Total Active Users:** `{active_count}`\n"
        f"🔴 **Total Expired Users:** `{expired_count}`"
    )
    await message.reply_text(list_text)


# ==========================================
# INTERACTIVE PREMIUM ADMIN CONTROL MENU
# ==========================================
@Client.on_message(filters.command(["premium", "premiummenu"]) & filters.user(Config.ADMIN))
async def cmd_premium_menu_dashboard(client: Client, message: Message):
    await show_premium_menu(client, message.chat.id, is_callback=False)


async def show_premium_menu(client: Client, chat_id, is_callback=True, query: CallbackQuery = None):
    now = datetime.datetime.now()
    pro_count = await digital_botz.premium.count_documents({"plan_type": "Pro", "expiry_time": {"$gt": now}})
    ultra_count = await digital_botz.premium.count_documents({"plan_type": "UltraPro", "expiry_time": {"$gt": now}})
    active_count = await digital_botz.premium.count_documents({"expiry_time": {"$gt": now}})

    text = (
        "💎 **Modern Premium Admin Control Panel** 💎\n\n"
        "Configure plan limits, add new users, and view statistics dynamically.\n\n"
        f"🟢 **Active Subscriptions:** `{active_count}`\n"
        f"🔵 **Pro Plans:** `{pro_count}`\n"
        f"🟣 **UltraPro Plans:** `{ultra_count}`"
    )

    keyboard = [
        [
            InlineKeyboardButton("➕ Add Premium", callback_data="admin_add_prem"),
            InlineKeyboardButton("➖ Remove Premium", callback_data="admin_rem_prem")
        ],
        [
            InlineKeyboardButton("👤 Premium Info", callback_data="admin_info_prem"),
            InlineKeyboardButton("📋 Premium Users", callback_data="admin_list_users")
        ],
        [
            InlineKeyboardButton("📊 Premium Stats", callback_data="admin_stats_prem"),
            InlineKeyboardButton("🔄 Refresh", callback_data="admin_refresh_prem")
        ],
        [
            InlineKeyboardButton("❌ Close Panel", callback_data="close")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if is_callback and query:
        try:
            await query.message.edit_text(text, reply_markup=reply_markup)
        except MessageNotModified:
            pass
    else:
        await client.send_message(chat_id, text, reply_markup=reply_markup)


@Client.on_callback_query(filters.regex("^admin_"))
async def cb_admin_panel_dispatcher(client: Client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if user_id not in Config.ADMIN:
        return await query.answer("Access Denied ❌", show_alert=True)

    if data == "admin_refresh_prem":
        await query.answer("Refreshed stats!")
        return await show_premium_menu(client, query.message.chat.id, is_callback=True, query=query)

    elif data == "admin_stats_prem":
        now = datetime.datetime.now()
        pro_count = await digital_botz.premium.count_documents({"plan_type": "Pro", "expiry_time": {"$gt": now}})
        ultra_count = await digital_botz.premium.count_documents({"plan_type": "UltraPro", "expiry_time": {"$gt": now}})
        expired_count = await digital_botz.premium.count_documents({"expiry_time": {"$lte": now}})
        active_count = await digital_botz.premium.count_documents({"expiry_time": {"$gt": now}})

        stats_text = (
            "📊 **Detailed Premium Statistics**\n\n"
            f"🔵 **Pro Subscriptions:** `{pro_count}`\n"
            f"🟣 **UltraPro Subscriptions:** `{ultra_count}`\n"
            f"🟢 **Active Subscriptions:** `{active_count}`\n"
            f"🔴 **Expired Subscriptions:** `{expired_count}`\n\n"
            "Press Back to return to Dashboard."
        )
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="admin_back_prem")]])
        await query.message.edit_text(stats_text, reply_markup=back_kb)

    elif data == "admin_back_prem":
        return await show_premium_menu(client, query.message.chat.id, is_callback=True, query=query)

    elif data == "admin_list_users":
        now = datetime.datetime.now()
        users_cursor = digital_botz.premium.find({"expiry_time": {"$gt": now}}).limit(50)
        users_list = []
        async for u in users_cursor:
            uid = u.get("id")
            ptype = u.get("plan_type", "Pro")
            exp = u.get("expiry_time")
            exp_str = exp.strftime("%d %b %Y") if exp else "N/A"
            users_list.append(f"• `{uid}` ({ptype}) - Exp: `{exp_str}`")

        if not users_list:
            display_text = "📋 **No active premium users found.**"
        else:
            display_text = "📋 **Premium Users (Top 50 Active):**\n\n" + "\n".join(users_list)

        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="admin_back_prem")]])
        await query.message.edit_text(display_text, reply_markup=back_kb)

    elif data == "admin_add_prem":
        await query.message.delete()
        try:
            target_response = await client.ask(
                chat_id=query.message.chat.id,
                text="👤 **Please send/reply with the target User ID:**",
                filters=filters.text,
                timeout=60
            )
            target_id = int(target_response.text)
            await add_premium_flow(client, query.message, target_id)
        except ListenerTimeout:
            await client.send_message(query.message.chat.id, "⏳ **Request timed out.**")
        except ValueError:
            await client.send_message(query.message.chat.id, "❌ **Invalid User ID. Must be integer.**")

    elif data == "admin_rem_prem":
        await query.message.delete()
        try:
            target_response = await client.ask(
                chat_id=query.message.chat.id,
                text="👤 **Please enter/reply with the User ID you want to remove:**",
                filters=filters.text,
                timeout=60
            )
            target_id = int(target_response.text)
            await remove_premium_flow(client, query.message, target_id)
        except ListenerTimeout:
            await client.send_message(query.message.chat.id, "⏳ **Request timed out.**")
        except ValueError:
            await client.send_message(query.message.chat.id, "❌ **Invalid User ID.**")

    elif data == "admin_info_prem":
        await query.message.delete()
        try:
            target_response = await client.ask(
                chat_id=query.message.chat.id,
                text="👤 **Please enter the User ID to fetch premium info:**",
                filters=filters.text,
                timeout=60
            )
            target_id = int(target_response.text)

            # Show Info
            plan, max_upload, expiry = await digital_botz.get_premium_plan_and_limit(target_id)
            if plan == "Free":
                await client.send_message(query.message.chat.id, "❌ **User does not have an active premium plan.**")
                return

            user_data = await digital_botz.get_user(target_id)
            start_date = user_data.get("start_time") if user_data else None

            remaining_time = "Expired"
            status = "Expired 🔴"
            if expiry:
                delta = expiry - datetime.datetime.now()
                if delta.total_seconds() > 0:
                    remaining_time = f"{delta.days}d {delta.seconds // 3600}h"
                    status = "Active 🟢"
            else:
                remaining_time = "N/A"
                status = "Active (Lifetime) 🟢"

            start_str = start_date.strftime("%d %b %Y %H:%M") if start_date else "N/A"
            expiry_str = expiry.strftime("%d %b %Y %H:%M") if expiry else "N/A"

            info_text = (
                "👤 **Premium User Profile Info**\n\n"
                f"⚡ **User ID:** `{target_id}`\n"
                f"💎 **Plan:** `{plan}`\n"
                f"📅 **Start Date:** `{start_str}`\n"
                f"📆 **Expiry Date:** `{expiry_str}`\n"
                f"⏳ **Remaining Time:** `{remaining_time}`\n"
                f"📂 **Upload Limit:** `{humanbytes(max_upload)}`\n"
                f"📊 **Premium Status:** {status}"
            )
            await client.send_message(query.message.chat.id, info_text)
        except ListenerTimeout:
            await client.send_message(query.message.chat.id, "⏳ **Request timed out.**")
        except ValueError:
            await client.send_message(query.message.chat.id, "❌ **Invalid User ID.**")
