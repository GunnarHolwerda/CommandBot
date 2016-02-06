"""
    This file has functions that help discord run all of the commands added
    in custom_discord.py
"""
import random

# BUTTS CONSTANTS
BUTT_REPLACE_DELIMITER = '$'
BUTT_REPLACE_STRING = "butts"

# SCORE CONSTANTS
ESPN_NBA_BASE_URL = "http://espn.go.com/nba/scoreboard/_/"
ESPN_NCAAM_BASE_URL = "http://espn.go.com/mens-college-basketball/scoreboard/_/"


def space_string(str_value):
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


def get_corner_text(sentence):
    """
        Returns a string like so with input: yolo
        YOLO
        O
        L
        O

        @param: sentence, sentence to transform

        @return: string in that format
    """
    sentence = sentence.upper()

    corner_text = sentence + "\n"
    skip_first = True
    for c in sentence:
        if skip_first:
            skip_first = False
        else:
            corner_text += c + "\n"

    return corner_text


def replace_with_butts(msg):
    """
        Returns a the message with specific words replaced with butts.
        A user can choose what word to replace by preceding it with $ at the
        end of the string
        OR
        A user can let the program randomly pick words to replace with butts

        @param: msg, the msg to replace words in
    """
    replace_str = __extract_replace_str(msg)
    if replace_str:
        index_of_delimiter = msg.find(BUTT_REPLACE_DELIMITER) - 1
        new_msg = msg[:index_of_delimiter]

        return new_msg.replace(replace_str, BUTT_REPLACE_STRING)
    else:
        return_str = "Could not find the delimiter '$'' to specify the replace str\n"
        return_str += "Initializing crazy butt power...\n"

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
            new_msg = new_msg.replace(" " + word + " ", " " + BUTT_REPLACE_STRING + " ")

        return_str += new_msg
        return return_str


def __extract_replace_str(msg):
    """
        Extracts the replacement string from the msg, if not found returns ""
    """
    index = msg.find(BUTT_REPLACE_DELIMITER) + 1
    if index == 0:
        return ""
    else:
        return msg[index:]


def code_wrap(msg):
    """
        Returns the string passed wrapped in triple `'s to wrap in a code block

        @return: ``` + msg + ```, parameter passed returned wrapped in ```
    """
    return "```" + msg + "```"
