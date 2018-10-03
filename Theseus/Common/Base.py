import json

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Common - Base classes'
__any__ = ['Request', 'Response', 'Source', 'Destination', 'Data']


class Data(object):

    def to_json(self) -> str:
        """ Dump object to a JSON formatted string """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        """ Dump to string """
        return self.dump()


class Request(Data):
    pass


class Response(Data):
    def __bool__(self):
        """ Allow this object to return true of false based on the status field """
        if self.status in ['error', 'failure']:
            return False
        else:
            return True


class Source(Data):
    """ Base class for Sources

    Args:
        accountIndex(int): the index number of the account to pay from
        walletId(str): the wallet ID of the wallet to pay from

    """
    def __init__(self, accountIndex, walletId):
        self.accountIndex = accountIndex
        self.walletId = walletId


class Destination(Data):
    """ Base class for Destinations

    Args:
        amount(int): amount to pay
        address(str): receive address to pay to

    """
    def __init__(self, amount, address):
        self.amount = amount
        self.address = address
