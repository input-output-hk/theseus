from Theseus.Common import Wallet
import json

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Common - Address objects'
__any__ = ['AddressRequest', 'AddressResponse']


class AddressRequest(object):
    """ Address Request - a request to create a new address for a wallet  """
    def __init__(self, wallet: Wallet, accountIndex):
        self.accountIndex = accountIndex # 2147483648  # wallet.account   TODO: this should not be hardcoded !
        self.walletId = wallet.id
        if wallet.spendingPassword:
            self.spendingPassword = wallet.spendingPassword
        else:
            self.spendingPassword = ''

    def to_json(self) -> str:
        """ Dump object to a JSON formatted string """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class AddressResponse(object):
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
