import json
from Theseus import get_logger
from Theseus.Common.Base import Request, Response, Source, Destination


class TransactionDestination(Destination):
    """ An object representing a transaction destination

    A Transaction can have multiple destinations , this reflects one of them.

    """
    def dump(self) -> str:
        """ Dump object to a string """
        template = "Cardano TransactionDestination\n\tAmount:(0)\n\tAddress:{1}\n"
        return template.format(self.amount, self.address)


class TransactionSource(Source):
    """" An Location object representing a transaction source

    A transaction can have multiple inputs , this reflects one of them

    Returns:
        TransactionSource

    """
    def dump(self) -> str:
        """ Dump object to a string """
        template = "Cardano TransactionSource\n\tAccount ID:(0)\n\tWallet ID:{1}\n"
        return template.format(self.accountIndex, self.walletId)


class TransactionRequest(Request):
    """ An object representing a Cardano transaction request

    Args:
        source (TransactionSource): the id of the wallet from whence to source the payment
        destinations (list): a list of destinations for the payment
        grouping_policy (str):

    Returns:
        TransactionRequest
        
    """
    def __init__(self, source=TransactionSource, destinations=[], groupingPolicy="OptimizeForHighThroughput", spendingPassword=''):
        self.source = source
        self.destinations = destinations
        self.groupingPolicy = groupingPolicy
        self.spendingPassword = spendingPassword

    def dump(self) -> str:
        """ Dump object to a string """
        template = "Cardano Transaction Request\n\tTransactionSource:(0)\n\tDestinations:{1}\n\tGrouping Policy:{2}\n\tSpending Password:{3}"

        destinations_dumped = ''
        for dest in self.destinations:
            destinations_dumped += dest.to_json()

        return template.format(self.source, destinations_dumped, self.groupingPolicy, self.spendingPassword)


class TransactionResponse(Response):
    """ An object representing a Cardano transaction response

    This data is returned as slice of the data array which may contain multiple transaction responses.

    Args:
        json (str): the raw json response

    Members:
        transaction_id (str): the transactions unique identifier

        creation_time (str) : the creation timestamp

        status (list) : the statuses of the transaction

        amount (int): the value of the transaction

        inputs (list): a list of transaction inputs

        outputs (list): a list of transaction outputs

        direction (str): the direction of the transaction, incoming or outgoing

        confirmations (int): the amount of confirmations recieved

        type (int): the type of the transaction

    Returns:
        TransactionResponse
        
    """
    def __init__(self, json):

        self.transaction_id = str
        self.confirmations = str
        self.creation_time = str
        self.amount = int
        self.status = str
        self.inputs = []
        self.outputs = []
        self.direction = str
        self.type = str

        self.from_json(json)

    def from_json(self, raw_json):
        """ Populate this object with data from a json"""
        parsed_json = json.loads(raw_json)
        if parsed_json['status'] in ['error','failed']:
            logger = get_logger('TransactionResponse')
            logger.error("Transaction Error: {0}".format(raw_json))
        else:
            self.transaction_id = parsed_json['data']['id']
            self.confirmations = parsed_json['data']['confirmations']
            self.creation_time = parsed_json['data']['creationTime']
            self.amount = parsed_json['data']['amount']
            self.inputs = parsed_json['data']['inputs']
            self.outputs = parsed_json['data']['outputs']
            self.direction = parsed_json['data']['direction']
            self.type = parsed_json['data']['type']
            self.status = parsed_json['status']

    def dump(self) -> str:
        """ Dump object to a string """
        template = "Cardano Transaction Response\n\tID:{0}\n\tCreation Time:{1}\n\tAmount:{2}\n\tStatus:{3}\n"
        return template.format(self.transaction_id, self.creation_time, self.amount, self.status)

