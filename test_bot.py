#!/usr/bin/env python3

"""
Simple test bot to debug /start command issue
"""

import asyncio
import logging
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message
from config import API_HASH, APP_ID, TG_BOT_TOKEN

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create simple bot without web server
app = Client(
    "TestBot",
    api_hash=API_HASH,
    api_id=APP_ID,
    bot_token=TG_BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Simple start command handler for testing"""
    logger.info(f"📨 Received /start from user {message.from_user.id}")
    
    try:
        await message.reply_text(
            "🤖 **TEST BOT RESPONSE**\n\n"
            "✅ Bot is working!\n"
            f"👤 Your ID: `{message.from_user.id}`\n"
            f"📝 Your message: `{message.text}`\n"
            "🔧 This is a test to debug /start command issues."
        )
        logger.info("✅ Response sent successfully")
    except Exception as e:
        logger.error(f"❌ Failed to send response: {e}")

@app.on_message(filters.text & filters.private)
async def echo_handler(client: Client, message: Message):
    """Echo any text message"""
    logger.info(f"📝 Received text: {message.text[:50]}...")
    
    try:
        await message.reply_text(f"🔄 Echo: {message.text}")
    except Exception as e:
        logger.error(f"❌ Failed to echo: {e}")

async def main():
    """Main function to run test bot"""
    try:
        logger.info("🔄 Starting test bot...")
        await app.start()
        
        me = await app.get_me()
        logger.info(f"✅ Test bot started: @{me.username}")
        logger.info("💡 Send /start to test the bot")
        
        # Keep bot running for 30 seconds
        logger.info("⏳ Bot running for 30 seconds...")
        await asyncio.sleep(30)
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await app.stop()
        logger.info("✅ Test bot stopped")

if __name__ == "__main__":
    asyncio.run(main())