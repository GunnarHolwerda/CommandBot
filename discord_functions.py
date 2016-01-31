"""
    This module is numerous functions that will come in handy along with the
    Discord Python API
"""

import re

def strip_command_string(command, msg_content):
    """
        Strips off the command and space from the front of the message content

        @param: command, the command string without a space to be stripped
        @param: msg_content, the full message to strip the command from

        @return: returns the message content - command string
    """
    return msg_content.replace(command + " ", '')

def parse_command(command):
    """
        Parses the command string for arguments and options and returns them
        as a dict in the form:
        dict = {
            'args': ()
            'opts': {
                'opt1': value
            }
        }

        @param: command, the command string returned from strip_command_string

        @return: dict, dictionary containing all options and args
    """
    args_and_options = {}
    args_and_options['args'] = __parse_args(command)
    args_and_options['opts'] = __parse_options(command)

    return args_and_options


def __parse_args(command):
    """
        Strips all arguments from a command string and returns them as a dict

        Arguments are required for a command

        @param: command, the string returned from strip_command_string

        @return: dict of arguments passed to command
    """
    args = ()

    option_start_index = command.find('$') - 1
    if option_start_index >= -1:
        # Check if no args passed then we need to add back the 1 location, that
        # is supposed to be for a space
        if option_start_index == -1:
            option_start_index = 0
        command = command[:option_start_index]

    args = command.split(' ')

    return args


def __parse_options(command):
    """
        Strips all options from a command string and returns them as a dict

        Options follow this syntax: $option=value

        @param: command, the command returned by strip_command_string

        @return: dict of options passed to command
    """
    options = {}

    command_arr = command.split(' ')

    for word in command_arr:
        if word.startswith('$'):
            match = re.search(r'\$(\S+)=(\S+)', word)
            opt = match.group(1)
            value = match.group(2)

            options[opt] = value

    return options
