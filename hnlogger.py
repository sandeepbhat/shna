"""shna logger."""
import logging

LOGGER_NAME = "shna"


def setup_logger():
    """Set up logger.

    Returns:
        logger: Logger object
    """
    # Create logger
    _logger = logging.getLogger(LOGGER_NAME)
    # Set log level
    _logger.setLevel(logging.DEBUG)
    # Console stream handler
    stream_handler = logging.StreamHandler()
    # Log message format.
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    # Log level
    stream_handler.setLevel(logging.DEBUG)
    _logger.addHandler(stream_handler)

    return _logger


def get_logger(module_name: str):
    """Get an instance of the logger.

    Args:
        module_name: Name of the python module in which the logger is being used.
    Returns:
        logger: Logger object.
    """
    return logging.getLogger("{}.{}".format(LOGGER_NAME, module_name))
