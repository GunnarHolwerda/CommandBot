"""
    Holds the Command to run the butts command
"""

import random
from .command import BaseCommand

class ButtCommand(BaseCommand):
    """
        Returns a the message with specific words replaced with butts.
        A user can choose what word to replace by preceding it with $ at the
        end of the string
        OR
        A user can let the program randomly pick words to replace with butts

        Required arguments: None

        Supported options:
            $replace=value (value is the word to be replaced in the sentence)
    """

    BUTT_REPLACE_STRING = "butts"

    def __init__(self, command_str):
        super(ButtCommand, self).__init__(command_str)
        self._command = "!butts"

    def run(self):
        if 'replace' in self._opts:
            return self.__chosen_replace()
        else:
            return self.__random_replace()

    def __chosen_replace(self):
        """
            This method gets called when the replace option has been passed
            it replaces all instances of the replace string with
            BUTT_REPLACE_STRING
        """
        replace_str = self._opts['replace']
        return self._command_str.replace(replace_str, self.BUTT_REPLACE_STRING)

    def __random_replace(self):
        """
            When no options are passed this method will replace random strings
            with BUTT_REPLACE_STRING
        """
        return_str = ""
        msg = self._command_str

        words = msg.split()
        num_words = len(words)
        num_to_replace = max(5, int(0.2 * num_words), 1)

        replace_words = []

        while len(replace_words) < num_to_replace:
            rand_num = random.randint(0, num_words - 1)
            if words[rand_num] not in replace_words and len(words[rand_num]) > 2:
                replace_words.append(words[rand_num])

        new_msg = msg
        for word in replace_words:
            new_msg = new_msg.replace(" " + word + " ", " " + self.BUTT_REPLACE_STRING + " ")

        return_str += new_msg

        return return_str
