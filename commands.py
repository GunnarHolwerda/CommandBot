"""
    This file runs the command
"""

from discord_commands.command import BaseCommand
from discord_commands.butts_command import ButtCommand
from discord_commands.cowsay_command import CowSayCommand
from discord_commands.dankmemes_command import DankMemesCommand
from discord_commands.sports_commands.nba_command import NBACommand
from discord_commands.sports_commands.ncaam_command import NCAAMCommand


commands = {
    '!nba': NBACommand,
    '!ncaam': NCAAMCommand,
    '!dankmemes': DankMemesCommand,
    '!cowsay': CowSayCommand,
    '!butt': ButtCommand
}

def run_command(msg_content):
    """
        Command dispatcher for running commands

        @param: msg_content, the full message from discord

        @return: None, if command not found, else the result of the command
    """
    command = get_command(msg_content)
    command_str = get_command_str(msg_content)

    if command in commands.keys():
        obj = commands[command](command_str)
        return obj.run()
    elif command == "!code":
        return BaseCommand(command_str).code_wrap(command_str)
    else:
        return None

def get_command_str(msg_content):
    """
        Strips off the command and space from the front of the message content

        @param: command, the command string without a space to be stripped
        @param: msg_content, the full message to strip the command from

        @return: returns the message content - command string
    """
    return " ".join(msg_content.split()[1:])

def get_command(msg_content):
    """
        Strips off the command from the front end of the message

        @param: msg_content, the whole message to get the command from
    """
    return msg_content.split()[0]
