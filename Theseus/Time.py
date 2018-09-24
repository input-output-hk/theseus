import time

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Theseus - Time Functions'
__all__ = ['timestamp', 'sleep']


def timestamp():
    """ Return human readable timestamp

    Returns:
        str: a time stamp representing the current date and time with microseconds

    """
    return time.time()


def sleep(seconds: float):
    """ Wait for an amount of seconds 
    
    Args:
        seconds(float): wait for this many seconds
    """
    time.sleep(seconds)
