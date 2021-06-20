import logging
from telegram.ext import Updater
from Aashii.utils.database import Database
from Aashii.utils.misc import error_handler


class Server:
    def __init__(self, token: str, database_url: str, handlers: dict):
        self.updater = Updater(token=token, user_sig_handler=self.signal_handler)
        self.database = Database(database_url)
        self.updater.dispatcher.bot_data["database"] = self.database
        self._setup_handlers(handlers)

    def _setup_handlers(self, handlers: dict):

        dispatcher = self.updater.dispatcher
        for handler_type, handles in handlers.items():
            for handle in handles:
                h_kwargs, d_args = handle[0], handle[1:]
                handler = handler_type(**h_kwargs)
                dispatcher.add_handler(handler, *d_args)

        dispatcher.add_error_handler(error_handler)

    def listen(self, listen: str, port: int, url: str, url_path: str):

        self.updater.start_webhook(
            listen=listen,
            port=port,
            url_path=url_path,
            webhook_url=f"{url}/{url_path}",
            allowed_updates=["callback_query", "message"],
        )
        logging.info("Started listening ...")
        self.updater.idle()

    def poll(self, poll_interval: int = 0):

        self.updater.start_polling(
            poll_interval=poll_interval,
            allowed_updates=["callback_query", "message"],
        )
        logging.info("Started polling ...")
        self.updater.idle()

    def signal_handler(self, *_):

        del self.database
        logging.info("Got an interruption, bye.")
