#!/usr/bin/python3

"""
    This program adds commands to a discord server being logged in by the user
    specified in user.py
"""
import discord
import asyncio
import user
import os
from pprint import pprint
#from discord_commands import sports_commands
from discord_commands.sports_commands.nba_command import NBACommand
from discord_functions import strip_command_string
from discord_commands_old import get_corner_text, replace_with_butts, code_wrap
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
    cmd = NBACommand("")
    print(cmd.run())


@client.event
@asyncio.coroutine
def on_message(message):
    """
        This message gets called everytime a message is received in Discord

        @param: message, message object that contains information about the msg
    """
    msg = message.content

    if msg.startswith('!dankmemes'):
        sentence = strip_command_string('!dankmemes', msg)
        new_msg = get_corner_text(sentence)
        yield from client.send_message(message.channel, new_msg)

    elif msg.startswith('!butt'):
        command_str = strip_command_string('!butt', msg)
        butt_string = replace_with_butts(command_str)
        yield from client.send_message(message.channel, butt_string)

    elif msg.startswith('!cowsay'):
        sentence = strip_command_string('!cowsay', msg)
        # This command runs a command in the terminal, checks for && or ; to
        # avoid someone running malicious commands
        if sentence.find('&&') == -1 and sentence.find(';') == -1:
            new_msg = os.popen("cowsay %s" % sentence).read()
        else:
            return
        yield from client.send_message(message.channel, new_msg)

    elif msg.startswith('!code'):
        code = strip_command_string('!code', msg)
        code_str = code_wrap(code)
        yield from client.send_message(message.channel, code_str)

    # elif msg.startswith('!nba'):
    #     args = strip_command_string('!nba', msg)
    #     opts_args = parse_command(args)
    #     new_msg = code_wrap(get_nba_scores(opts_args))
    #     yield from client.send_message(message.channel, new_msg)
    #
    # elif msg.startswith('!ncaam'):
    #     args = strip_command_string('!ncaam', msg)
    #     opts_args = parse_command(args)
    #     new_msg = code_wrap(get_ncaam_scores(opts_args))
    #     yield from client.send_message(message.channel, new_msg)

client.run(user.email, user.password)
