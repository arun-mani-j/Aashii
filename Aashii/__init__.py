from os import getenv
import logging
from .server import Server

log_file = getenv("LOG_FILE")

logging.basicConfig(
    filename=log_file,
    format="%(asctime)s -%(levelname)s - %(message)s",
    level=logging.INFO,
)
