"""
    Houses a dictionary holding references to every command available
"""
from .help_command.help_command import HelpCommand
from .butts_command.butts_command import ButtCommand
from .cowsay_command.cowsay_command import CowSayCommand
from .dankmemes_command.dankmemes_command import DankMemesCommand
from .sports_commands.nba_command import NBACommand
from .sports_commands.ncaam_command import NCAAMCommand
from .spotify_commands.spotify_search_command import SpotifySearchCommand


commands = {
    '!nba': NBACommand,
    '!ncaam': NCAAMCommand,
    '!dankmemes': DankMemesCommand,
    '!cowsay': CowSayCommand,
    '!butt': ButtCommand,
    '!song': SpotifySearchCommand,
    '!help': HelpCommand
}
