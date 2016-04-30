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
            $space=value - Boolean [default=False], adds spaces between letters
    """

    def __init__(self, message):
        super(DankMemesCommand, self).__init__(message)
        self._command = "!dankmemes"

    def run(self):
        sentence = self._command_str.upper()
        if 'space' in self._opts and self._opts['space']:
            sentence = DankMemesCommand.__space_string(sentence)

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

    @staticmethod
    def info():
        return "Prints the word given to it vertically and horizontally starting in the upper left"

    @staticmethod
    def __space_string(str_value):
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
