"""
    Holds the Command for !cowsay
"""

from ..command import BaseCommand
from .command_line_command import CommandLineCommand

class CowSayCommand(BaseCommand, CommandLineCommand):
    """
        Runs cowsay on the string passed and prints out the command from the cow

        Required Arguments:
            A str or sentence (SENTENCE MUST BE WRAPPED IN QUOTES)

        Options Supported:
            $fortune=True, The cow will say your fortune
    """

    def __init__(self, command_str):
        super(CowSayCommand, self).__init__(command_str)
        self._command = "!cowsay"
        self._cmd_line_command = "cowsay {}".format(self._command_str)

    def validate(self):
        return self._command_line_validate()

    def run(self):
        if 'fortune' in self._opts and self._opts['fortune']:
            self._cmd_line_command = "fortune | cowsay"

        return self.code_wrap(self._call_command_line_for_result())

    @staticmethod
    def help():
        return """
            Runs cowsay on the string passed and prints out the command from the
            cow

            Required Arguments:
                A str or sentence (SENTENCE MUST BE WRAPPED IN QUOTES)

            Options Supported:
                $fortune=True, The cow will say your fortune
        """
