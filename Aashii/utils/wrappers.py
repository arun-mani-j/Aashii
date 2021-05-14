from telegram import Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext
from Aashii.constants import Message


def check_is_blocked_by_user(func):

    """
    Checks if the bot is blocked by the user.
    """

    def wrapped(update: Update, context: CallbackContext):

        database = context.bot_data["database"]

        try:
            func(update, context)
        except Unauthorized:
            message = (
                update.callback_query.message
                if update.callback_query
                else update.message
            )
            user_message_id = (
                update.callback_query.message.message_id
                if update.callback_query
                else update.message.reply_to_message.message_id
            )
            user_id = database.get_user_id(user_message_id)
            full_name = database.get_user_full_name(user_id)
            text = Message.BLOCKED_BY_USER.format(USER_ID=user_id, FULL_NAME=full_name)
            message = message.reply_html(text)
            database.add_message(message.message_id, user_id)

    return wrapped


def check_is_group_command(func):

    """
    Checks if the command is sent in group.
    """

    def wrapped(update: Update, context: CallbackContext):

        if update.message.chat.type != update.message.chat.PRIVATE:
            func(update, context)
        else:
            update.message.reply_html(Message.NOT_PRIVATE_COMMAND)

    return wrapped


def check_is_reply_to_user_linked_silent(func):

    """
    Checks if the message is a reply to a message linked to a user
    and doesn't shout on otherwise.
    """

    def wrapped(update: Update, context: CallbackContext):

        database = context.bot_data["database"]
        reply = update.message.reply_to_message
        if reply and database.get_user_id(reply.message_id):
            func(update, context)

    return wrapped


def check_is_reply_verbose(func):

    """
    Checks if the message is a reply to any message
    and warns on otherwise.
    """

    def wrapped(update: Update, context: CallbackContext):

        reply = update.message.reply_to_message
        if reply:
            func(update, context)
        else:
            update.message.reply_html(Message.INVALID_REPLY)

    return wrapped


def check_user_status(func):

    """
    Checks if the user is blocked and ignores the message if they are.
    """

    def wrapped(update: Update, context: CallbackContext):

        database = context.bot_data["database"]
        chat = update.message.chat
        user_id = update.message.from_user.id

        if chat.type == chat.PRIVATE and database.get_user_status(user_id):
            update.message.reply_html(Message.BLOCKED_USER_STATUS)
        else:
            func(update, context)

    return wrapped
