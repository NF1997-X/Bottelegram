#(©)Codexbotz

import asyncio
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))  # type: ignore[arg-type]
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_messages = await message.copy(chat_id = CHANNEL_ID, disable_notification=True)
        post_message = post_messages[0] if isinstance(post_messages, list) else post_messages
    except FloodWait as e:
        sleep_time = getattr(e, 'value', getattr(e, 'x', 1))
        await asyncio.sleep(float(sleep_time) if isinstance(sleep_time, (int, float)) else 1)
        post_messages = await message.copy(chat_id = CHANNEL_ID, disable_notification=True)
        post_message = post_messages[0] if isinstance(post_messages, list) else post_messages
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(CHANNEL_ID)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    
    # Get bot username from client.me
    try:
        me = await client.get_me()
        username = me.username
    except:
        username = "bot"
        
    link = f"https://t.me/{username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    
    await reply_text.edit_text(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except FloodWait as e:
            sleep_time = getattr(e, 'value', getattr(e, 'x', 1))
            await asyncio.sleep(float(sleep_time) if isinstance(sleep_time, (int, float)) else 1)
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))  # type: ignore[arg-type]
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(CHANNEL_ID)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    
    # Get bot username from client.me
    try:
        me = await client.get_me()
        username = me.username
    except:
        username = "bot"
        
    link = f"https://t.me/{username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        sleep_time = getattr(e, 'value', getattr(e, 'x', 1))
        await asyncio.sleep(float(sleep_time) if isinstance(sleep_time, (int, float)) else 1)
        await message.edit_reply_markup(reply_markup)
    except Exception:
        pass