#(©)Codexbotz

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, CHANNEL_ID
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))  # type: ignore[arg-type]
async def batch(client: Client, message: Message):
    await message.reply_text(
        "**Batch Link Generator**\n\n"
        "Please forward the first and last messages from your DB channel to generate batch links.\n"
        "You can also send DB channel post links.\n\n"
        "Reply to this message with the first message or link."
    )

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))  # type: ignore[arg-type]
async def link_generator(client: Client, message: Message):
    await message.reply_text(
        "**Single Link Generator**\n\n"
        "Please forward a message from your DB channel or send the DB channel post link.\n"
        "Reply to this message with the message or link."
    )

# Alternative batch function that works with the current message flow
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.reply & filters.text)  # type: ignore[arg-type]
async def handle_batch_reply(client: Client, message: Message):
    if not message.reply_to_message:
        return
    
    replied_msg = message.reply_to_message.text
    if not ("Batch Link Generator" in replied_msg or "Single Link Generator" in replied_msg):
        return
    
    msg_id = await get_message_id(client, message)
    if not msg_id:
        await message.reply_text("❌ Error\n\nThis message is not from the DB Channel", quote=True)
        return
    
    # Generate single link
    base64_string = await encode(f"get-{msg_id * abs(CHANNEL_ID)}")
    
    # Get bot username 
    try:
        me = await client.get_me()
        username = me.username or "bot"
    except:
        username = "bot"
        
    link = f"https://t.me/{username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)