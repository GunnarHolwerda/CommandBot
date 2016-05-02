"""
    Implementation of the AliasCommand to create aliases for commands
"""

from discord_commands.command import BaseCommand


class AliasCommand(BaseCommand):
    """
    	Creates an alias to a command, essentially renaming the command string

        Required arguments:
            first: alias - The new alias for the command
            second: command - the command to create the alias for, can include opts and args

        Supported options:
            $persist=value - boolean t=True or False if you want alias to persist across restart.
                                 default is True

        Example usage:
        !alias !d !dankmemes
        !alias !cf !cowsay $fortune=True
    """

    def __init__(self, message):
        super(AliasCommand, self).__init__(message)
        self._command = "!alias"

        # Parsing the command_str to get the alias and the cmd for the alias
        self._alias, self._aliased_command = self.__get_alias_and_command_for_alias()
        self._command_to_alias = self._args[1]
        self._command_obj = None

    def validate(self):
        from discord_commands.all_commands import COMMANDS
        from discord import Message

        aliases = COMMANDS['aliases']

        # Determine if the alias already exists for user
        if self._msg_is_dm() and self.get_msg_author().id in aliases \
                and self._alias in aliases[self.get_msg_author().id]:
            return False, "Command already exists: {}".format(self._alias)

        # Determine if the alias already exists for the server
        if self.get_msg_server() and self.get_msg_server().id in aliases \
                and  self._alias in aliases[self.get_msg_server().id]:
            return False, "Command already exists: {}".format(self._alias)

        # Determine if command that is trying to be aliased exists
        if self._command_to_alias not in COMMANDS:
            return False, "Command {} is not a valid command".format(self._command_to_alias)

        if self._alias in COMMANDS:
            return False, "That alias already exists as a command"

        # Determine if the command is a valid command (Can create a command object)
        if len(self._aliased_command) > len(self._command_to_alias):
            command_str = self._aliased_command.replace(self._command_to_alias + ' ', '')
        else:
            command_str = self._aliased_command.replace(self._command_to_alias, '')

        self._command_obj = COMMANDS[self._args[1]](Message(content=command_str, server=self._message.server))

        if not self._command_obj:
            return False, "Format of command was invalid"
        else:
            return True, "OK"

    def run(self):
        from discord_commands.all_commands import COMMANDS

        command_class = self._command_obj.__class__
        args = self._command_obj._args
        opts = self._command_obj._opts

        aliases = COMMANDS['aliases']

        id = 0
        if self.get_msg_server() and self.get_msg_server().id not in aliases:
            id = self.get_msg_server().id
        elif self.get_msg_author().id not in aliases:
            id = self.get_msg_author().id

        COMMANDS['aliases'][id] = {}
        aliases[id][self._alias] = {'class': command_class, 'args': args, 'opts': opts}

        if 'persist' not in self._opts or self._opts['persist']:
            self._write_to_startup(command_str=self._command + " " + self._command_str_with_options)

        return "New alias {} -> {} created.".format(self._alias, self._aliased_command)

    def __get_alias_and_command_for_alias(self):
        """
            Pulls out the alias from the command_str and also the command that is going to be
            aliased
        """

        split = self._command_str_with_options.split(' ')
        return split[0], ' '.join(split[1:])


    @staticmethod
    def help():
        return """
        Creates an alias to a command, essentially renaming the command string.

        Required arguments:
            first: command - the command to create the alias for, can include opts and args
            second: alias - The new alias for the command

        Supported options:
            $persist=value - boolean true or false if you want alias to persist across restart.
                                 default is True

        Example usage:
        !alias !d !dankmemes
        !alias !cf !cowsay $fortune=True
        """
