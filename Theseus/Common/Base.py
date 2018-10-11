import json

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Common - Base classes'
__any__ = ['Request', 'Response', 'Source', 'Destination', 'Data']


class Data(object):
    """ A base class for any classes handling data from or for the API

    This class is subclassed by Request , Response , Source and Destination

    """
    def to_json(self) -> str:
        """ Dump object to a JSON formatted string

        This method will iterate over this classed members and dump them to json

        Returns:
            str : a string containing a json representation of your object

        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        """ Dump to string

        Subclasses of this class are expected to provide a dump method

        """
        return self.dump()


class Request(Data):
    """" A base class for classed handling data requests to the API

    This class is subclassed by TransactionRequest

    """
    pass


class Response(Data):
    """" A base class for classed handling data responses from the API

    This class is subclassed by TransactionResponse

    """
    def __bool__(self):
        """ Allow this object to return true of false based on the status field

         Returns:
             bool: a boolean representing the status of the request

         """
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
