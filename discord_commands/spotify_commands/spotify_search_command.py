"""
    Implementation of SpotifyCommand for Searching spotify
"""

from .spotify_command import SpotifyCommand
from discord_commands.command import BaseCommand

class SpotifySearchCommand(SpotifyCommand, BaseCommand):
    """
        Searches Spotify for a value and returns a link to the first result

        Required arguments:
            String to search for (track name)

        Supported options:
            $type=value (Type of search: artist, track, album, playlist)
    """

    SUPPORTED_SEARCH_TYPES = ['artist', 'track', 'album', 'playlist']

    def __init__(self, command_str):
        super(SpotifySearchCommand, self).__init__(command_str)
        self._command = "!song"

    def run(self):
        if 'type' in self._opts:
            if self._opts['type'] in SpotifySearchCommand.SUPPORTED_SEARCH_TYPES:
                search_type = self._opts['type']
            else:
                return "Unknown type specified\n" + self.help()
        else:
            search_type = 'track'

        query = self._command_str

        results = self._spotify.search(query, limit=1, type=search_type)
        items = results[search_type + "s"]['items']
        if len(items) > 0:
            item = items[0]
            url = item['external_urls']['spotify']
        else:
            url = "No results found."

        return url

    @staticmethod
    def help():
        return """
            Searches Spotify for a value and returns a link to the first result

            Required arguments:
                String to search for (track name)

            Supported options:
                $type=value (Type of search: artist, track, album, playlist)
        """
