import os, re
from telegram import BotCommand


def _command(fname):
    cmd = fname
    dsc = _p.sub("", open(f"data/static/{fname}").read(80)) + "..."
    return BotCommand(cmd, dsc)


_p = re.compile("<[^>]*>")
commands = {
    "admins": [
        BotCommand("announce", "Announce all users"),
        BotCommand("block", "Blocks the user"),
        BotCommand("cancel", "Cancels the announcement"),
        BotCommand("unblock", "Unblocks the user"),
    ],
    "all": [
        BotCommand("help", "Help on usage"),
        BotCommand("start", "Start the adventure"),
    ],
    "private": [_command(fname) for fname in os.listdir("data/static")],
}
