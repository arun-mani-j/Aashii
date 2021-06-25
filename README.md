# Aashii

_Aashii_ is a simple bot to help members contact admins of a group in Telegram.

# Commands

- /announce - Sends the message to all subscribers of bot.
- /block - Blocks the user from contacting the admins, you can also give the user ID to be blocked.
- /cancel - Cancels the announcement in progress.
- /help - Sends the help message.
- /start - Starts the bot.
- /unblock - Unblocks the user, you can also give the user ID to be unblocked.

# Static Commands

You can add simple text sending commands dynamically to the bot.
All you have to do is, create a file inside `data/static` with the name of command as filename.
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

| Name                  | Description                                                          |
| --------------------- | --------------------------------------------------------------       |
| ADMINS_GROUP_ID       | Admins group ID.⁽¹⁾                                                  |
| ANNOUNCEMENT_INTERVAL | The delay between announcing messages to each user.                  |
| BOT_TOKEN             | Token of the bot.⁽¹⁾                                                 |
| CHAT_GROUP_ID         | Chat group ID.⁽¹⁾                                                    |
| DATABASE_URL          | Database connection URL to connect to PostgreSQL server.⁽¹⁾          |
| DELAY_SECONDS         | The delay between forward of message between users and admins.       |
| GROUP_NAME            | Name of the group the bot represents.                                |
| INFORM_ERROR          | Errors will be reported in admins group if `TRUE`.                   |
| LISTEN                | The URL to listen for webhooks.                                      |
| LOG_FILE              | The file to log errors.                                              |
| POLL_INTERVAL         | The interval between subsequent polling.                             |
| PORT                  | The port to listen for webhooks.                                     |
| STEP                  | Number of divisions at which the announcement statistics is updated. |
| TRACEBACK_VALUE       | The depth of error description.                                      |
| URL                   | The base URL for webhooks.                                           |

## Notes

1. Highly required.
2. The bot has to be a member of admins group and chat group.
3. If webhook parameters are not available, the bot will use long polling method.
4. If `INFORM_ERROR` is `TRUE`, there won't be any effect of `LOG_FILE`.
5. `STEP` indicates on what value an announcement progress is updated. A value of `10` will make the bot update the details when the progress reaches 10%, 20% ... 90% progress.

# Thank You
