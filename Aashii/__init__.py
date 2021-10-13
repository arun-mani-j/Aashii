"""Aashii is a bot to maintain communication between users and admins."""

from os import getenv
import logging
from .server import Server

log_file = getenv("LOG_FILE")

logging.basicConfig(
    filename=log_file,
    format="%(asctime)s -%(levelname)s - %(message)s",
    level=logging.INFO,
)
