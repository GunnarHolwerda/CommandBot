"""
    Implementation of Sportcommand for NBA Scores
"""
from . import SportCommand


class NBACommand(SportCommand):
    """
        Scrapes ESPN.com for NBA scores and prints out all scores for the day

        Required arguments: None

        Supported options:
            $date=value (value must follow %m/%d/%Y format)
    """
    def __init__(self, command_str):
        super(NBACommand, self).__init__(command_str)
        self.__espn_url = "http://espn.go.com/nba/scoreboard/_/"
        self.command = "!nba"


    def __run__(self):
        date_string = super(NBACommand, self).__parse_date_option()

        data = super(NBACommand, self).__extract_espn_json_scoreboard_data(
            "{}date/{}".format(self.espn_url, date_string))
        scores = super(NBACommand, self).__create_scores_dict(data)

        msg = super(NBACommand, self).__generate_score_printout(scores)

        return msg
