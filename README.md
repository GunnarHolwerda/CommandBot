# PyDiscordClient
A Python3.4 program that can be run in the background to add additional commands to your Discord Server.

# Setup
Make sure you are using Python 3.4 when installing packages and running commands.

#### Install all required packages using pip from `requirements.txt`

`$ pip3 install /path/to/requirements.txt`

#### Edit user.py

Edit `user.py` to include your username and password for your Discord Account. Feel free to create a new account and put their credentials in the file, just make sure they have accepted an invite to your server.

#### Run the client
To run the client:
`$ python3 custom_discord.py`

Or you can make custom_discord.py executable and run it that way too.

If you want the command to run in the background and be able to close the terminal window you run it in:

`$ chmod +x /path/to/custom_discord.py`

`$ nohup ./custom_discord.py &`

In order to kill the command after running it with nohup, use `$ ps -ef | grep python3` to find the process id of the program and then kill it using `kill -9 <pid>`.

NOTE: All commands here are given to be run on a linux system.

# Supported Commands
Arguments are required text for the Commands
Options are optional and passed in via the format:
`$option=value`


`!code <words>`
##### Arguments
*   words, is any text

##### Options
*   None

##### Description
*   Wraps the words in ``` to format the text as code

`!butt <words>`
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

# Notes
I work on this in my free time and would love to hear suggestions you have for other commands you would like.

## My short list of things todo include:
*   Create NCAACommand to have a NCAAMCommand extend from so that I can include the conference information in other college athletic commands that I may add
*   Delete the command message that has been sent
*   Add ability for commands to have a short option (i.e. !dankmemes could also be used as !dank or !d, etc)
*   Create a refresh script that will parse all commands in discord_commands and build all_commands.py from that, so that any new command added, doesn't need to be manually added.


# Development
If you would like to help develop for this project feel free!

The current way to add a command would be to add a file or folder to discord_commands.

Make sure your command extends `BaseCommand` defined in command.py as that class takes care of parsing options and arguments

Implement the `run` and static 'help' method on your command and have it return the string for the message that will be sent and the help text to be displayed when !help is called.

Import your command into all_commands.py and add an entry in the commands dictionary with your command as the key and your class name as the value.
