
class Account:
    """ An object representing an Account

    An account is a child of a wallet may have multiple wallets and instance of wallet backend can have multiple accounts

    Args:
        walletId (int): A wallet ID
        accountId (int) : The account id for this account.
    """
    def __init__(self, walletId, index, amount, name, addresses=[]):
        self.walletId = walletId
        self.index = index
        self.addresses = addresses
        self.amount = amount
        self.name = name

    def dump(self):
        template = "Account\n\tWallet_ID:{0}\n\tAccount_ID:{1}\n\tName:{2}"
        return template.format(self.index, self.walletId, self.name)
