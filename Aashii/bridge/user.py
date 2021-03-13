from time import sleep
from telegram import ChatAction, Update
from telegram.ext import CallbackContext
from Aashii.constants import Literal
from Aashii.utils.wrappers import check_user_status


@check_user_status
def forward_to_admins(update: Update, context: CallbackContext):

    """
    Sends the user's message to admins.
    """

    database = context.bot_data["database"]
    user_id = update.message.from_user.id
    context.bot.send_chat_action(
        chat_id=Literal.ADMINS_GROUP_ID, action=ChatAction.TYPING
    )
    sleep(Literal.DELAY_SECONDS)
    message = update.message.forward(Literal.ADMINS_GROUP_ID)
    database.add_message(message.message_id, user_id)
