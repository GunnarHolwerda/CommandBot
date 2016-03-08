"""
    Startup.py script that is ran when the client gets initialized used to persist settings
    accross restarts
"""

from command_dispatcher import run_command

def startup():
    """	This method is ran when DiscordBot is started """
    print("Initializing saved commands")
