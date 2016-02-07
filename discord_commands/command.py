"""
    Holds BaseCommand abstract class
"""
from datetime import datetime
import re


class BaseCommand:
    """
        Abstract class for a Command
    """

    def __init__(self, command_str):
        print("BaseCommand constructor being called")
        self._command = ""
        self._command_str = command_str
        self._opts = self.__parse_options()
        self._args = self.__parse_args()

    def _parse_date_option(self):
        """
            Parses the date option and returns the date_string to be used by
            ESPN urls

            @param: args, dictionary of arguments and options

            @return: date_string, string date in %Y%m%d format
        """
        if self._opts and 'date' in self._opts:
            date_obj = datetime.strptime(self.opts['date'], "%m/%d/%Y")
            date_string = date_obj.strftime("%Y%m%d")
        else:
            date_obj = datetime.now()
            date_string = date_obj.strftime("%Y%m%d")

        return date_string

    def __parse_args(self):
        """
            Strips all arguments from a command string and returns them as a dict

            Arguments are required for a command

            @param: command, the string returned from strip_command_string

            @return: dict of arguments passed to command
        """
        args = ()

        option_start_index = self._command_str.find('$') - 1
        if option_start_index >= -1:
            # Check if no args passed then we need to add back the 1 location, that
            # is supposed to be for a space
            if option_start_index == -1:
                option_start_index = 0
            self._command_str = self._command_str[:option_start_index]

        args = self._command_str.split(' ')

        return args


    def __parse_options(self):
        """
            Strips all options from a command string and returns them as a dict

            Options follow this syntax: $option=value

            @param: command, the command returned by strip_command_string

            @return: dict of options passed to command
        """
        options = {}

        command_arr = self._command_str.split(' ')

        for word in command_arr:
            if word.startswith('$'):
                match = re.search(r'\$(\S+)=(\S+)', word)
                opt = match.group(1)
                value = match.group(2)

                options[opt] = value

        return options


    # Abstract Methods
    def run(self):
        """
            Command to be overwritten that will run the command
        """
        raise NotImplementedError()
