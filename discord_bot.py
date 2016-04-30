#!/usr/bin/python3

"""
    This program adds commands to a discord server being logged in by the user
    specified in user.py
"""
import argparse
import asyncio
import discord
import bot
import os
import logging
from command_dispatcher import run_command, run_startup

# ArgParse
parser = argparse.ArgumentParser(description="Discord Bot")
parser.add_argument('-u', '--update-commands', dest='update_commands',
                    action='store_true',
                    help='Updates all_commands.py file to include any' +
                    ' new commands added to discord_commands directory')
parser.add_argument('-s', '--fresh-start', dest='fresh_start',
                    action='store_true', help='Starts the bot without using startup.py')
parser.add_argument('-l', '--no-log', dest='no_log', action='store_true', help="Disables logging")
parser.add_argument('-t', '--token', dest='token', type=str, help="Specify a specific token")
args = parser.parse_args()
client = discord.Client()

# Setup logging
if not args.no_log:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='/tmp/log/discord/discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


@client.event
@asyncio.coroutine
def on_ready():
    """
        This functions runs when the client is logged in
    """
    print('Logged in as ')
    print(client.user.name)
    print(client.user.id)
    print('-------------')

    if not args.fresh_start:
        run_startup()


@client.event
@asyncio.coroutine
def on_message(message):
    """
        This message gets called everytime a message is received in Discord

        @param message: str, message object that contains information about the msg
    """
    msg = message.content
    msgs = run_command(msg)

    if msgs:
        for msg in msgs:
            yield from client.send_message(message.channel, msg)


if __name__ == "__main__":
    if args.update_commands:
        os.system('python3 scripts/update_all_commands.py')
        exit()

    # Start the bot
    print("Starting DiscordBot")
    if args.token:
        client.run(args.token)
    else:
        client.run(bot.token)
