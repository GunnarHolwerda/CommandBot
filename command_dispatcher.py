"""
    Command Dispatcher
"""

from discord_commands.command import BaseCommand
from discord_commands.all_commands import COMMANDS

ALIASES = COMMANDS['aliases']


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

    if is_alias_or_command(command, message):
        obj = get_command_object(command, message)
        valid, error = obj.validate()
        result = obj.run() if valid else error
    elif command == "!code":
        result = BaseCommand(message).code_wrap(message.content)
    else:
        return None

    return break_into_messages(result)

def is_alias_or_command(command, message):
    """

    @param command: the command to check if exists
    @type command: str
    @param message: the message
    @type message: discord.Message
    @return: True, if exists, False otherwise
    @rtype: bool
    """

    if command in COMMANDS.keys():
        return True
    elif message.server and command in ALIASES[message.server.id]:
        return True
    elif not message.server and \
            message.channel.is_private and \
            message.author.id in ALIASES and\
            command in ALIASES[message.author.id]:
        return True
    else:
        return False



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

    if command_is_server_alias(command, message.server):
        return parse_alias_to_command(message, ALIASES[message.server.id][command])
    elif command_is_dm_alias(command, message.author):
        return parse_alias_to_command(message, ALIASES[message.author.id][command])
    else:
        return COMMANDS[command](message)


def command_is_server_alias(command, server):
    """
    Returns True if the command is an alias for a server
    @param command: The command
    @type command: str
    @param user: The Discord Server object to check the alias for
    @type user: discord.Server
    @return: True if the command is an alias for the server, False otherwise
    """
    return server and server.id in ALIASES and command in ALIASES[server.id]

def command_is_dm_alias(command, user):
    """
    Returns True if the command is an alias for a user in their DM's with the bot
    @param command: The command
    @type command: str
    @param user: The Discord User object to check the alias for
    @type user: discord.User
    @return: True if the command is an alias for the user, False otherwise
    """
    return user.id in ALIASES and command in ALIASES[user.id]

def parse_alias_to_command(message, alias):
    """
    Will explode and alias into a full command and return the object for that command
    @param message: The message from discord
    @type message: discord.Message
    @param alias: The alias to explode
    @type alias: dict
    @return: The BaseCommand object to be run
    @rtype: BaseCommand
    """
    # Expand argument list into the command str
    for arg in alias['args']:
        message.content += " " + arg
    # Parse option dictionary and add the options to the command
    for opt, value in alias['opts'].items():
        message.content += " $" + opt + "=" + str(value)

    return alias['class'](message)

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
