from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler
from .base.commands import (
    announce_users,
    block_user_cl,
    cancel_announcement,
    send_help,
    send_start,
    static_command,
    unblock_user_cl,
)
from .base.callback_query import block_user_cb, connect_admin_cb, unblock_user_cb
from .bridge.admin import forward_to_user
from .bridge.user import forward_to_admins

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
        ({"command": "help", "callback": send_help},),
        ({"command": "start", "callback": send_start},),
        ({"command": "unblock", "callback": unblock_user_cl},),
    ],
    MessageHandler: [
        ({"filters": Filters.command, "callback": static_command},),
        (
            {
                "filters": Filters.chat_type.groups & Filters.reply,
                "callback": forward_to_user,
            },
        ),
        ({"filters": Filters.chat_type.private, "callback": forward_to_admins},),
    ],
}
