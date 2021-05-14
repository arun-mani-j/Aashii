from time import sleep
from telegram import ChatAction, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext
from Aashii.constants import Literal
from Aashii.utils.wrappers import (
    check_is_blocked_by_user,
    check_is_reply_to_user_linked_silent,
)


@check_is_reply_to_user_linked_silent
@check_is_blocked_by_user
def forward_to_user(update: Update, context: CallbackContext):

    """
    Sends the message from admins to the user.
    """

    database = context.bot_data["database"]
    message_id = update.message.reply_to_message.message_id
    user_id = database.get_user_id(message_id)
    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    sleep(Literal.DELAY_SECONDS)
    update.message.copy(user_id)
