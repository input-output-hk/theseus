from Theseus.Logging import log_to_console, log_to_file, get_logger, timestamp
from Theseus.Daedalus import Wallet
from Theseus.Daedalus.Transaction import TransactionRequest, TransactionResponse, TransactionDestination, TransactionSource
from Theseus.Daedalus.Address import AddressRequest, AddressResponse
from Theseus.Protocols.SSHTunnel import SSHTunnel
from Theseus.Faucet import Faucet
from Theseus.Secrets import Secrets

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Theseus Automated Test Framework'
__all__ = ['Daedalus', 'Wallet',
           'TransactionRequest', 'TransactionRequest', 'TransactionResponse','TransactionDestination', 'TransactionSource',
           'AddressResponse', 'AddressRequest',
           'Faucet', 'Secrets', 'SSHTunnel',
           'get_logger', 'timestamp']

import atexit
import logging
import os
import signal
import sys
import time
from .version import __version__, __build__


def finish(reason=None):
    """ An Exit handler: Provides a way to finish and log a reason why you finished.

    If a reason is supplied then the finish will be deemed to be unexpected and a harsh
    kill will be applied to everything potentially causing destructors not to be run.
    In the absence of a reason a normal exit occurs in which
    everything terminates by going out of scope which means destructors will be run.
    finish is run by atexit at the end of a normal session.

    Args:
        reason (str) : Description of why you want to finish early

    Returns:
        None

    Notes:
        Use this when:
            making an error you have caught be fatal

            when debugging a test and you want it to finish early

        Don't use this:
            at the end of every script

            in libraries unless you are very sure its not possible to continue safely
    """
    if reason:
        logger = logging.getLogger('theseus.finish')
        message = 'Exiting unexpectedly because ' + str(reason)
        logger.info(message)
        print("\n" + message)
        time.sleep(1)  # pause to let the message get to disk
        os._exit(1)  # this is harsh kill to stop anything else happening
    else:
        logger = logging.getLogger('theseus')
        logger.info('Exiting')


def _signal_handler(signal: int, frame: any):
    """ signal_handler - catches exit signals and attempts to work out why and shutdown gracefully

    This should not be called directly , it will be called by the signal handler.
    We have to be careful about looking for things that might not exist so this is run in a try


    Args:
        signal(int): signal number
        frame(Frame): the frame that was running when we where called

    """
    try:
        class_name = frame.f_locals['self'].__class__.__name__
    except KeyError:
        class_name = frame

    if signal == 2:
        signal = 'Ctrl + C'
    else:
        signal = 'Signal: {0}'.format(signal)

    finish('Caught {0} while running in {1}'.format(signal, class_name))


signal.signal(signal.SIGINT, _signal_handler)
atexit.register(finish)


def version():
    """ Returns the Theseus version """
    return __version__


def build():
    """ Returns the Theseus build number """
    return __build__


# start the logging
logger = logging.getLogger('theseus')
logger.setLevel('DEBUG')

# configure the general log , if we are called by a script then make script.daedalus.log
log_file = 'theseus.log'
special_cases = ['noserunner.py', 'utrunner.py', 'jb-unittest_runner.py']
launching_filename = os.sep.join(sys.argv[0].split(os.sep)[-1:])

if '.py' in launching_filename:
    if launching_filename not in special_cases:
        log_file = sys.argv[0] + '.' + log_file

log_to_file(log_file, 'DEBUG')
log_to_console('INFO')

logger.info("Logging to: {0}".format(log_file))
logger.info('Starting up Theseus V{0}({1})'.format(version(), build()))
