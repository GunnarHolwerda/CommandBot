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
            $conf=value (value is a 3 letter code for a conference)
    """

    conferences = {
        'all': 50,  # All NCAA Division 1 games
        'a10': 3,   # Atlantic 10 Conference
        'sun': 46,  # Atlantic Sun Conference
        'acc': 2,   # Atlantic Coast Conference
        'ame': 1,   # American East Conference
        'amr': 62,  # American Athletic Conference
        'b12': 8,   # Big 12 Conference
        'est': 4,   # Big East Conference
        'sky': 5,   # Big Sky Conference
        'sth': 6,   # Big South Conference
        'b10': 7,   # Big 10 Conference
        'wst': 9,   # Big West Conference
        'usa': 11,  # Conference USA
        'caa': 10,  # Colonial Athletic Conference
        'hor': 45,  # Horizon Conference
        'ivy': 12,  # Ivy League
        'maa': 13,  # Metro Atlantic Athletic Conference
        'mac': 14,  # Mid-American Conference
        'mea': 16,  # Mid-Eastern Athletic Conference
        'mvc': 18,  # Missouri Valley Conference
        'mwc': 44,  # Mountain West Conference
        'nec': 19,  # Northeast Conference
        'ovc': 20,  # Ohio Valley Conference
        'pac': 21,  # Pac-12 Conference
        'pat': 22,  # Patriot Conference
        'sec': 23,  # South Eastern Conference
        'swa': 26,  # Southwestern Athletic Conference
        'srn': 24,  # Southern Conference
        'lnd': 25,  # Southland Conference
        'smt': 49,  # Summit Conference
        'blt': 27,  # Sun Belt Conference
        'wac': 30,  # Western Athletic Conference
        'wcc': 29   # West Coast Conference
    }

    def __init__(self, message):
        super(NCAAMCommand, self).__init__(message)
        self._command = "!ncaam"
        self._espn_url = "http://espn.go.com/mens-college-basketball/scoreboard/_/"

    def run(self):
        if 'conf' in self._opts:
            conf_url = self.__parse_conference_option(self._opts['conf'])
        else:
            conf_url = ""

        date_string = super(NCAAMCommand, self)._parse_date_option()
        date_url = "date/{}".format(date_string)

        url_options = conf_url + date_url

        data = super(NCAAMCommand, self)._extract_espn_json_scoreboard_data(url_options=url_options)
        scores = SportCommand._create_scores_dict(data)

        msg = SportCommand._generate_score_printout(scores)

        return self.code_wrap(msg)

    @staticmethod
    def help():
        return """
            Scrapes ESPN.com for NCAAM scores and prints out all scores for the day
            defaults to teams in the top 25

            Required arguments: None

            Supported options:
                $date=value (value must follow %m/%d/%Y format)
                $conf=value (value is a 3 letter code for a conference)
                    Most Popular Conference codes:
                        all - All NCAA Division 1 games
                        acc - Atlantic Coast Conference
                        b12 - Big 12 Conference
                        est - Big East Conference
                        b10 - Big 10 Conference
                        pac - Pac-12 Conference

                    ** All conferences supported, but not listed here
        """

    @staticmethod
    def info():
        return "Sends message with NCAAM scores for the date and conference specified (default today and top 25"

    @classmethod
    def __parse_conference_option(cls, conference):
        """
            Based on conference option returns part of url needed
        """
        return "group/" + str(cls.conferences[conference]) + "/"
