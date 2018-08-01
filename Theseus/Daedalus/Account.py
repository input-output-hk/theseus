class Account:
    """ An object representing a Daedalus Account

    An account may have multiple wallets and instance of daedalus can currently have one account

    Args:
        wallet_id (str): A walllet ID
        account_id (int) : The account id for this account.
    """
    def __init__(self, wallet_id , account_id=0):
        self._wallet_id = wallet_id
        self._account_id = account_id

    @property
    def wallet_id(self):
        return self._wallet_id

    @wallet_id.setter
    def wallet_id(self, value):
        self._wallet_id = value

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    def dump(self):
        template = "Daedalus Account\n\tWallet_ID:{0}\n\tAccount_ID:{1}"
        return template.format(self.account_id, self.wallet_id)