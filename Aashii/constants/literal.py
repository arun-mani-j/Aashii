"""
Contains Literal object.
"""

import os


class Literal:

    """
    Lieral contains values that are simple and never change, like admins group ID.
    """

    ADMINS_GROUP_ID = os.getenv("ADMINS_GROUP_ID")

    ANNOUNCEMENT_INTERVAL = float(os.getenv("ANNOUNCEMENT_INTERVAL", "2"))

    CHAT_GROUP_ID = os.getenv("CHAT_GROUP_ID")

    DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", "2"))

    GROUP_NAME = os.getenv("GROUP_NAME", "Illuminati")
