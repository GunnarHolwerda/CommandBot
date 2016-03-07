"""
    Holds the Command to run the dankmemes command
"""

from ..command import BaseCommand


class DankMemesCommand(BaseCommand):
    """
        Returns a string like so with input: yolo
        YOLO
        O
        L
        O

        Required arguments:
            A string or sentence

        Supported options:
            $space=true
    """

    def __init__(self, command_str):
        super(DankMemesCommand, self).__init__(command_str)
        self._command = "!dankmemes"

    def run(self):
        sentence = self._command_str.upper()
        if 'space' in self._opts and self._opts['space'] == "true":
            sentence = self.__space_string(sentence)

        corner_text = sentence + "\n"
        skip_first = True
        for c in sentence:
            if skip_first:
                skip_first = False
            else:
                corner_text += c + "\n"

        return corner_text

    @staticmethod
    def help():
        return """
            Returns a string like so with input: yolo
            YOLO
            O
            L
            O

            Required arguments:
                A string or sentence

            Supported options:
                $space=true (Places spaces between each character)
        """

    def __space_string(self, str_value):
        """
            Adds spaces between each character in the strings
            @param: str_value, the string to add the spaces too

            @return: returns the spaced out string
        """
        spaced_string = ""
        for i in range(0, len(str_value) * 2):
            if i % 2 == 0:
                spaced_string += str_value[int(i / 2)]
            else:
                spaced_string += " "
        return spaced_string
