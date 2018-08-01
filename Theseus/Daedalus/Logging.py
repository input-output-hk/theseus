import logging

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Daedalus - Logging Functions'
__all__ = ['get_logger']

logger = logging.getLogger('daedalus')


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
        if stub != 'theseus.daedalus':
            key = 'theseus.daedalus.' + key
        return logging.getLogger(str(key))
    else:
        return logger.getLogger('theseus.daedalus.unknown')
