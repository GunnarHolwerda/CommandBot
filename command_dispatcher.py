"""
    Command Dispatcher
"""

from discord_commands.command import BaseCommand
from discord_commands.all_commands import commands

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
