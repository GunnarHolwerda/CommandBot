#!/usr/bin/python3

"""
    This program adds commands to a discord server being logged in by the user
    specified in user.py
"""
import discord
import asyncio
import user
from command_dispatcher import run_command

client = discord.Client()

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

client.run(user.email, user.password)
