"""Contains Literal object."""

import os


class Literal:
    """Lieral contains values that are simple and never change, like admins' group ID."""

    ADMINS_GROUP_ID = int(os.getenv("ADMINS_GROUP_ID"))

    ANNOUNCEMENT_INTERVAL = float(os.getenv("ANNOUNCEMENT_INTERVAL", "0.5"))

    CHAT_GROUP_ID = int(os.getenv("CHAT_GROUP_ID"))

    DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", "2"))

    GROUP_NAME = os.getenv("GROUP_NAME", "Illuminati")

    INFORM_ERROR = os.getenv("INFORM_ERROR", "TRUE") == "TRUE"

    REPLY_CHARACTER = os.getenv("REPLY_CHARACTER", "!")

    STEP = int(os.getenv("STEP", "10"))

    TRACEBACK_VALUE = int(os.getenv("TRACEBACK_VALUE", "5"))
