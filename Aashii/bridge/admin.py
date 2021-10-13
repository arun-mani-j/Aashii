"""Contains functions to send messages from admins to users."""

from telegram import ChatAction, Update
from telegram.ext import CallbackContext
from Aashii.constants import Literal
from Aashii.utils.misc import get_user_src_message
from Aashii.utils.transfer import send_edited_message, send_message
from Aashii.utils.wrappers import check_is_blocked_by_user


def _send_users(context: CallbackContext):
    database = context.bot_data["database"]
    update, user_id, reply_to = context.job.context
    message = update.message
    dest_msg_ids = send_message(context.bot, message, user_id, reply_to, True, False)
    database.add_admin_message(message.message_id, user_id, dest_msg_ids[0])


@check_is_blocked_by_user
def edit_admin_message(update: Update, context: CallbackContext):
    """Edit the message of admins sent to user."""
    database = context.bot_data["database"]
    user_id = update.edited_message.from_user.id
    message_id = update.edited_message.message_id
    user_id, dest_message_id = database.get_user_dest_message_id_from_admins(message_id)

    if not user_id:
        return

    send_edited_message(
        context.bot, update.edited_message, dest_message_id, user_id, False
    )


@check_is_blocked_by_user
def forward_to_user(update: Update, context: CallbackContext):
    """Send the message from admins to the user."""
    user_id, reply_to = get_user_src_message(update, context)

    if not user_id:
        return

    context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    context.job_queue.run_once(
        callback=_send_users,
        when=Literal.DELAY_SECONDS,
        context=(update, user_id, reply_to),
    )
