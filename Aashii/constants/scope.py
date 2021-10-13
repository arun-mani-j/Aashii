"""Containts Scope object."""

from telegram import (
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
    BotCommandScopeDefault,
)
from .literal import Literal


class Scope:
    """Represents the various supported command scopes."""

    ADMINS = BotCommandScopeChat(Literal.ADMINS_GROUP_ID)
    ALL = BotCommandScopeDefault()
    PRIVATE = BotCommandScopeAllPrivateChats()
