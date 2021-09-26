"""
=====================================================================
Name:           Orion Humphrey
Project:     	Discord Tag Bot
Date:           Sept 9, 2021
Version:        1
Description:    Discord bot to scrape a webpage from a URL in a
                message an provide keyword tags for the link
Notes:          This was partially made to show I know python at a
                certain date. The bot can also play a knock knock
                sound in the channel.
TODO:           # Knock sound
                # Auto tagging of links
                # Error handling
                # Logging
                # Tag if request message has link
                # Manual tags
                # Check guild
                # Change logic to use command function
=====================================================================
"""

import re
import logging
import os
import discord
from process_tags import create_tags

# Global
# Random header to prevent pages from blocking scraping
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh;U;PPC Mac OS X 10_4_11;ja-jp) Apple\
    WebKit/533.19.4 (KHTML	like Gecko) Version/4.1.3 Safari/533.19.4'}

# Enable Logging
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter(
    '%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'))
logger.addHandler(handler)

# Create client object
client = discord.Client()


@client.event
async def on_ready():
    """Function to log that the bot has been started
    """
    logger.info("Bot Started")


@client.event
async def on_message(message):
    """Function to generate keyword tags from a link in a message. Function
    looks for the !tag command

    Args:
        message (Message): Discord Message object
    """
    # Prevent bot from talking to itself
    if message.author == client.user:
        return
    # Regex to pull the !tag command out of a message
    # Using an if statement because there is <50% chance a message contains a tag
    # request making this logic faster than a try/catch.
    tag_regex = re.compile(r'!tag')
    if tag_mo := tag_regex.search(message.content):
        tag_request = tag_mo.group()
    else:
        tag_request = None

    # If someone in chat says 'X', reply with 'X'
    if tag_request:
        # Checking if there if the message was a reply
        if message.reference:
            # Regex to pull a url out of the message replied to
            url_regex = re.compile(r'http\S*')
            url_mo = url_regex.search(message.reference.resolved.content)

            # Check if a URL is in the message. Using a try/catch because as
            # users learn how the command works, there will be a >50% chance
            # the message will contain a URL making this logic faster than
            # an if statement.
            try:
                url = url_mo.group()
                # Create tags
                tags = create_tags(url, header)
                # Reply to tag request
                try:
                    await message.reply(content='Here are your tags:\n' + tags)
                    logger.info(
                        f'{message.author} made a successful tag request.')
                except AttributeError as err:
                    logger.error(err)
                    await message.channel.send('An error occurred. Check the log for details.')
            except AttributeError as err:
                await message.channel.send('To tag a message, it must contain a link to a webpage.')
                logger.info(
                    f'{message.author} made a tag request to a message without a link to a webpage.')

        else:
            await message.channel.send('!tag must be called in a reply.')
            logger.info(
                f'{message.author} made a tag request outside of a reply.')

# Start client
client.run(os.environ["BOT_API_KEY"])
