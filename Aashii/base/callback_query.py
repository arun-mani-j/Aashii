from telegram import InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from Aashii.constants import Button, Message


def block_user_cb(update: Update, context: CallbackContext):

    """
    Blocks the user for the incoming callback query.
    """

    database = context.bot_data["database"]
    message = update.callback_query.message
    user_id = database.get_user_id(message.message_id)
    full_name = database.get_user_full_name(user_id)
    text = Message.BLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    markup = InlineKeyboardMarkup.from_row([Button.CONNECT, Button.UNBLOCK])

    database.set_user_status(user_id, True)
    update.callback_query.answer()
    message.edit_reply_markup(markup)
    message = message.reply_html(text)
    database.add_message(message.message_id, user_id)
    context.bot.send_message(
        chat_id=user_id, text=Message.BLOCKED_USER_STATUS, parse_mode=ParseMode.HTML
    )


def connect_admin_cb(update: Update, context: CallbackContext):

    """
    Connects the admin with the user.
    """

    database = context.bot_data["database"]
    message = update.callback_query.message
    admin_id = update.callback_query.from_user.id
    admin_name = update.callback_query.from_user.full_name
    user_id = database.get_user_id(message.message_id)
    full_name = database.get_user_full_name(user_id)
    text = Message.ADMIN_CONNECTED.format(
        ADMIN_ID=admin_id,
        ADMIN_FULL_NAME=admin_name,
        USER_ID=user_id,
        USER_FULL_NAME=full_name,
    )
    update.callback_query.answer()
    message = message.reply_html(text)
    database.add_message(message.message_id, user_id)
    context.bot.send_message(
        chat_id=user_id, text=Message.ADMIN_CONNECTED_STATUS, parse_mode=ParseMode.HTML
    )


def unblock_user_cb(update: Update, context: CallbackContext):

    """
    Unblocks the user for the incoming callback query.
    """

    database = context.bot_data["database"]
    message = update.callback_query.message
    user_id = database.get_user_id(message.message_id)
    full_name = database.get_user_full_name(user_id)
    text = Message.UNBLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    markup = InlineKeyboardMarkup.from_row([Button.BLOCK, Button.CONNECT])

    database.set_user_status(user_id, False)
    update.callback_query.answer()
    message.edit_reply_markup(markup)
    message = message.reply_html(text)
    database.add_message(message.message_id, user_id)
    context.bot.send_message(
        chat_id=user_id, text=Message.UNBLOCKED_USER_STATUS, parse_mode=ParseMode.HTML
    )
