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
    def __init__(self, message):
        super(NBACommand, self).__init__(message)
        self._espn_url = "http://espn.go.com/nba/scoreboard/_/"
        self._command = "!nba"

    def run(self):
        date_string = super(NBACommand, self)._parse_date_option()
        date_url = "date/{}".format(date_string)

        data = super(NBACommand, self)._extract_espn_json_scoreboard_data(url_options=date_url)
        scores = SportCommand._create_scores_dict(data, playoff_func=NBACommand.__add_playoff_data)

        msg = SportCommand._generate_score_printout(scores)

        return self.code_wrap(msg)

    @staticmethod
    def help():
        return """
            Scrapes ESPN.com for NBA scores and prints out all scores for the day

            Required arguments: None

            Supported options:
                $date=value (value must follow %m/%d/%Y format)
        """

    @staticmethod
    def info():
        return "Returns NBA scores for a specific date (default is today)"

    @staticmethod
    def __add_playoff_data(json_data):
        """
        This method will get passed to _create_scores_dict so that playoff
        information can be added to the message
        @param json_data: The json data, from root it will be json_data['events']['competitions']
        @return: True if playoff data exists, false otherwise
        """
        return 'series' in json_data
