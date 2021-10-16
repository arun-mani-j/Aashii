"""Contains handlers for all interactions to the bot."""

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    TypeHandler,
)
from telegram import Update
from Aashii.base.commands import (
    announce_users,
    block_user_cl,
    cancel_announcement,
    delete,
    send_help,
    send_start,
    static_command,
    unblock_user_cl,
    whois,
)
from Aashii.base.callback_query import block_user_cb, connect_admin_cb, unblock_user_cb
from Aashii.bridge.admin import edit_admin_message, forward_to_user
from Aashii.bridge.user import edit_user_message, forward_to_admins
from Aashii.utils.misc import add_user

handlers = {
    CallbackQueryHandler: [
        ({"callback": block_user_cb, "pattern": r"^block$"},),
        ({"callback": connect_admin_cb, "pattern": r"^connect$"},),
        ({"callback": unblock_user_cb, "pattern": r"^unblock$"},),
    ],
    CommandHandler: [
        ({"command": "announce", "callback": announce_users},),
        ({"command": "block", "callback": block_user_cl},),
        ({"command": "cancel", "callback": cancel_announcement},),
        ({"command": "delete", "callback": delete},),
        ({"command": "help", "callback": send_help},),
        ({"command": "start", "callback": send_start},),
        ({"command": "unblock", "callback": unblock_user_cl},),
        ({"command": "whois", "callback": whois},),
    ],
    MessageHandler: [
        ({"filters": Filters.command, "callback": static_command},),
        (
            {
                "filters": Filters.chat_type.groups
                & Filters.reply
                & Filters.update.edited_message,
                "callback": edit_admin_message,
            },
        ),
        (
            {
                "filters": Filters.chat_type.groups,
                "callback": forward_to_user,
            },
        ),
        (
            {
                "filters": Filters.chat_type.private & Filters.update.edited_message,
                "callback": edit_user_message,
            },
        ),
        ({"filters": Filters.chat_type.private, "callback": forward_to_admins},),
    ],
    TypeHandler: [
        ({"type": Update, "callback": add_user}, -1),
    ],
}
