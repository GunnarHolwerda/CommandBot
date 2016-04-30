"""
    Command for getting helptext for another command
"""

from ..command import BaseCommand


class HelpCommand(BaseCommand):
    """
        Displays help for a command

        Required arguments:
            If left empty will list all available commands on system
            Otherwise pass in a command,
            Command (i.e. !dankmemes)

        Supported options:
            None
    """

    def __init__(self, message):
        super(HelpCommand, self).__init__(message)
        self._command = "!help"

    def validate(self):
        return True, "OK"

    def run(self):
        from ..all_commands import commands
        if self._args:
            return self.code_wrap(commands[self._args[0]].help())
        else:
            ret_str = "Usage: !help <command>\nPrint help information for the command specified"
            ret_str += "\n\nAvailable Commands: \n"
            for command, obj in commands.items():
                if not isinstance(obj, dict):
                    ret_str += "- " + command + " - " + obj.info() + "\n"
                else:
                    ret_str += "- " + command + " - " + obj['class'].info() + "\n"
            return self.code_wrap(ret_str)

    @staticmethod
    def info():
        return "Displays help text for a command"

    @staticmethod
    def help():
        return """
            Displays help for a command

            Required arguments:
                Command (i.e. !dankmemes)

            Supported options:
                None
        """
