"""
    Abstract class for a Spotify Command that all spotify commands will
    extend
"""
import spotipy


class SpotifyCommand:
    """
        Abstract class for all SpotifyCommands
    """

    def __init__(self, command_str):
        super(SpotifyCommand, self).__init__(command_str)
        self._spotify = spotipy.Spotify()
