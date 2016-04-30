"""
    Command Dispatcher
"""

from discord_commands.command import BaseCommand
from discord_commands.all_commands import commands


def run_startup():
    """
        This method is called at startup and calls the startup function from startup.py
        which will initialize any persisting commands
    """
    from startup import startup
    BaseCommand.freeze_writing = True
    startup()
    BaseCommand.freeze_writing = False


def run_command(message):
    """
        Command dispatcher for running commands

        :param message: discord.Message, the full message from discord

        :return: None, if command not found, else the result of the command
    """
    command = get_command(message.content)

    if command in commands.keys():
        obj = get_command_object(command, message)
        valid, error = obj.validate()
        result = obj.run() if valid else error
    elif command == "!code":
        result = BaseCommand(message).code_wrap(message.content)
    else:
        return None

    return break_into_messages(result)


def get_command_object(command, message):
    """
        Returns the object for the command being called format

        @param command: str
        @param message: discord.Message object
        @type message: discord.Message

        @return the command object
        @rtype BaseCommand
    """
    # Strip off the command from the message content
    if len(message.content) > len(command):
        message.content = message.content.replace(command + " ", "")
    else:
        message.content = message.content.replace(command, "")

    # If the command is a dictionary it was added as an alias
    if isinstance(commands[command], dict):
        message.content = ""
        # Expand argument list into the command str
        for arg in commands[command]['args']:
            message.content += " " + arg
        # Parse option dictionary and add the options to the command
        for opt, value in commands[command]['opts'].items():
            message.content += " $" + opt + "=" + str(value)

        return commands[command]['class'](message)
    else:
        return commands[command](message)


def break_into_messages(full_msg):
    """
        Breaks the message into a list of 2000 character strings

        :param full_msg: str
    """
    if len(full_msg) < 2000:
        return [full_msg]
    else:
        msg_list = []
        while len(full_msg) > 2000:
            msg_list.append(full_msg[0:2000])
            full_msg = full_msg[2001:len(full_msg)]

        return msg_list


def get_command_str(msg_content):
    """
        Strips off the command and space from the front of the message content

        :param msg_content: str, the full message to strip the command from

        :return: returns the message content - command string
    """
    return " ".join(msg_content.split()[1:])


def get_command(msg_content):
    """
        Strips off the command from the front end of the message

        :param msg_content: str, the whole message to get the command from
    """
    return msg_content.split()[0]
