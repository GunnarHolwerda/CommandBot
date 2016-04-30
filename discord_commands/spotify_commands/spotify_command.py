"""
    Abstract class for a Spotify Command that all spotify commands will
    extend
"""
import spotipy


class SpotifyCommand:
    """
        Abstract class for all SpotifyCommands
    """

    def __init__(self, message):
        super(SpotifyCommand, self).__init__(message)
        self._spotify = spotipy.Spotify()
