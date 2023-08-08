import os
import logging


class Logger:
    """Logger class is a wrapper around the logging module.
    Useful if you need to apply dependecy injection to your code."""

    def __init__(self, logger_name: str):
        self.logger = self.__config_logger(logger_name)

    @classmethod
    def __config_logger(cls, logger_name: str):
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=os.environ.get("LOG_LEVEL", "INFO"),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        return logging.getLogger(logger_name)

    @classmethod
    def get_logger(cls, logger_name: str):
        """Return a logger object without instantiating the class.

        Args:
            logger_name (str): Name of the logger

        Returns:
            Logger: Logger object
        """
        return cls.__config_logger(logger_name)
