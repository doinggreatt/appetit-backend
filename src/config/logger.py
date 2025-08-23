import logging
import sys
import os

LOG_DIR = 'src/logs'
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if not root_logger.hasHandlers():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)

def get_module_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)


    module_logdir = os.path.join(LOG_DIR, module_name)
    os.makedirs(module_logdir, exist_ok=True)

    if not logger.handlers:
        debug_handler = logging.FileHandler(os.path.join(module_logdir, "debug.log"), encoding="utf-8")
        debug_handler.setLevel(logging.DEBUG)

        info_handler = logging.FileHandler(os.path.join(module_logdir, "info.log"), encoding="utf-8")
        info_handler.setLevel(logging.INFO)

        error_handler = logging.FileHandler(os.path.join(module_logdir, "error.log"), encoding="utf-8")
        error_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        for handler in (debug_handler, info_handler, error_handler):
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    return logger