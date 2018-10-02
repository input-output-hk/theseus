from Theseus.Common.Wallet import Wallet
from Theseus.Common.Base import Request, Response

import json

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Common - Address objects'
__any__ = ['AddressRequest', 'AddressResponse']


class AddressRequest(Request):
    """ Address Request - a request to create a new address for a wallet  """
    def __init__(self, wallet: Wallet, accountIndex=int):
        if wallet.account.__sizeof__() > 0:
            accountIndex = wallet.account[0].index
        self.accountIndex = accountIndex
        self.walletId = wallet.id
        if wallet.spendingPassword:
            self.spendingPassword = wallet.spendingPassword
        else:
            self.spendingPassword = ''


class AddressResponse(Response):
    """ Address Response - a response from a request to create addresses """
    def __init__(self, json_data: str):
        self.data = {}
        self.status = str
        self.meta = {}

        self.from_json(json_data)

    def from_json(self, json_data):
        """ Populate this object with data from the a json string"""
        parsed_json = json.loads(json_data)
        self.status = parsed_json['status']
        if parsed_json['status'] != 'error':
            self.data.update(parsed_json['data'])
            self.meta.update(parsed_json['meta'])
