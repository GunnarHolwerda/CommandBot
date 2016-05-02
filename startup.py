"""
    Startup.py script that is ran when the client gets initialized used to persist settings
    accross restarts
"""

from discord import Message, Server, User

def startup(dispatcher):
    """
    This method is ran when the bot starts up. Currently used to persist aliases that are created
    @param dispatcher: command_dispatcher.CommandDispatcher
    """
    print("Initializing saved commands")
    msg = Message(content="!alias !d !dankmemes")
    msg.server = Server(id='108769127627280384')
    dispatcher.run_command(msg)
    msg = Message(content="!alias !cf !cowsay $fortune=True")
    msg.server = Server(id='108769127627280384')
    dispatcher.run_command(msg)
    msg = Message(content="!alias !cf !cowsay $fortune=True")
    msg.author = User(id='108768204184113152')
    dispatcher.run_command(msg)
    msg = Message(content="!alias !d !dankmemes")
    msg.author = User(id='108768204184113152')
    dispatcher.run_command(msg)
