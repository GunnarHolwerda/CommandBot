"""
    Holds the Command for !cowsay
"""

import os
from .command import BaseCommand

class CowSayCommand(BaseCommand):
    """
        Runs cowsay on the string passed and prints out the command from the
        cow

        Required Arguments:
            A str or sentence (SENTENCE MUST BE WRAPPED IN QUOTES)

        Options Supported:
            None
    """

    def __init__(self, command_str):
        super(CowSayCommand, self).__init__(command_str)
        self._command = "!cowsay"

    def run(self):
        # This command runs a command in the terminal, checks for && or ; to
        # avoid someone running malicious commands
        if self._command_str.find('&&') == -1 and self._command_str.find(';') == -1:
            return self.code_wrap(os.popen("cowsay %s" % self._command_str).read())
        else:
            return "Nice try."

    @staticmethod
    def help():
        return """
            Runs cowsay on the string passed and prints out the command from the
            cow

            Required Arguments:
                A str or sentence (SENTENCE MUST BE WRAPPED IN QUOTES)

            Options Supported:
                None
        """
