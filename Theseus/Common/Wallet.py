

class Wallet(object):
    """ An object representing a Wallet

    Args:
        id (str): a ID for the wallet
        name (str): the display name of the wallet
        passphrase(str): the recovery passphrase for the wallet
        balance(int): the current balance of the wallet
        assuranceLevel(str): the assurance level for security either strict or normal , defaults to normal
        spendingPassword (str): optional spending password
        account (str): the account this wallet is connected to , zero is unconnected.
        hasSpendingPassword (bool): if a spending password is set
        spendingPasswordLastUpdate(str): when password was last updated
    Returns:
        a wallet object

    Notes:
        if you need to change values here use the api to change them in the backend and create a new object,
        updating them if possible but changes will not be sent to the back end so its not worth it.
        A wallet is a child of the wallet backend which is part of either Daedalus or Cardano.
        A wallet can have multiple child accounts

    """
    def __init__(self, id, name, passphrase=False, balance=0, assuranceLevel="normal", spendingPassword=False,
                 spendingPasswordLastUpdate=str, account=0, hasSpendingPassword=False, syncState={}, createdAt=str, type=str ):
        self.id = id
        self.name = name
        self.passphrase = passphrase
        self.balance = balance
        self.assuranceLevel = assuranceLevel
        self.spendingPassword = spendingPassword
        self.account = account
        self.spendingPasswordLastUpdate = spendingPasswordLastUpdate
        self.hasSpendingPassword = hasSpendingPassword
        self.syncState = syncState
        self.createdAt = createdAt
        self.type = type
        self.account = 0  # this will be overwritten

    #def add_account(self, account: Account):
    #    self.accounts.append(account)

    #def del_account(self, account: Account):
    #    for check in self.accounts:
    #        if check == account:
    #            del check

    def __str__(self):
        return "{0} - {1}".format(self.name, self.balance)

    def dump(self):
        template = "Wallet\n\tName:{0}\n\tID:{1}\n\tPassphrase:{2}\n\tBalance:{3}\n\tSpendingPassword:{4}\n\tAssurance:{5}\n\tAccounts:{6}"
        return template.format(self.name, self.id, self.passphrase, self.balance, self.spendingPassword, self.assuranceLevel, self.account)
