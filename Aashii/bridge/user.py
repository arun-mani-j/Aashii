from telegram import ChatAction, Update
from telegram.ext import CallbackContext
from Aashii.constants import Literal
from Aashii.utils.wrappers import check_user_status


def __send_admins(context: CallbackContext):

    database = context.bot_data["database"]
    message = context.job.context
    user_id = message.from_user.id
    message = message.forward(Literal.ADMINS_GROUP_ID)
    database.add_message(message.message_id, user_id)


@check_user_status
def forward_to_admins(update: Update, context: CallbackContext):

    """
    Sends the user's message to admins.
    """

    context.bot.send_chat_action(
        chat_id=Literal.ADMINS_GROUP_ID, action=ChatAction.TYPING
    )
    context.job_queue.run_once(
        callback=__send_admins, when=Literal.DELAY_SECONDS, context=update.message
    )
