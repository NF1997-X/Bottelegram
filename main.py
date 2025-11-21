#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
from bot import Bot

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    try:
        logger.info("Starting File Sharing Bot...")
        bot = Bot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()