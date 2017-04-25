# Discord Bot Framework
This is a python framework that can be used to create Discord bots and their commands

# Setup
Make sure you are using Python 3.4 when installing packages and running commands.

#### Install all required packages using pip from `requirements.txt`

`$ pip3 install /path/to/requirements.txt`

#### Run the client
To run the client:
`$ python3 discord_bot.py`

If you want the command to run in the background and be able to close the terminal window you run it in:

`$ chmod +x /path/to/discord_bot.py`

`$ ./discord_bot.py -t <your_bot_token>`

You will need to create a bot token if you are going to run this bot on your own. They can be created through [Discord's Official API page](https://discordapp.com/developers/applications/me/create)

# Initial Setup
1. Download and extract or clone the project
2. run `python3 discord_bot.py -t <token>` and input your token
3. The bot is now running with all of the built in commands!

# Documentation
If you would like to help develop for this project feel free!

#### How to add a command
1. Create a folder in the discord_commands folder
2. In the folder place an `__init__.py` and
`<your_command>_command.py`.  
3. Create a class in `<your_command>_command.py` that extends BaseCommand  
4. Implement the `run`, `help`, and `validate` functions from BaseCommand (You can skip validate if no validation needs to be done)  
5. In your `__init__.py` include a line:  
`from .<your_command>_command import <CommmandClassName>`
6. Run `python3 discord_bot.py -u` to run the script that builds the list of commands the server will run

#### Run a command at startup
If you want your command to persist across restarts of the Bot, you will call `self._write_to_startup()`, this will write out the function as it was called to `startup.py`.

#### Sports Commands
The sports commands use scraping and regex to parse the scoreboard page of ESPN to build the scores data. If you extend the SportCommand class, you will need to set the `_espn_url` property to the url to the scoreboard of your sport.

#### The Alias Command
The alias command allows you to create commands out of commands and their options. When this is called it will create a new command, that will call an existing command with options or anything.

# Notes
I worked on this project in my free time, and have since not been able to work much on it. Feel free to fork, ask for features, and create pull requests of your own!

## Built In Commands
Arguments are required text for the Commands
Options are optional and passed in via the format:
`$option=value`


`!code <words>`
##### Arguments
*   words, is any text

##### Options
*   None

##### Description
*   Wraps the words in \`\`\` to format the text as code

`!replace <words>`
##### Arguments
*   words, is any text

##### Options
*   $replace, Specify the string to be replaced with butts in words

##### Description
*   Replaces up to 5 distinct words in the text passed with the word 'butts'


`!dankmemes <words>`
##### Arguments
*   words, is any text

##### Options
*   $space, if passed as 'true' will place a space between each letter of the text passed

##### Description
*   Prints the passed text in the following format:

When passed 'what' would print:
```
WHAT
H
A
T
```

`!nba`
##### Arguments
*   None

##### Options
*   $date, specify date in M/D/Y format (1/23/2016) to print the games for that day

##### Description
*   Prints all upcoming, in progress, and finished NBA games for the current day. Includes scores, quarter, and time left in quarter

`!ncaam`
##### Arguments
*   None

##### Options
*   $date, specify date in M/D/Y format (1/23/2016) to print the games for that day
*   $conf, specify conference based on 3 letter conference code, conference code can be found in discord_commands/sports_commands/ncaam_command.py (Defaults to the top 25, when conference specified, all games are listed)

##### Description
*   Prints all upcoming, in progress, and finished NCAAM games for the current day and top 25. Includes scores, quarter, and time left in quarter


`!song <query>`
##### Arguments
*   query, the query to search for (song title, artist, etc)

##### Options
*   $type, specify type of search (default = track), all options: track, artist, playlist, album

##### Description
*   Returns url to first result from the Spotify search, if you want the link to open in the Desktop client instead of the web refer to: [Open Spotify Links With Desktop Client](https://support.spotify.com/us/learn-more/faq/#!/article/why-do-spotify-links-always-open-in-the-spotify-web-player)

`!cowsay <words>`
##### Arguments
*   words, the words for the cow to say, if more than one word, wrap in quotes

##### Options
*   None

##### Description
*   Prints out a cow saying whatever words you passed it.

`!help <command>`
##### Arguments
*   command, command (i.e. !dankmemes) to get the help text for, if no command
    is passed all commands on the system will be printed out in a list

##### Options
*   None

##### Description
*   Prints out help text for a specified command

`!alias <alias> <command>`
##### Arguments
*   alias, the alias to set for the command
*   command, command (i.e. !dankmemes) to set the alias for

##### Options
*   $persist, boolean (True or False) if set to False will not save the alias to be created when the bot restarts, defaults to True

##### Description
*   Creates an alias for an existing command
