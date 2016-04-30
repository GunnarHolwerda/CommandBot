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

    def __init__(self, message):
        super(SpotifySearchCommand, self).__init__(message)
        self._command = "!song"
        self._search_type = "track"

    def validate(self):
        if 'type' in self._opts:
            if self._opts['type'] in SpotifySearchCommand.SUPPORTED_SEARCH_TYPES:
                self._search_type = self._opts['type']
            else:
                return False, "Unknown search type specified {}. " \
                              "Known types: track (default), artist, album, playlist.".format(self._opts['type'])
        return True, "OK"

    def run(self):
        query = self._command_str

        results = self._spotify.search(query, limit=1, type=self._search_type)
        items = results[self._search_type + "s"]['items']
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

    @staticmethod
    def info():
        return "Searches Spotify for the song and returns a link to the song"
