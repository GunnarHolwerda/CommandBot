"""
    This module is numerous functions that will come in handy along with the
    Discord Python API
"""

def strip_command_string(command, msg_content):
    """
        Strips off the command and space from the front of the message content

        @param: command, the command string without a space to be stripped
        @param: msg_content, the full message to strip the command from

        @return: returns the message content - command string
    """
    return msg_content.replace(command + " ", '')
