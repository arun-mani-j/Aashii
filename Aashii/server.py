"""Contains the Server object."""

import logging
from telegram.ext import Defaults, Updater
from telegram import ParseMode
from Aashii.constants import Scope
from Aashii.utils.database import Database
from Aashii.utils.misc import error_handler


class Server:
    """Server takes care of setting up the bot, handlers and getting updates."""

    def __init__(self, token: str, commands: dict, database_url: str, handlers: dict):
        """Create a new Server."""
        defaults = Defaults(parse_mode=ParseMode.HTML, allow_sending_without_reply=True)
        self.updater = Updater(
            token=token, defaults=defaults, user_sig_handler=self.signal_handler
        )
        self.database = Database(database_url)
        self.updater.dispatcher.bot_data["database"] = self.database
        self._setup_handlers(handlers)
        self._setup_commands(commands)

    def _setup_commands(self, commands: dict):

        admins = commands["admins"] + commands["all"]
        private = commands["private"] + commands["all"]
        self.updater.bot.set_my_commands(admins, scope=Scope.ADMINS)
        self.updater.bot.set_my_commands(private, scope=Scope.PRIVATE)

    def _setup_handlers(self, handlers: dict):

        dispatcher = self.updater.dispatcher
        for handler_type, handles in handlers.items():
            for handle in handles:
                h_kwargs, d_args = handle[0], handle[1:]
                handler = handler_type(**h_kwargs)
                dispatcher.add_handler(handler, *d_args)

        dispatcher.add_error_handler(error_handler)

    def listen(self, listen: str, port: int, url: str, url_path: str):
        """Listen for incoming webhook updates."""
        self.updater.start_webhook(
            listen=listen,
            port=port,
            url_path=url_path,
            webhook_url=f"{url}/{url_path}",
            allowed_updates=["callback_query", "edited_message", "message"],
        )
        logging.info("Started listening ...")
        self.updater.idle()

    def poll(self, poll_interval: int = 0):
        """Poll for new updates."""
        self.updater.start_polling(
            poll_interval=poll_interval,
            allowed_updates=["callback_query", "edited_message", "message"],
        )
        logging.info("Started polling ...")
        self.updater.idle()

    def signal_handler(self, *_):
        """Clean up resources and sign off."""
        del self.database
        logging.info("Got an interruption, bye.")
