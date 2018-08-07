import json
import typing
import Theseus


class Destination:
    """ An object representing a transaction destination

    A Transaction can have multiple destinations , this reflects one of them.

    Args:
        amount (int): the amount of lovelaces to send
        address (str): the wallet address to send the ada to
    """
    def __init__(self, amount, address):
        self.amount = amount
        self.address = address

    def dump(self) -> str:
        """ Dump object to a string """
        template = "Cardano Transaction Destination\n\tAmount:(0)\n\tAddress:{1}\n"
        return template.format(self.amount, self.address)

    def to_json(self) -> str:
        """ Dump object to a json formatted string """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Source:
    """" An object representing a transaction source

    A transaction can have multiple inputs , this reflects one of them

    Args:
        self.account_id (int): account_id
        self.wallet_addresss (str): wallet_adddress

    Returns:
        Source

    """
    def __init__(self, account_id, wallet_id):
        self.accountIndex = account_id
        self.walletId = wallet_id

    def dump(self) -> str:
        """ Dump object to a string """
        template = "Cardano Transaction Source\n\tAccount ID:(0)\n\tWallet ID:{1}\n"
        return template.format(self.account_id, self.wallet_id)

    def to_json(self) -> str:
        """ Dump object to a json formatted string """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class TransactionRequest:
    """ An object representing a Cardano transaction request

    Args:
        source (Source): the id of the wallet from whence to source the payment
        destinations (list): a list of destinations for the payment
        grouping_policy (str):

    Returns:
        TransactionRequest
    """
    def __init__(self, source=Source, destinations=[], grouping_policy="OptimizeForHighThroughput", spending_password=False):
        self.source = source
        self.destinations = destinations
        self.grouping_policy = grouping_policy
        self.spending_password = spending_password

    def dump(self) -> str:
        """ Dump object to a string """
        template = "Cardano Transaction Request\n\tSource:(0)\n\tDestinations:{1}\n\tGrouping Policy:{2}\n\tSpending Password:{3}"
        destinations_dumped =''
        for dest in self.destinations:
            destinations_dumped += dest.to_json()

        return template.format(self.source, destinations_dumped, self.grouping_policy, self.spending_password)

    def to_json(self) -> str:
        """ Dump object to a json formatted string """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class TransactionResponse:
    """ An object representing a Cardano transaction response

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

    Returns:
        TransactionResponse
    """
    def __init__(self, json):
        #transaction_id, creation_time, amount, status=[], inputs=[], outputs=[], direction="outgoing", confirmations=0, type="foreign"):

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

    def to_json(self) -> str:
        """ Dump object to a JSON formatted string """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
