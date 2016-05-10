"""
    Abstract class for a Sports Command that all sports commands will
    extend
"""
import json
import requests
import re
import logging

logger = logging.getLogger('command-bot')


class SportCommand:
    """
        Abstract class for all SportCommands
    """
    # ESPN GAME STATE CONSTANTS
    ESPN_GAME_NOT_STARTED = "STATUS_SCHEDULED"
    ESPN_GAME_IN_PROGRESS = "STATUS_IN_PROGRESS"
    ESPN_GAME_HALFTIME = "STATUS_HALFTIME"
    ESPN_GAME_FINISHED = "STATUS_FINAL"

    def __init__(self, message):
        super(SportCommand, self).__init__(message)
        #print("Initializing SportCommand")
        self._espn_url = ""

    # SportCommand methods
    def _extract_espn_json_scoreboard_data(self, url_options=None):
        """
            Extracts JSON object from ESPN scoreboard page and returns as a json
            object
            @return: dictionary built from the json object found on the page
        """
        url = self._espn_url + url_options
        page = requests.get(url).text

        # Load scoreboardData json object off of page to parse for information
        json_text = re.search(
            r'window\.espn\.scoreboardData\s*=\s*({.*});window', page).group(1)

        logger.info("Received game information: %s", json_text)

        json_data = json.loads(json_text)

        return json_data

    @staticmethod
    def _create_scores_dict(json_data, playoff_func=None):
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

            if playoff_func and playoff_func(competition):
                scores[game_id]['playoffs'] = competition['series']['summary']

            scores[game_id]['teams'] = []

            for team in competition['competitors']:
                # NBA scoreboardData has a ranks array
                if 'ranks' in team:
                    rank = team['ranks'][0]['rank']['current']
                # NCAAM has a curated rank field
                elif 'curatedRank' in team:
                    rank = team['curatedRank']['current']
                else:
                    rank = 'N\\A'

                team_dict = {
                    'rank': rank,
                    'score': team['score'],
                    'team': team['team']['name'],
                    'location': team['team']['location'],
                    'displayName': team['team']['displayName'],
                    'abbreviation': team['team']['abbreviation'],
                    'winner': team['winner']
                }

                # For unknown teams, records aren't kept and are None
                if team['records']:
                    team_dict['record'] = team['records'][0]['summary']

                scores[game_id]['teams'].append(team_dict)

        return scores

    @classmethod
    def _generate_score_printout(cls, scores):
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
            if game_state == SportCommand.ESPN_GAME_FINISHED:
                if team_one['winner']:
                    team_two['abbreviation'] = team_two['abbreviation'].lower()
                elif team_two['winner']:
                    team_one['abbreviation'] = team_one['abbreviation'].lower()

            score_str = "{:<4} vs {:<4} ... {:<3}-{:>3} {}".format(team_one['abbreviation'],
                                                                   team_two['abbreviation'],
                                                                   team_one['score'],
                                                                   team_two['score'],
                                                                   score['status']['description'])

            if 'playoffs' in score:
                score_str += " {}".format(score['playoffs'])

            score_str += "\n"
            if game_state == cls.ESPN_GAME_FINISHED:
                final_scores += score_str
            elif game_state == cls.ESPN_GAME_IN_PROGRESS or game_state == cls.ESPN_GAME_HALFTIME:
                in_progress += score_str
            else:
                not_started += score_str

        return not_started + "\n" + in_progress + "\n" + final_scores
