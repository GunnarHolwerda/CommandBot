"""
    Implementation of Sportcommand for NCAAM Basketball Scores
"""
from sport_command import SportCommand


class NCAAMCommand(SportCommand):
    """
        Scrapes ESPN.com for NCAAM scores and prints out all scores for the day

        Required arguments: None

        Supported options:
            $date=value (value must follow %m/%d/%Y format)
    """
    def __init__(self, command_str):
        super(NCAAMCommand, self).__init__(command_str)
        self.__espn_url = "http://espn.go.com/mens-college-basketball/scoreboard/_/"
        self.command = "!ncaam"

    def __run__(self):
        date_string = super(NCAAMCommand, self).__parse_date_option()

        data = super(NCAAMCommand, self).__extract_espn_json_scoreboard_data(
            "{}date/{}".format(self.espn_url, date_string))
        scores = super(NCAAMCommand, self).__create_scores_dict(data)

        msg = super(NCAAMCommand, self).__generate_score_printout(scores)

        return msg
