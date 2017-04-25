"""
    Startup.py script that is ran when the client gets initialized used to persist settings
    accross restarts
"""

from discord import Message, Server, User
import logging

logger = logging.getLogger('command-bot')

def startup(dispatcher):
    """
    This method is ran when the bot starts up. Currently used to persist aliases that are created
    @param dispatcher: command_dispatcher.CommandDispatcher
    """
    logger.info("Initializing saved commands")
