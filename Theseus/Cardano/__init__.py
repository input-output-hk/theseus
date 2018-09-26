import json
from typing import Dict, List, Iterable

# hack to stop urlib3 complaining when we turn off SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests

import logging
from .Faucet import Faucet
from Theseus.Common.WalletAPI import WalletAPI
from Theseus.Common.Wallet import Wallet
from Theseus.Common.Transaction import TransactionRequest, TransactionResponse, TransactionDestination, TransactionSource
from Theseus.Common.Address import AddressResponse, AddressRequest

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Cardano Testing functions'
__all__ = ['Cardano', 'Wallet', 'WalletAPI', 'TransactionRequest', 'TransactionResponse', 'TransactionDestination',
           'TransactionSource', 'AddressRequest', 'AddressResponse']


class Cardano(WalletAPI):
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
            if stub != 'theseus.cardano':
                key = 'theseus.cardano.' + key
            return logging.getLogger(str(key))
        else:
            return logging.getLogger('theseus.cardano.unknown')

    def import_poor_wallet(self, wallet_number: int=0)-> bool:
        """ Import Wallet: Import a poor wallet

        This is only available on state-demo cardano nodes

        Args:
            wallet_number (int) : Poor Key number (0-11)

        Returns:
            boolean: True if wallet is was imported
        """
        url = " https://{0}:{1}/api/internal/import-wallet".format(self._host, self._port)
        payload = dict(
            filePath="state-demo/genesis-keys/generated-keys/poor/key{0}.sk".format(wallet_number)
        )
        self.logger.info("Importing Poor Wallet: {0}".format(wallet_number))
        response = requests.post(url, verify=self._ssl_verify, headers=self.json_headers, data=json.dumps(payload))

        if response.status_code == 200:
            self.logger.info("Poor wallet was imported")
            return True
        else:
            self.logger.error("Error importing poor wallet: {0}".format(response.text))
            return False
