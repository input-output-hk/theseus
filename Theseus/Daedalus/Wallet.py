class Wallet:
    """ An object representing a Daedalus Wallet

    Args:
        id (str): a daedalus ID for the wallet
        name (str): the display name of the wallet
        passphrase(str): the recovery passphrase for the wallet
        balance(int): the current balance of the wallet
        assurance(str): the assurance level for security either strict or normal , defaults to normal
        spending_password (str): optional spending password
        account (str): the account this wallet is connected to , zero is unconnected.

    Returns:
        a wallet object

    Notes:
        There are no setters on this object because it represents the state of the backend,
        if you need to change values here use the api to change them in the backend.

    """
    def __init__(self, id, name, passphrase=False, balance=0, assurance="normal", spending_password=False, account=0):
        self._id = id
        self._name = name
        self._passphrase = passphrase
        self._balance = balance
        self._assurance = assurance
        self._spending_password = spending_password
        self._account = account

    @property
    def id(self):
        return  self._id

    @property
    def passphrase(self):
        return self._passphrase

    @property
    def name(self):
        return self._name

    @property
    def balance(self):
        return self._balance

    @property
    def account(self):
        return self._account

    def __str__(self):
        return "{0} - {1}".format(self.name, self.balance)

    def dump(self):
        template = "Daedalus Wallet\n\tName:{0}\n\tID:{1}\n\tPassphrase:{2}\n\tBalance:{3}\n\tSpendingPassword:{4}\n\tAssurance:{5}"
        return template.format(self._name, self._id, self._passphrase, self._assurance, self._spending_password, self._assurance)