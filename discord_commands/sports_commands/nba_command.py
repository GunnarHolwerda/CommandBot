"""
    Implementation of Sportcommand for NBA Scores
"""
from .sport_command import SportCommand
from discord_commands.command import BaseCommand

class NBACommand(SportCommand, BaseCommand):
    """
        Scrapes ESPN.com for NBA scores and prints out all scores for the day

        Required arguments: None

        Supported options:
            $date=value (value must follow %m/%d/%Y format)
    """
    def __init__(self, command_str):
        super(NBACommand, self).__init__(command_str)
        #super(NBACommand, self).__init__()
        self._espn_url = "http://espn.go.com/nba/scoreboard/_/"
        self._command = "!nba"



    def run(self):
        date_string = super(NBACommand, self)._parse_date_option()
        date_url = "date/{}".format(date_string)

        data = super(NBACommand, self)._extract_espn_json_scoreboard_data(date_url=date_url)
        scores = SportCommand._create_scores_dict(data)

        msg = SportCommand._generate_score_printout(scores)

        return msg
