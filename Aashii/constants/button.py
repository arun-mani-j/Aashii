"""Contains Button object."""

from telegram import InlineKeyboardButton
from .label import Label


class Button:
    """Button contains inline keyboard buttons used in reply markup."""

    BLOCK = InlineKeyboardButton(text=Label.BLOCK, callback_data="block")

    CONNECT = InlineKeyboardButton(text=Label.CONNECT, callback_data="connect")

    UNBLOCK = InlineKeyboardButton(text=Label.UNBLOCK, callback_data="unblock")
