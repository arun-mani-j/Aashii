"""Contains handlers related to commands."""

from telegram import Bot, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from Aashii.constants import Button, Literal, Message
from Aashii.utils.broadcast import announce
from Aashii.utils.misc import (
    block_user,
    get_membership,
    get_user_src_message,
    unblock_user,
)
from Aashii.utils.wrappers import (
    check_is_group_command,
    check_is_reply_verbose,
    check_user_status,
)


@check_is_group_command
@check_is_reply_verbose
def announce_users(update: Update, context: CallbackContext):
    """Announce the replied message to every user in database."""
    if context.bot_data.get("announcement"):
        update.message.reply_html(Message.ANNOUNCEMENT_IN_DUE)
        return

    database = context.bot_data["database"]
    context.bot_data["announcement"] = update.message.reply_to_message
    context.bot_data["sent"] = context.bot_data["failed"] = 0
    context.bot_data["users"], context.bot_data["total"] = database.get_users()
    step = len(context.bot_data) // Literal.STEP
    context.bot_data["steps"] = [(step * i) for i in range(1, Literal.STEP + 1)]
    text = Message.ANNOUNCEMENT_INIT.format(TOTAL=context.bot_data["total"])
    context.bot_data["log_message"] = update.message.reply_html(text)
    context.job_queue.run_repeating(
        announce, interval=Literal.ANNOUNCEMENT_INTERVAL, name="announcement"
    )


@check_is_group_command
def block_user_cl(update: Update, context: CallbackContext):
    """Block the user from contacting the admins based on command."""
    database = context.bot_data["database"]

    if context.args and context.args[0].isdigit():
        user_id = int(context.args[0])
    else:
        user_id, _ = get_user_src_message(update, context)
        if not user_id:
            update.message.reply_html(Message.INVALID_REPLY)
            return

    msg_id = block_user(user_id, context)

    full_name = database.get_user_full_name(user_id)
    text = Message.BLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    message = update.message.reply_html(text)
    database.add_admin_message(update.message.message_id, user_id, msg_id)
    database.add_user_message(1, user_id, message.message_id)


@check_is_group_command
def cancel_announcement(update: Update, context: CallbackContext):
    """Cancel an announcement if scheduled."""
    if context.bot_data.pop("announcement", None):
        job = context.job_queue.get_jobs_by_name("announcement")[0]
        job.schedule_removal()
        log_message = context.bot_data.pop("log_message")
        sent = context.bot_data.pop("sent")
        failed = context.bot_data.pop("failed")
        total = context.bot_data.pop("total")
        percent = int(((sent + failed) / total) * 100)
        edit_text = Message.ANNOUNCEMENT_CANCELLED.format(
            SENT=sent, FAILED=failed, PROGRESS=percent
        )
        text = Message.CANCELLED_ANNOUNCEMENT.format(PROGRESS=percent)
        log_message.edit_text(edit_text)
        del context.bot_data["users"]
    else:
        text = Message.NO_ANNOUNCEMENT

    update.message.reply_html(text)


@check_is_group_command
@check_is_reply_verbose
def delete(update: Update, context: CallbackContext):
    """Delete the message sent by admins to users."""
    database = context.bot_data["database"]
    reply = update.message.reply_to_message

    user_id, dest_msg_id = database.get_user_dest_message_id_from_admins(
        reply.message_id
    )

    if user_id:
        try:
            context.bot.delete_message(user_id, dest_msg_id)
        except:
            update.message.reply_html(Message.DELETE_FAILED)
        else:
            update.message.reply_html(Message.DELETE_DONE)
    else:
        update.message.reply_html(Message.NOT_LINKED)


def send_help(update: Update, context: CallbackContext):
    """Send the bot's usage guide intended for private or\
    group depending upon the place of invocation."""
    if update.message.chat.type == update.message.chat.PRIVATE:
        update.message.reply_html(text=Message.HELP_PRIVATE)
    else:
        update.message.reply_html(text=Message.HELP_GROUP)
        context.bot_data["lastUserId"] = Literal.ADMINS_GROUP_ID


@check_user_status
def send_start(update: Update, context: CallbackContext):
    """Connect the user with admins group in case of private chat,\
    else show the bot's description."""
    if update.message.chat.type != update.message.chat.PRIVATE:
        update.message.reply_html(Message.START_GROUP)
        context.bot_data["lastUserId"] = Literal.ADMINS_GROUP_ID
        return

    buttons = [Button.BLOCK, Button.CONNECT]
    database = context.bot_data["database"]
    keyboard = InlineKeyboardMarkup.from_row(buttons)
    user = update.message.from_user
    user_id = user.id
    full_name = user.full_name
    membership = get_membership(user_id, context.bot)
    username = f"@{user.username}" if user.username else None
    text = Message.USER_CONNECTED.format(
        FULL_NAME=full_name,
        USER_ID=user_id,
        USERNAME=username,
        MEMBERSHIP=membership,
        BLOCKED=False,
    )

    update.message.reply_html(
        Message.START_PRIVATE.format(GROUP_NAME=Literal.GROUP_NAME)
    )
    message = context.bot.send_message(
        chat_id=Literal.ADMINS_GROUP_ID,
        text=text,
        reply_markup=keyboard,
    )
    database.add_user_message(update.message.message_id, user_id, message.message_id)


def static_command(update: Update, context: CallbackContext):
    """Send static command mentioned in static folder."""
    command = update.message.text[1:].split("@")[0]

    try:
        text = open(f"data/static/{command}").read()
    except FileNotFoundError:
        update.message.reply_html(Message.INVALID_COMMAND)
    else:
        update.message.reply_html(text)

    if update.message.chat.type != update.message.chat.PRIVATE:
        context.bot_data["lastUserId"] = Literal.ADMINS_GROUP_ID


@check_is_group_command
def unblock_user_cl(update: Update, context: CallbackContext):
    """Unblock the user from contacting the admins based on command."""
    database = context.bot_data["database"]

    if context.args and context.args[0].isdigit():
        user_id = int(context.args[0])
    else:
        user_id, _ = get_user_src_message(update, context)
        if not user_id:
            update.message.reply_html(Message.INVALID_REPLY)
            return

    msg_id = unblock_user(user_id, context)

    full_name = database.get_user_full_name(user_id)
    text = Message.UNBLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    message = update.message.reply_html(text)
    database.add_admin_message(update.message.message_id, user_id, msg_id)
    database.add_user_message(1, user_id, message.message_id)


@check_is_group_command
def whois(update: Update, context: CallbackContext):
    """Get information about user replied to or given as argument."""
    database = context.bot_data["database"]

    if context.args and context.args[0].isdigit():
        user_id = int(context.args[0])
    else:
        user_id, _ = get_user_src_message(update, context)
        if not user_id:
            update.message.reply_html(Message.INVALID_REPLY)
            return

    username, full_name, blocked = database.get_user(user_id)
    membership = get_membership(user_id, context.bot)
    text = Message.USER.format(
        FULL_NAME=full_name,
        USER_ID=user_id,
        USERNAME=username,
        MEMBERSHIP=membership,
        BLOCKED=blocked,
    )
    update.effective_message.reply_html(text)
