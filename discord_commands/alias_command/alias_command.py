"""
    Implementation of the AliasCommand to create aliases for commands
"""

from discord_commands.command import BaseCommand

class AliasCommand(BaseCommand):
    """
    	Creates an alias to a command, essentially renaming the command string

        Required arguments:
            first: command - the command to create the alias for
            second: alias - The new alias for the command

        Supported options:
            $persist=value - boolean true or false if you want alias to persist across restart.
                             default is True

        Example usage:
        !alias !dankmemes !d
    """

    def __init__(self, command_str):
        super(AliasCommand, self).__init__(command_str)
        self._command = "!alias"

    def run(self):
        from discord_commands.all_commands import commands

        # TODO: Possibly check format of alias to ensure it isn't a common word, (maybe ensure, it
        # starts with a !)
        command = self._args[0]
        alias = self._args[1]
        command_class = commands[command]
        commands[alias] = command_class

        if 'persist' not in self._opts or self._opts['persist']:
            self.write_to_startup()

        return "New alias {} -> {} created.".format(alias, command)

    def validate(self):
        if len(self._args) == 2:
            from discord_commands.all_commands import commands
            if self._args[0] in commands:
                return True, "OK"
            else:
                return False, "Command {} not found".format(self._args[0])
        else:
            return False, "Not enough arguments supplied"

    @staticmethod
    def help():
        return """
        	Creates an alias to a command, essentially renaming the command string

            Required arguments:
                first: command - the command to create the alias for
                second: alias - The new alias for the command

            Supported options:


            Example usage:

            !alias !dankmemes !d
        """
