"""
    This file has functions that help discord run all of the commands added
    in custom_discord.py
"""
import random
import requests
import json
import re
from datetime import datetime

# BUTTS CONSTANTS
BUTT_REPLACE_DELIMITER = '$'
BUTT_REPLACE_STRING = "butts"

# SCORE CONSTANTS
ESPN_NBA_BASE_URL = "http://espn.go.com/nba/scoreboard/_/"
ESPN_NCAAM_BASE_URL = "http://espn.go.com/mens-college-basketball/scoreboard/_/"

# ESPN GAME STATE CONSTANTS
ESPN_GAME_NOT_STARTED = "STATUS_SCHEDULED"
ESPN_GAME_IN_PROGRESS = "STATUS_IN_PROGRESS"
ESPN_GAME_HALFTIME = "STATUS_HALFTIME"
ESPN_GAME_FINISHED = "STATUS_FINAL"


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
            new_msg = new_msg.replace(
                " " + word + " ", " " + BUTT_REPLACE_STRING + " ")

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


def get_nba_scores(args=None):
    """
        Scrapes ESPN.com for NBA scores and prints out all scores for the day
        @param: args, dictionary returned by parse_command in discord_functions

        Required arguments: None
        Supported options:
            $date=value (value must follow %m/%d/%Y format)

        @return: msg, the printout of all of the scores
    """

    date_string = __parse_date_option(args)

    data = __extract_espn_json_scoreboard_data(
        "{}date/{}".format(ESPN_NBA_BASE_URL, date_string))
    scores = __create_scores_dict(data)

    msg = __generate_score_printout(scores)
    return msg


def get_ncaam_scores(args=None):
    """
        Scrapes ESPN.com for NCAAM scores and prints out all scores for the day

        @param: args, dictionary returned by parse_command in discord_functions

        Required arguments: None
        Supported options:
            $date=value (value must follow %m/%d/%Y format)

        @return: msg, the printout of all of the scores
    """

    date_string = __parse_date_option(args)

    data = __extract_espn_json_scoreboard_data(
        "{}date/{}".format(ESPN_NCAAM_BASE_URL, date_string))
    scores = __create_scores_dict(data)

    msg = __generate_score_printout(scores)
    return msg


def __generate_score_printout(scores):
    """
        Generates the printout for sport score commands

        @param: scores, a dictionary containing score data
        @return: the string printout of the game states
    """
    final_scores = "Final Scores:\n"
    in_progress = "In Progess:\n"
    not_started = "Not started:\n"
    for _, score in scores.items():
        game_state = score['status']['state']
        team_one = score['teams'].pop()
        team_two = score['teams'].pop()

        # Determine winner, losing team has lowercase abbreviation
        if game_state == ESPN_GAME_FINISHED:
            if team_one['winner']:
                team_two['abbreviation'] = team_two['abbreviation'].lower()
            elif team_two['winner']:
                team_one['abbreviation'] = team_one['abbreviation'].lower()

        score_str = "{:<4} vs {:<4} ... {:<3}-{:>3} {}\n".format(team_one['abbreviation'],
                                                                 team_two[
                                                                     'abbreviation'],
                                                                 team_one[
                                                                     'score'],
                                                                 team_two[
                                                                     'score'],
                                                                 score['status']['description'])

        if game_state == ESPN_GAME_FINISHED:
            final_scores += score_str
        elif game_state == ESPN_GAME_IN_PROGRESS or game_state == ESPN_GAME_IN_PROGRESS:
            in_progress += score_str
        else:
            not_started += score_str

    return not_started + "\n" + in_progress + "\n" + final_scores


def __extract_espn_json_scoreboard_data(url):
    """
        Extracts JSON object from ESPN scoreboard page and returns as a json
        object

        @param: url, url to the espn scoreboard page
        @return: dictionary built from the json object found on the page
    """
    page = requests.get(url).text
    # Load scoreboardData json object off of page to parse for information
    json_text = re.search(
        r'window\.espn\.scoreboardData\s*=\s*({.*});window', page).group(1)
    return json.loads(json_text)


def __create_scores_dict(json_data):
    """
        Parses JSON object from ESPN to build a scores dictionary of scores for
        the day

        @param: json_data, the dictionary from ESPN built off the JSON data
        @return: scores, dictionary built from sifting through json_data
    """
    games = json_data['events']
    scores = {}
    for game in games:
        game_id = int(game['id'])
        competition = game['competitions'][0]
        scores[game_id] = {'status': {
            'period': competition['status']['period'],
            'time': competition['status']['displayClock'],
            'description': competition['status']['type']['shortDetail'],
            'state': competition['status']['type']['name']
        }}

        scores[game_id]['teams'] = []

        for team in competition['competitors']:
            # NBA scoreboardData has a ranks array
            if 'ranks' in team:
                rank = team['ranks'][0]['rank']['current']
            # NCAAM has a curated rank field
            elif 'curatedRank' in team:
                rank = team['curatedRank']['current']

            scores[game_id]['teams'].append(
                {
                    'rank': rank,
                    'score': team['score'],
                    'team': team['team']['name'],
                    'location': team['team']['location'],
                    'displayName': team['team']['displayName'],
                    'abbreviation': team['team']['abbreviation'],
                    'record': team['records'][0]['summary'],
                    'winner': team['winner']
                }
            )

    return scores


def __parse_date_option(args=None):
    """
        Parses the date option and returns the date_string to be used by
        ESPN urls

        @param: args, dictionary of arguments and options

        @return: date_string, string date in %Y%m%d format
    """
    if args and 'date' in args['opts']:
        date_obj = datetime.strptime(args['opts']['date'], "%m/%d/%Y")
        date_string = date_obj.strftime("%Y%m%d")
    else:
        date_obj = datetime.now()
        date_string = date_obj.strftime("%Y%m%d")

    return date_string
