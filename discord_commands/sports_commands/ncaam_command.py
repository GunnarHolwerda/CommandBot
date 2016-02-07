"""
    Implementation of Sportcommand for NCAAM Basketball Scores
"""
from sport_command import SportCommand
from discord_commands.command import BaseCommand


class NCAAMCommand(BaseCommand, SportCommand):
    """
        Scrapes ESPN.com for NCAAM scores and prints out all scores for the day

        Required arguments: None

        Supported options:
            $date=value (value must follow %m/%d/%Y format)
    """
    def __init__(self, command_str):
        BaseCommand.__init__(self, command_str)
        self.command = "!ncaam"
        SportCommand.__init__(self)
        self.__espn_url = "http://espn.go.com/mens-college-basketball/scoreboard/_/"

    def run(self):
        date_string = BaseCommand.__parse_date_option(self)

        data = SportCommand.__extract_espn_json_scoreboard_data(
            "{}date/{}".format(self.espn_url, date_string))
        scores = SportCommand.__create_scores_dict(data)

        msg = SportCommand.__generate_score_printout(scores)

        return msg
