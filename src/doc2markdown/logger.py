import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from src.doc2markdown.config import LOG_DIR


def setup_logger() -> logging.Logger:

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("Doc2Markdown")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    logfile = LOG_DIR / f"{timestamp}.log"

    file_handler = RotatingFileHandler(
        logfile,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger