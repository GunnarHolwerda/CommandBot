"""
    Implementation of the AliasCommand to create aliases for commands
"""

from discord_commands.command import BaseCommand

class AliasCommand(BaseCommand):
    """
    	Creates an alias to a command, essentially renaming the command string

        Required arguments:
            first: alias - the command to create the alias for
            second: command - The new alias for the command

        Supported options:
            $persist=value - boolean true or false if you want alias to persist across restart.
                             default is True

        Example usage:
        !alias !d !dankmemes
    """

    def __init__(self, command_str):
        super(AliasCommand, self).__init__(command_str)
        self._command = "!alias"

        # Parsing the command_str to get the alias and the cmd for the alias
        self._alias, self._aliased_command = self.__get_alias_and_command_for_alias()
        self._command_obj = None

    def validate(self):
        from discord_commands.all_commands import commands

        # Create the command object for the aliased command
        command_str = self._aliased_command.replace(self._args[0] + ' ', '')
        self._command_obj = commands[self._args[0]](command_str)

        # Validate alias and command object could be created
        if self._command_obj and self._alias:
            if self._alias in commands:
                return False, "Command already exists: {}".format(self._alias)
            else:
                return True, "OK"
        else:
            return False, "Command {} not found or alias could not be parsed".format(self._args[0])

    def run(self):
        from discord_commands.all_commands import commands

        command_class = self._command_obj.__class__
        args = self._command_obj._args
        opts = self._command_obj._opts

        # Add alias to commands dictionary
        commands[self._alias] = {'class': command_class, 'args': args, 'opts': opts}

        if 'persist' not in self._opts or self._opts['persist']:
            self._write_to_startup(command_str=self._command + " " +  self._full_command_str)

        return "New alias {} -> {} created.".format(self._alias, self._aliased_command)

    def __get_alias_and_command_for_alias(self):
        """
            Pulls out the alias from the command_str and also the command that is going to be
            aliased
        """
        full_args = []
        for split in self._full_command_str.split('!'):
            # Skip any empty list items
            if not split:
                continue
            else:
                full_args.append("!" + split)

        return full_args[1], full_args[0]


    @staticmethod
    def help():
        return """
        	Creates an alias to a command, essentially renaming the command string

            Required arguments:
                first: command - the command to create the alias for, can include opts and args
                second: alias - The new alias for the command

            Supported options:
                $persist=value - boolean true or false if you want alias to persist across restart.
                                 default is True

            Example usage:
            !alias !dankmemes !d
            !alias !cowsay $fortune=True !cf
        """
