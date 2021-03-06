import logging
from Theseus.Common.WalletAPI import WalletAPI
from Theseus.Common.Wallet import Wallet
from Theseus.Common.Transaction import TransactionRequest, TransactionResponse, TransactionDestination, TransactionSource
from Theseus.Common.Address import AddressResponse, AddressRequest


__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Daedalus Testing functions'
__all__ = ['Daedalus', 'Wallet', 'WalletAPI', 'TransactionRequest', 'TransactionResponse', 'TransactionDestination',
           'TransactionSource', 'AddressRequest', 'AddressResponse']


class Daedalus(WalletAPI):
    def get_logger(self, key=None):
        """ Get a logging handle

        Supplies a logging handle , this is mostly so that you don't have to import logging directly

        Args:
            key (str) : A unique identifier for the logging handle

        Returns:
            (logging) : A logging handle
        """
        if key:
            # enforce our logging prefix
            stub = key[0:7]
            if stub != 'theseus.daedalus':
                key = 'theseus.daedalus.' + key
            return logging.getLogger(str(key))
        else:
            return logging.getLogger('theseus.daedalus.unknown')
