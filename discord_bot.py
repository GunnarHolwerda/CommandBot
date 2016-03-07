#!/usr/bin/python3

"""
    This program adds commands to a discord server being logged in by the user
    specified in user.py
"""
import argparse
import asyncio
import discord
import user
import os
from command_dispatcher import run_command

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discord Bot")
    parser.add_argument('-u', '--update-commands', dest='update_commands',
                        action='store_true',
                        help='Updates all_commands.py file to include any' +
                        ' new commands added to discord_commands directory')
    args = parser.parse_args()

    if args.update_commands:
        os.system('/usr/bin/python3 scripts/update_all_commands.py')
        exit()

    # Start the bot
    client = discord.Client()
    client.run(user.email, user.password)


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


@client.event
@asyncio.coroutine
def on_message(message):
    """
        This message gets called everytime a message is received in Discord

        @param: message, message object that contains information about the msg
    """
    msg = message.content
    new_msg = run_command(msg)

    if new_msg:
        yield from client.send_message(message.channel, new_msg)
