"""
Miscellaneous functions.
"""

import logging
from telegram import ParseMode
from telegram.ext import CallbackContext
from Aashii.constants import Message


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
