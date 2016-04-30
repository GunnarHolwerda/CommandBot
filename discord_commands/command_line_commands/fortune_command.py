"""
    Holds the Command for !cowsay
"""

from ..command import BaseCommand
from .command_line_command import CommandLineCommand

class FortuneCommand(BaseCommand, CommandLineCommand):
    """
        Runs fortune from the command line and returns the result

        Required Arguments:
            None

        Options Supported:
            None
    """

    def __init__(self, command_str):
        super(FortuneCommand, self).__init__(command_str)
        self._command = "!fortune"
        self._cmd_line_command = "fortune"

    def validate(self):
        return self._command_line_validate()

    def run(self):
        result = self._call_command_line_for_result()
        return self.code_wrap(result)

    @staticmethod
    def help():
        return """
            Runs fortune from the command line and returns the result

            Required Arguments:
                None

            Options Supported:
                None
        """

    @staticmethod
    def info():
        return "Sends a message including a fortune"
