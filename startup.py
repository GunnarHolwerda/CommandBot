"""
    Startup.py script that is ran when the client gets initialized used to persist settings
    accross restarts
"""

from command_dispatcher import run_command
from discord import Message, Server

def startup():
    """	This method is ran when DiscordBot is started """
    print("Initializing saved commands")
    msg = Message(content="!alias !d !dankmemes")
    msg.server = Server(id='108769127627280384')
    run_command(msg)
    msg = Message(content="!alias !cf !cowsay $fortune=True")
    msg.server = Server(id='108769127627280384')
    run_command(msg)
