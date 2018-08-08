import Theseus
import json
import typing


class AddressRequest:
    """ Address Request - a request to create a new address for a wallet  """
    def __init__(self, wallet: Theseus.Wallet, password: str):
        self.accountIndex = wallet.account
        self.walletId = wallet.id
        self.spendingPassword = password

    def to_json(self) -> str:
        """ Dump object to a JSON formatted string """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class AddressResponse:
    """ Address Response - a response from a request to create addresses """
    def __init__(self, json: str):
        self.data = typing.Dict[str, str]
        self.status = str
        self.meta = typing.Dict[typing.Dict]

        self.from_json(json)

    def from_json(self, json):
        """ Populate this object with data from the a json string"""
        parsed_json = json.loads(json)
        self.data = parsed_json['data']
        self.status = parsed_json['status']
        self.meta = parsed_json['meta']