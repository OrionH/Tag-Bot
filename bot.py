#!/usr/bin/env python
"""
=====================================================================
@author:        Orion Humphrey
Project:     	Discord Tag Bot
Date:           Nov 11, 2021
Version:        2
Description:    Discord bot to scrape a webpage from a URL in a
                message an provide keyword tags for the link
Notes:          This was partially made to show I know python at a
                certain date.
=====================================================================
"""

import re
import logging
import os
import sys
import discord
from discord.ext import commands
from process_tags import create_tags
from api_token import BOT_API_TOKEN

# Create log folder
if not os.path.exists('logs'):
    os.mkdir('logs')

# Enable Logging
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='logs/bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter(
    '%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'))
logger.addHandler(handler)

# Enable STDOUT Logging
handler2 = logging.StreamHandler(sys.stdout)
handler2.setFormatter(logging.Formatter(
    '%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S'))
logger.addHandler(handler2)

# Create bot object with a specified command prefix
bot = commands.Bot(command_prefix='!', case_insensitive=True,
                   strip_after_prefix=True)
# Default help command removed in replace of a custom help command
bot.remove_command('help')


@bot.event
async def on_ready():
    """Function to log that the bot has been started
    """
    logger.info("Bot Started")


@bot.command()
async def help(ctx) -> None:
    """Function to show a list of bot commands in an embedded message.

    Args:
        ctx (Context): The message that invoked this function.
    """
    embed = discord.Embed(
        title='Bot Commands',
        description='Use these commands to tag links with keywords.',
        color=discord.Color.gold(),
        url='https://github.com/OrionH/Tag-Bot'
    )
    embed.set_thumbnail(url='https://i.imgur.com/LjD6elk.png')
    embed.set_image(url='https://i.imgur.com/rvvIBxi.png')

    embed.add_field(
        name='!help',
        value='Shows this list of help commands',
        inline=False,
    )
    embed.add_field(
        name='!tag',
        value='Reply to a message that contains a link with the !tag command to generate keywords for the webpage.',
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command()
async def tag(ctx) -> None:
    """Function to generate keyword tags from a link in a message. Function
#     looks for the !tag command

    Args:
        ctx (Context): The message that invoked this function.
    """
    if ctx.message.reference:
        # Regex to pull a url out of the message replied to
        url_regex = re.compile(r'http\S*')
        url_mo = url_regex.search(ctx.message.reference.resolved.content)

        # Check if a URL is in the ctx.message. Using a try/catch because as
        # users learn how the command works, there will be a >50% chance
        # the message will contain a URL making this logic faster than
        # an if statement.
        try:
            url = url_mo.group()
            # Create tags
            tags = create_tags(url)
            # Reply to tag request
            try:
                await ctx.message.reply(content='Here are your tags:\n' + tags)
                logger.info(
                    f'{ctx.message.author} made a successful tag request.')
            except AttributeError as err:
                logger.error(err)
                await ctx.message.channel.send('An error occurred. Check the log for details.')
        except AttributeError as err:
            await ctx.message.channel.send('To tag a message, it must contain a link to a webpage.')
            logger.info(
                f'{ctx.message.author} made a tag request to a message without a link to a webpage.')

    else:
        await ctx.message.channel.send('!tag must be called in a reply.')
        logger.info(
            f'{ctx.message.author} made a tag request outside of a reply.')


if __name__ == '__main__':
    # Start bot
    bot.run(os.environ["BOT_API_TOKEN"] or BOT_API_TOKEN)
