"""
    Implementation of Sportcommand for NCAAM Basketball Scores
"""
from .sport_command import SportCommand
from discord_commands.command import BaseCommand


class NCAAMCommand(BaseCommand, SportCommand):
    """
        Scrapes ESPN.com for NCAAM scores and prints out all scores for the day

        Required arguments: None

        Supported options:
            $date=value (value must follow %m/%d/%Y format)
    """
    def __init__(self, command_str):
        super(NCAAMCommand, self).__init__(command_str)
        self._command = "!ncaam"
        self._espn_url = "http://espn.go.com/mens-college-basketball/scoreboard/_/"

    def run(self):
        date_string = super(NCAAMCommand, self)._parse_date_option()
        date_url = "date/{}".format(date_string)

        data = super(NCAAMCommand, self)._extract_espn_json_scoreboard_data(date_url=date_url)
        scores = SportCommand._create_scores_dict(data)

        msg = SportCommand._generate_score_printout(scores)

        return msg
