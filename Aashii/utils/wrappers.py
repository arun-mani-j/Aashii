"""Wrappers for various handlers."""

from telegram import Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext
from Aashii.constants import Literal, Message
from Aashii.utils.misc import get_user_src_message


def check_is_blocked_by_user(func):
    """Check if the bot is blocked by the user."""

    def wrapped(update: Update, context: CallbackContext):
        database = context.bot_data["database"]

        try:
            func(update, context)
        except Unauthorized:
            user_id, _ = get_user_src_message(update, context)
            full_name = database.get_user_full_name(user_id)
            text = Message.BLOCKED_BY_USER.format(USER_ID=user_id, FULL_NAME=full_name)
            msg = update.effective_message.reply_html(text)
            database.add_user_message(1, user_id, msg.message_id)

        context.bot_data["lastUserId"] = Literal.ADMINS_GROUP_ID

    return wrapped


def check_is_group_command(func):
    """Check if the command is sent in group."""

    def wrapped(update: Update, context: CallbackContext):
        message = update.edited_message or update.message
        if message.chat.type != message.chat.PRIVATE:
            func(update, context)
            context.bot_data["lastUserId"] = Literal.ADMINS_GROUP_ID
        else:
            message.reply_html(Message.NOT_PRIVATE_COMMAND)

    return wrapped


def check_is_reply_to_user_linked_silent(func):
    """Check if the message is a reply to a message linked to a user and\
    not shout on otherwise."""

    def wrapped(update: Update, context: CallbackContext):
        user_id, _ = get_user_src_message(update, context)
        if user_id:
            func(update, context)

    return wrapped


def check_is_reply_verbose(func):
    """Check if the message is a reply to any message and warns on otherwise."""

    def wrapped(update: Update, context: CallbackContext):
        message = update.edited_message or update.message
        reply = message.reply_to_message
        if reply:
            func(update, context)
        else:
            update.message.reply_html(Message.INVALID_REPLY)

    return wrapped


def check_user_status(func):
    """Check if the user is blocked and ignores the message if they are."""

    def wrapped(update: Update, context: CallbackContext):
        database = context.bot_data["database"]
        message = update.edited_message or update.message
        chat = message.chat
        user_id = message.from_user.id

        if chat.type == chat.PRIVATE and database.get_user_blocked(user_id):
            message.reply_html(Message.BLOCKED_USER_STATUS)
        else:
            func(update, context)

    return wrapped
