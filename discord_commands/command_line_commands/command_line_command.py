"""
    Holds the Command for !cowsay
"""

import os

class CommandLineCommand:
    """
        Abstract class for all commands that run a direct command from the command line
    """

    def __init__(self, message):
        super(CommandLineCommand, self).__init__(message)
        self._cmd_line_command = ""

    def _command_line_validate(self):
        # This command runs a command in the terminal, checks for && or ; to
        # avoid someone running malicious commands
        if self._cmd_line_command.find('&&') != -1 or self._cmd_line_command.find(';') != -1:
            return False, "Illegal command"
        else:
            return True, "OK"

    def _call_command_line_for_result(self):
        return os.popen(self._cmd_line_command).read()
