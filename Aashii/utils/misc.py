"""
Miscellaneous functions.
"""

import logging
import traceback
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
    sent = context.bot_data["sent"]
    failed = context.bot_data["failed"]
    total = context.bot_data["total"]
    steps = context.bot_data["steps"]

    try:
        user_id = context.bot_data["users"].pop(0)
    except IndexError:
        text = Message.ANNOUNCEMENT_DONE.format(SENT=sent, FAILED=failed, TOTAL=total)
        del context.bot_data["announcement"]
        del context.bot_data["log_message"]
        del context.bot_data["users"]
        del context.bot_data["sent"]
        del context.bot_data["failed"]
        del context.bot_data["total"]
        del context.bot_data["steps"]
        context.job.schedule_removal()
    else:
        try:
            announcement.copy(user_id)
        except Exception as e:
            logging.error(str(e))
            context.bot_data["failed"] = failed + 1
        else:
            context.bot_data["sent"] = sent + 1
        finally:
            count = sent + failed + 1
            total = context.bot_data["total"]
            percent = int((count / total) * 100)
            if count in steps:
                text = Message.ANNOUNCEMENT_PULSE.format(
                    SENT=sent, FAILED=failed, PROGRESS=percent
                )
            else:
                text = None
    finally:
        if text:
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

    error = str(context.error)
    tb = "".join(
        traceback.format_tb(context.error.__traceback__, Literal.TRACEBACK_VALUE)
    )
    error_text = Message.ERROR.format(ERROR=error, TRACEBACK=tb)
    if Literal.INFORM_ERROR:
        try:
            context.bot.send_message(
                chat_id=Literal.ADMINS_GROUP_ID,
                text=error_text,
                parse_mode=ParseMode.HTML,
            )
        except:
            logging.error("%s\n%s", error, tb)
    else:
        logging.error("%s\n%s", error, tb)


def unblock_user(user_id: int, context: CallbackContext):

    """
    Unblocks the user from contacting admins and informs the user.
    """

    database = context.bot_data["database"]
    database.set_user_status(user_id, False)
    try:
        context.bot.send_message(
            chat_id=user_id,
            text=Message.UNBLOCKED_USER_STATUS,
            parse_mode=ParseMode.HTML,
        )
    except Unauthorized:
        pass
