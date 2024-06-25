import logging
import os
import traceback
from datetime import datetime
from functools import wraps


# ANSI escape codes for coloring log levels
class LogColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


LOG_COLORS = {
    "DEBUG": LogColors.OKCYAN,
    "INFO": LogColors.OKGREEN,
    "WARNING": LogColors.WARNING,
    "ERROR": LogColors.FAIL,
    "CRITICAL": LogColors.BOLD + LogColors.FAIL,
}


# Custom formatter to include colors
class CustomFormatter(logging.Formatter):
    def format(self, record):
        """
        Format the log record with ANSI colored log levels.

        :param record: LogRecord object to format.
        :return: Formatted log message.
        """
        record.asctime = datetime.fromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        record.msg = f"{record.asctime} {record.msg}"

        log_color = LOG_COLORS.get(record.levelname, LogColors.ENDC)
        record.levelname = f"{log_color}{record.levelname}{LogColors.ENDC}"
        record.msg = f"{log_color}{record.msg}{LogColors.ENDC}"
        return super().format(record)


# Get Robocorp working directory
robocorp_root_x = os.getenv("ROBOT_ROOT")
robocorp_root = os.getenv("ROBOT_ROOT", "output")
log_directory = os.path.join(robocorp_root, "output")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logs
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = os.path.join(log_directory, f"log_{current_time}.log")
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s [%(filename)s:%(lineno)d]"
)
file_handler.setFormatter(file_formatter)

# Configure logger with colored output for console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = CustomFormatter(
    "%(asctime)s %(levelname)s %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(console_formatter)

# Set up the main logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_decorator(func):
    """
    Decorator function to log function calls and exceptions.

    :param func: Function to decorate.
    :return: Decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function to log function calls and exceptions.

        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        :return: Result of the decorated function.
        """
        logger.info(
            f"Started function '{func.__name__}' with args {args} and kwargs {kwargs}"
        )
        try:
            result = func(*args, **kwargs)
            logger.info(f"Function '{func.__name__}' returns {result}")
            return result
        except Exception as e:
            logger.exception(
                f"Exception in function '{func.__name__}': {traceback.format_exc()}"
            )
            raise e

    return wrapper
