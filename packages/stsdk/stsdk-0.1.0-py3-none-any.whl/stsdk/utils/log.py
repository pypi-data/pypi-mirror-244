import inspect
import os
import sys

from loguru import logger

from stsdk.utils.config import config


class LogUtil:
    def __init__(self, log_directory=config.LOG_PATH):
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)

        log_file_info = os.path.join(self.log_directory, "{time:YYYY-MM-DD}_info.log")
        log_file_error = os.path.join(self.log_directory, "{time:YYYY-MM-DD}_error.log")
        log_file_warning = os.path.join(
            self.log_directory, "{time:YYYY-MM-DD}_warning.log"
        )
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</green> | <level>{level: <8}</level> | <cyan>{"
            "message}</cyan> "
        )
        logger.remove()
        logger.add(sys.stdout, format=log_format, colorize=True)
        logger.add(
            log_file_info,
            level="INFO",
            rotation="1 day",
            retention="3 days",
            format=log_format,
            colorize=False,
        )
        logger.add(
            log_file_error,
            level="ERROR",
            rotation="1 day",
            retention="3 days",
            format=log_format,
            colorize=False,
        )
        logger.add(
            log_file_warning,
            level="WARNING",
            rotation="1 day",
            retention="3 days",
            format=log_format,
            colorize=False,
        )

    def log(self, level, message):
        frame = inspect.currentframe().f_back.f_back
        filename = inspect.getframeinfo(frame).filename
        function = inspect.getframeinfo(frame).function
        lineno = inspect.getframeinfo(frame).lineno
        logger.log(level, f"{filename}:{function}:{lineno} - {message}")

    def debug(self, message):
        self.log("DEBUG", message)

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)

    def exception(self, message):
        self.log("ERROR", message)


log = LogUtil()
