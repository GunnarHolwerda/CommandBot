"""
    Holds BaseCommand abstract class
"""
from datetime import datetime
import re
import logging

logger = logging.getLogger('command-bot')


class BaseCommand:
    """
        Abstract class for a Command
    """

    freeze_writing = False

    def __init__(self, message):
        """
        Constructor for BaseCommand
        @param message: discord.message
        @type message: discord.Message
        """
        self._command = ""
        self._message = message
        self._command_str_with_options = message.content
        self._command_str = self.__strip_options(message.content)
        self._opts = self.__parse_options(message.content)
        self._args = self.__parse_args(message.content)
        logger.info("Command run: %s", self.__class__)


    def _msg_is_dm(self):
        """
        Determines if the message was sent as a DM
        @return: True if message is a dm, False otherwise
        @rtype: bool
        """
        return not self._message.server

    def get_msg_server(self):
        """
        @return: Returns the discord.Server object for the current message
        @rtype: discord.Server
        """
        return self._message.server

    def get_msg_author(self):
        """
        @return: Returns the discord.User object of the author for the current message
        @rtype: discord.User
        """
        return self._message.author

    def __parse_args(self, command_str):
        """
            Strips all arguments from a command string and returns them as a dict

            Arguments are required for a command

            :param: command, the string returned from strip_command_string

            :return: dict of arguments passed to command
        """
        args = []

        option_start_index = command_str.find('$') - 1
        if option_start_index >= -1:
            # Check if no args passed then we need to add back the 1 location, that
            # is supposed to be for a space
            if option_start_index == -1:
                option_start_index = 0
            command_str = command_str[:option_start_index]

        if command_str:
            args = command_str.split(' ')

        logger.info("Arguments parsed: %s", ",".join(args))

        return args

    @staticmethod
    def __parse_options(command_str):
        """
            Strips all options from a command string and returns them as a dict

            Options follow this syntax: $option=value

            @param: command, the command returned by strip_command_string

            @return: dict of options passed to command
        """
        options = {}

        command_arr = command_str.split(' ')

        for word in command_arr:
            if word.startswith('$'):
                match = re.search(r'\$(\S+)=(\S+)', word)
                opt = match.group(1)
                value = match.group(2)

                if value == "True" or value == "False":
                    value = bool(value)

                options[opt] = value

        import pprint
        logger.info("Options parsed: %s", pprint.pformat(options))

        return options

    @staticmethod
    def __strip_options(msg):
        """
            Strips the options off of the end of the command_str

            @returns: str, command_str with no options on the end
        """
        index = msg.find('$') - 1
        if index == -2:
            return msg
        else:
            return msg[:index]

    @staticmethod
    def code_wrap(string):
        """
            Returns string wrapped in triple back ticks to create code
            formatting in discord

            @param: string, any string

            @return: ``` + string + ```
        """
        return '```' + string + '```'

    def _write_to_startup(self, command_str=None):
        """	Writes out the command to startup.py to persist the setting across restart """

        # Disable writing out to startup file
        if BaseCommand.freeze_writing:
            return

        if command_str:
            self.__append_to_startup(command_str)
        else:
            args = ''.join(' ' + str(arg) for arg in self._args) if self._args else ''
            opts = ''.join(
                ' ${}={}'.format(opt, value) for opt, value in self._opts.items()
            ).strip() if self._opts else ''

            self.__append_to_startup(self._command + args + opts)

    def __append_to_startup(self, command):
        """
            Adds a run_command line to startup.py startup method

            :param command: command
        """
        if self._msg_is_dm():
            run_command_str = '    msg = Message(content=\"{}\")\n'\
                              '    msg.author = User(id=\'{}\')\n' \
                              '    dispatcher.run_command(msg)\n'.format(command,
                                                                         self.get_msg_author().id)
            logger.info("Adding command '%s' to startup.py for User %s",
                        command, self.get_msg_author().id)
        else:
            run_command_str = '    msg = Message(content=\"{}\")\n'\
                              '    msg.server = Server(id=\'{}\')\n' \
                              '    dispatcher.run_command(msg)\n'.format(command,
                                                                         self.get_msg_server().id)
            logger.info("Adding command '%s' to startup.py for Server %s",
                        command, self.get_msg_server().id)

        file_handle = open('startup.py', 'a')
        file_handle.write(run_command_str)
        file_handle.close()

    def _parse_date_option(self, return_format="%Y%m%d"):
        """
            Parses the date option and returns a date represented as a date

            :param: args, dictionary of arguments and options

            :param return_format: str, the date format

            :return: date_string, string date in %Y%m%d format by default
        """
        if self._opts and 'date' in self._opts:
            date_obj = datetime.strptime(self._opts['date'], "%m/%d/%Y")
            date_string = date_obj.strftime(return_format)
        else:
            date_obj = datetime.now()
            date_string = date_obj.strftime(return_format)

        return date_string

    # Abstract Methods
    def run(self):
        """ Command to be overwritten that will run the command """
        raise NotImplementedError()

    # Methods that can be overwritten
    def validate(self):
        """
            Validates the command, return True, "OK" on success and False, error_msg on failure

            :return: bool, str
        """
        return True, "OK"

    @staticmethod
    def info():
        """
            Spits out a sentence of info for the command to be used for help
            @return: A str of return help
            @rtype: str
        """
        return "No info provided"

    @staticmethod
    def help():
        """
            Command to be overwritten that will display help
        """
        raise NotImplementedError()
