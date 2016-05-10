#!/usr/bin/python3

"""
    This program adds commands to a discord server being logged in by the user
    specified in user.py
"""
import argparse
import asyncio
import discord
import os
import logging
import time
from command_dispatcher import CommandDispatcher

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

# Setup logging
if not args.no_log:
    # Set up logging for the Discord API Wrapper
    logger = logging.getLogger('command-bot')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='/var/log/discord/discord.log',
    encoding='utf-8',
    mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
    logger.addHandler(handler)
    logger.info("Starting command-bot")

if not args.token:
    print("A token must be supplied")
    logger.error("No token supplied exiting")
    exit()


client = discord.Client()
dispatcher = CommandDispatcher() if not args.fresh_start else CommandDispatcher(fresh_start=True)


@client.event
@asyncio.coroutine
def on_ready():
    """
        This functions runs when the client is logged in
    """
    logger.info("%s successfully started", client.user.name)


@client.event
@asyncio.coroutine
def on_message(message):
    """
        This message gets called every time a message is received in Discord

        @param message: str, message object that contains information about the msg
    """
    msgs = dispatcher.run_command(message)

    if msgs:
        for msg in msgs:
            yield from client.send_message(message.channel, msg)


if __name__ == "__main__":
    if args.update_commands:
        os.system('python scripts/update_all_commands.py')
        exit()

    # Start the bot
    while True:
        client.run(args.token)
        # Retry every five seconds to log back in
        time.sleep(5)
