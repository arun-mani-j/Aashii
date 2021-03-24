from telegram import Update
from telegram.ext import CallbackContext
from Aashii.constants import Message


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


def check_is_reply_to_user_linked_verbose(func):

    """
    Checks if the message is a reply to a message linked to a user
    and warns on otherwise.
    """

    def wrapped(update: Update, context: CallbackContext):

        database = context.bot_data["database"]
        reply = update.message.reply_to_message
        if reply and database.get_user_id(reply.message_id):
            func(update, context)
        else:
            update.message.reply_html(Message.NOT_LINKED)

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
