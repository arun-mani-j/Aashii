"""
Miscellaneous functions.
"""

import logging
from telegram import ParseMode
from telegram.error import Unauthorized
from telegram.ext import CallbackContext
from Aashii.constants import Literal, Message


def announce(context: CallbackContext):

    """
    Announces the announcement one by one.
    """

    announcement = context.bot_data["announcement"]
    log_message = context.bot_data["log_message"]

    try:
        user_id = context.bot_data["users"].pop(0)
    except IndexError:
        sent = context.bot_data.pop("sent")
        failed = context.bot_data.pop("failed")
        total = context.bot_data.pop("total")
        text = Message.ANNOUNCEMENT_DONE.format(SENT=sent, FAILED=failed, TOTAL=total)
        del context.bot_data["announcement"]
        del context.bot_data["log_message"]
        del context.bot_data["users"]
        context.job.schedule_removal()
    else:
        try:
            announcement.copy(user_id)
        except Exception as e:
            logging.error(str(e))
            context.bot_data["failed"] = context.bot_data["failed"] + 1
        else:
            context.bot_data["sent"] = context.bot_data["sent"] + 1
        finally:
            sent = context.bot_data["sent"]
            failed = context.bot_data["failed"]
            count = sent + failed
            total = context.bot_data["total"]
            percent = int((count / total) * 100)
            text = Message.ANNOUNCEMENT_PULSE.format(
                SENT=sent, FAILED=failed, PROGRESS=percent
            )
    finally:
        log_message.edit_text(text, parse_mode=ParseMode.HTML)


def block_user(user_id: int, context: CallbackContext):

    """
    Blocks the user from contacting admins and informs the user.
    """

    database = context.bot_data["database"]
    database.set_user_status(user_id, True)
    try:
        context.bot.send_message(
            chat_id=user_id, text=Message.BLOCKED_USER_STATUS, parse_mode=ParseMode.HTML
        )
    except Unauthorized:
        pass


def error_handler(_: object, context: CallbackContext):

    """
    Handles the known errors and exceptions.
    """

    error = Message.ERROR.format(ERROR=context.error)
    try:
        context.bot.send_message(
            chat_id=Literal.ADMINS_GROUP_ID, text=error, parse_mode=ParseMode.HTML
        )
    except:
        logging.error(str(context.error))


def unblock_user(user_id: int, context: CallbackContext):

    """
    Unblocks the user from contacting admins and informs the user.
    """

    database = context.bot_data["database"]
    database.set_user_status(user_id, False)
    try:
        context.bot.send_message(
            chat_id=user_id, text=Message.UNBLOCKED_USER_STATUS, parse_mode=ParseMode.HTML
        )
    except Unauthorized:
        pass
