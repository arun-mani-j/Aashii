# Aashii

_Aashii_ is a simple and yet powerful bot to help members contact admins of a group in Telegram.

# Commands

Except `/cancel`, `/help` and `/start`, all other commands require it to be a reply to a message. For the commands `/block`, `/unblock`, `/whois`, you can either pass a user ID or reply it to a message from the bot.

- /announce - Sends the quoted message to all subscribers of bot.
- /block - Blocks the user from contacting the admins, you can also give the user ID to be blocked.
- /cancel - Cancels the announcement in progress.
- /delete - Deletes the message of admins in users side.
- /help - Sends the help message.
- /start - Starts the bot.
- /unblock - Unblocks the user, you can also give the user ID to be unblocked.
- /whois - Gives details about the user of given user ID or sender of quoted message.

# Usage

Members just need to start the bot and casually message it. The messages will be sent to admins group.
Admins reply to messages of users and this gets sent to users. If your message is reply to any admins message, it won't sent to users unless you prefix your message with `REPLY_CHARACTER`, which is by default `!`.
That is, if you reply to an admins with `!` at start, then that message will be sent to users (of course with `!` removed).

There is `/delete` command to delete any message you sent to users by mistake.

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
6. Start the bot using `python3 -m Aashii`.

# Environment Variables

| Name                  | Description                                                            | Default    |
| --------------------- | ---------------------------------------------------------------------- | ---------- |
| ADMINS_GROUP_ID       | Admins group ID.⁽¹⁾                                                    | -          |
| ANNOUNCEMENT_INTERVAL | The delay seconds between announcing messages to each user.            | 0.5        |
| CHAT_GROUP_ID         | Chat group ID.⁽¹⁾                                                      | -          |
| DATABASE_URL          | Database connection URL to connect to PostgreSQL server.⁽¹⁾            | -          |
| DELAY_SECONDS         | The delay seconds between forward of message between users and admins. | 1          |
| GROUP_NAME            | Name of the group the bot represents.                                  | Illuminati |
| INFORM_ERROR          | Errors will be reported in admins group if `TRUE`.                     | TRUE       |
| LISTEN                | The URL to listen for webhooks.                                        | -          |
| LOG_FILE              | The file to log errors.                                                | -          |
| POLL_INTERVAL         | The interval between subsequent polling.                               | 1          |
| PORT                  | The port to listen for webhooks.                                       | 0          |
| REPLY_CHARACTER       | Only messages with this character prepended will be sent to users.     | !          |
| STEP                  | Number of divisions at which the announcement statistics is updated.   | 10         |
| TOKEN                 | Token of the bot.⁽¹⁾                                                   | -          |
| TRACEBACK_VALUE       | The depth of error description.                                        | 5          |
| URL                   | The base URL for webhooks without trailing `/`.                        | -          |

## Notes

1. Highly required.
2. The bot has to be a member of admins group and chat group.
3. If webhook parameters are not available, the bot will use long polling method.
4. If `INFORM_ERROR` is `TRUE`, there won't be any effect of `LOG_FILE`.
5. `STEP` indicates on what value an announcement progress is updated. A value of `10` will make the bot update the details when the progress reaches 10%, 20% … 90% progress.

# Thank You
