import logging

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Theseus - Logging Functions'
__all__ = ['log_to_console', 'log_to_file', 'get_logger', 'timestamp']

logger = logging.getLogger('theseus')


def get_logger(key=None):
    """ Get a logging handle

    Supplies a logging handle , this is mostly so that you don't have to import logging directly

    Args:
        key (str) : A unique identifier for the logging handle

    Returns:
        (logger) : A logging handle
    """
    if key:
        # enforce our logging prefix
        stub = key[0:7]
        if stub != 'theseus.':
            key = 'theseus.' + key
        return logging.getLogger(str(key))
    else:
        return logger.getLogger('theseus.unknown')


def log_to_console(level=None, formatter=None):
    """ Output logs to the console

    Causes logs to be additionally directed to the console, if you call this twice you will
    get duplicated logging. This does not disable or invalidate other logging options , it
    adds to them.

    Supported Logging levels are CRITICAL, ERROR, WARNING, INFO and DEBUG

    Logging formatters are documented here , they control the format of the logs.
    https://docs.python.org/3/library/logging.html#formatter-objects

    Example:
        Selecting DEBUG will show all other levels
        Selecting ERROR will show CRITICAL and ERROR only

    Args:
        level (str) : Display logs tagged below this level.
        formatter (Formatter) : The python logging formatter you want to use

    Returns:
        (logger) : A logging handle that you don't have to use

    """
    console = logging.StreamHandler()

    if level:
        console.setLevel(level)
    else:
        console.setLevel(logging.DEBUG)

    if formatter:
        formatter = logging.Formatter(format)
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


def log_to_file(filename, level=None, formatter=None):
    """ Output logs to a file

    Causes logs to be additionally directed to a file, if you call this twice you will
    get duplicated logging. This does not disable or invalidate other logging options , it
    adds to them.

    Supported Logging levels are CRITICAL, ERROR, WARNING, INFO and DEBUG

    Logging formatters are documented here , they control the format of the logs.
    https://docs.python.org/3/library/logging.html#formatter-objects

    Example:
        Selecting DEBUG will show all other levels
        Selecting ERROR will show CRITICAL and ERROR only

    Args:
        filename (str) : Filename to log to.
        level (str) : Display logs tagged below this level.
        formatter (Formatter) : The python logging formatter you want to use.

    Returns:
        (logger) : A logging handle that you don't have to use.

    """

    filehandler = logging.FileHandler(filename)

    if level:
        filehandler.setLevel(level)
    else:
        filehandler.setLevel(logging.DEBUG)

    if formatter:
        formatter = logging.Formatter(format)
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    filehandler.setFormatter(formatter)
    if len(logger.handlers) < 2:
        logger.addHandler(filehandler)

    return logger


def timestamp():
    """ Return human readable timestamp

    Returns:
        str: a time stamp representing the current date and time with microseconds

    """
    # import datetime
    # return datetime.datetime.utcnow()
    import time
    return time.time()
