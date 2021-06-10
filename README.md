# Aashii

_Aashii_ is a simple bot to help members contact admins of a group in Telegram.

# Commands

- /announce - Sends the message to all subscribers of bot.
- /block - Blocks the user from contacting the admins.
- /cancel - Cancels the announcement in progress.
- /help - Sends the help message.
- /start - Starts the bot.
- /unblock - Unblocks the user.

# Static Commands

You can add simple text sending commands dynamically to the bot.
All you have to do is, create a file inside <code>data/static</code> with the name of command as filename.
The bot will send the contents of that file whenever user sends that command.
The file can be formatted using HTML.

# Deployment

1. Clone the source code and make it your current directory.
2. Setup [PostgreSQL](https://www.postgresql.org) in your server.
3. Install the requirements specified in `requirements.txt`.
4. Fill the environment variables.
5. Execute `psql -f data/schema.sql` to initialize tables.
6. Start the bot using `python3 -m Aashi`.

# Environment Variables

| Name                  | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| ADMINS_GROUP_ID       | Admins group ID.                                               |
| ANNOUNCEMENT_INTERVAL | The delay between announcing messages to each user.            |
| BOT_TOKEN             | Token of the bot.                                              |
| CHAT_GROUP_ID         | Chat group ID.                                                 |
| DATABASE_URL          | Database connection URL to connect to PostgreSQL server.       |
| DELAY_SECONDS         | The delay between forward of message between users and admins. |
| GROUP_NAME            | Name of the group the bot represents.                          |
| LISTEN                | The URL to listen for webhooks.                                |
| POLL_INTERVAL         | The interval between subsequent polling.                       |
| PORT                  | The port to listen for webhooks.                               |
| URL                   | The base URL for webhooks.                                     |

## Notes

1. The bot has to be a member of admins group and chat group.
2. If webhook parameters are not available, the bot will use long polling method.

# Thank You
