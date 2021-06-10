from telegram import InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from Aashii.constants import Button, Literal, Message
from Aashii.utils.misc import announce, block_user, unblock_user
from Aashii.utils.wrappers import (
    check_is_blocked_by_user,
    check_is_group_command,
    check_is_reply_verbose,
    check_user_status,
)


@check_is_group_command
@check_is_reply_verbose
def announce_users(update: Update, context: CallbackContext):

    """
    Announces the replies message to every user in database.
    """

    if context.bot_data.get("announcement"):
        update.message.reply_html(Message.ANNOUNCEMENT_IN_DUE)
        return

    database = context.bot_data["database"]
    context.bot_data["announcement"] = update.message.reply_to_message
    context.bot_data["sent"] = context.bot_data["failed"] = 0
    context.bot_data["users"], context.bot_data["total"] = database.get_users()
    text = Message.ANNOUNCEMENT_INIT.format(TOTAL=context.bot_data["total"])
    context.bot_data["log_message"] = update.message.reply_html(text)
    context.job_queue.run_repeating(
        announce, interval=Literal.ANNOUNCEMENT_INTERVAL, name="announcement"
    )


@check_is_group_command
def block_user_cl(update: Update, context: CallbackContext):

    """
    Blocks the user from contacting the admins based on command.
    """

    database = context.bot_data["database"]

    if update.message.reply_to_message:
        message_id = update.message.reply_to_message.message_id
        user_id = database.get_user_id(message_id)

        if not user_id:
            update.message.reply_html(Message.INVALID_REPLY)
            return

    elif context.args and context.args[0].isdigit():
        user_id = int(context.args[0])
    else:
        update.message.reply_html(Message.INVALID_REPLY)
        return

    block_user(user_id, context)

    full_name = database.get_user_full_name(user_id)
    text = Message.BLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    message = update.message.reply_html(text)
    database.add_message(message.message_id, user_id)


@check_is_group_command
def cancel_announcement(update: Update, context: CallbackContext):

    """
    Cancels an announcement if scheduled.
    """

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
        log_message.edit_text(edit_text, parse_mode=ParseMode.HTML)
        del context.bot_data["users"]
    else:
        text = Message.NO_ANNOUNCEMENT

    update.message.reply_html(text)


def send_help(update: Update, _):

    """
    Sends the bot's usage guide intended for private or
    group depending upon the place of invocation.
    """

    if update.message.chat.type == update.message.chat.PRIVATE:
        update.message.reply_html(text=Message.HELP_PRIVATE)
    else:
        update.message.reply_html(text=Message.HELP_GROUP)


@check_user_status
def send_start(update: Update, context: CallbackContext):

    """
    Connects the user with admins group in case of private chat,
    else shows the bot's description.
    """

    if update.message.chat.type != update.message.chat.PRIVATE:
        update.message.reply_html(Message.START_GROUP)
        return

    buttons = [Button.BLOCK, Button.CONNECT]
    database = context.bot_data["database"]
    keyboard = InlineKeyboardMarkup.from_row(buttons)
    user = update.message.from_user
    full_name = user.full_name

    try:
        mem = context.bot.get_chat_member(Literal.CHAT_GROUP_ID, user.id)
    except Exception:
        status = Message.FALLBACK_STATUS
    else:
        status = mem.status.title()

    user_id = user.id
    username = f"@{user.username}" if user.username else Message.NO_USERNAME
    text = Message.USER_CONNECTED.format(
        FULL_NAME=full_name, USER_ID=user_id, USERNAME=username, STATUS=status
    )

    update.message.reply_html(
        Message.START_PRIVATE.format(GROUP_NAME=Literal.GROUP_NAME)
    )
    message = context.bot.send_message(
        chat_id=Literal.ADMINS_GROUP_ID,
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )
    database.add_user(user_id, username, full_name)
    database.add_message(message.message_id, user_id)


def static_command(update: Update, _: CallbackContext):

    command = update.message.text[1:].split("@")[0]

    try:
        text = open(f"data/static/{command}").read()
    except FileNotFoundError:
        update.message.reply_html(Message.INVALID_COMMAND)
    else:
        update.message.reply_html(text)


@check_is_group_command
def unblock_user_cl(update: Update, context: CallbackContext):

    """
    Unblocks the user from contacting the admins based on command.
    """

    database = context.bot_data["database"]

    if update.message.reply_to_message:
        message_id = update.message.reply_to_message.message_id
        user_id = database.get_user_id(message_id)

        if not user_id:
            update.message.reply_html(Message.INVALID_REPLY)
            return

    elif context.args and context.args[0].isdigit():
        user_id = int(context.args[0])
    else:
        update.message.reply_html(Message.INVALID_REPLY)
        return

    unblock_user(user_id, context)

    full_name = database.get_user_full_name(user_id)
    text = Message.UNBLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    message = update.message.reply_html(text)
    database.add_message(message.message_id, user_id)
