# Tag Bot
This bot tags discord posts that contain links with keywords on the webpage.

## Manually adding a Discord bot to your server
Visit the [Discord Developers page](https://discord.com/developers), select your server, and create a new application.

On the application's settings, go to the bot page and add a new bot. If your name is too similar to other bots such as "test bot", you will be rejected and have to change the name.

Once the bot is created, set "**Send Messages**" and "**Manage Messages**" in the permissions. The permissions integer is 10240.

You can find your token by the bot icon. Click the reveal button or copy it with the button. The Tag Bot can now be linked to your server. See the sections below to start the bot.

# Running the bot
The bot can be run manually or from a Docker container.

## Docker
### Requirements
- [Docker](https://www.docker.com/get-started)
- [Discord API token](https://discord.com/developers)

Pull the image from dockerhub.
```
docker pull orionhumphrey/tagbot-slim
```
Use the -e tag with your discord token to set the BOT_API_TOKEN environment variable.

To start the bot for the first time, run:
```
docker run --name Tagbot -d -e BOT_API_TOKEN=YourTokenHere orionhumphrey/tagbot-slim
```
You should now see the bot in your server. See Usage section below to get started with Tag Bot.

## Manual
### Requirements
- [Python 3](https://www.python.org/downloads/)
- Pip (Comes with Python)
- [Discord API token](https://discord.com/developers)

Navigate to program directory in a terminal and run the below command to install the required Python packages.
```
pip install -r requirements.txt
```
### Adding your token to the environment
The bot can automatically pull the API token from the computers environment variables or from a .env file.

Set variable name to **BOT_API_TOKEN**, and set variable value to **YourTokenHere**.

Here are resources for manually setting environment variables:
- [Windows](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0)
- [Linux](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
- [Mac](https://phoenixnap.com/kb/set-environment-variable-mac)

The program can also pull a variable from a .env file in the program directory.

In the program directory, create a file with no name and the extension as .env. Inside, set **BOT_API_TOKEN=YourTokenHere**.

To start the bot, navigate to the program directory in a terminal and run:
```
python bot.py
```
You should now see the bot in your server. Closing the terminal will shutdown the bot. See Usage section below to get started with Tag Bot.


## Usage


Reply to a message that contains a link with !tag to generated tags for that webpage.

The command must be used in a reply.

The message replied to must contain a link.

### Logs
Log handling can be edited in the code.
There are two log handlers. One for logging to a file and one for logging to stdout. You will not see stdout logs if running  Logs will be stored in bot.log in the program directory.
