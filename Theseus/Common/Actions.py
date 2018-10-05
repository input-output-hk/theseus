from Theseus.Common import Wallet, WalletAPI, AddressRequest, AddressResponse, Address, Account, TransactionRequest, \
    TransactionResponse, TransactionSource, TransactionDestination

__author__ = 'Amias Channer <amias.channer@iohk.io> for IOHK'
__doc__ = 'Common - Actions'
__any__ = ['Actions']


def quickpay(api: WalletAPI, source, destination, amount):
    """ Quickpay - pay a specific amount from one wallet to another

    The first available account and address will be used.

    Args:
        api(Theseus.Common.WalletAPI): a wallet api to use
        source: a wallet or account to pay from
        destination: a wallet or account or addresss to pay to
        amount: an amount of lovelace to pay

    Returns:
        bool: true if the payment succeeded

    Notes:
        This cannot work with an address as a source because we need

    """
    logger = api.get_logger('quickpay')
    transaction_source = ''
    transaction_destination = ''

    if isinstance(source, Wallet):
        # this doesn't consider fees
        if source.balance > amount:
            transaction_source = TransactionSource(source.account[0].index, source.id)
        else:
            logger.error(
                'Error: transaction source could not pay {0} from its balance of {1}'.format(amount, source.balance))
            return False

    if isinstance(source, Account):
        if source.amount > amount:
            transaction_source = TransactionSource(source.index, source.walletId)
        else:
            logger.error(
                'Error: transaction source could not pay {0} from its balance of {1}'.format(amount, source.amount))

    if isinstance(destination, Wallet):
        # use the first addresss on the first wallet
        transaction_destination = TransactionDestination(amount, destination.account[0].addresses[0]['id'])

    if isinstance(destination, Account):
        transaction_destination = TransactionDestination(amount, destination[0]['id'])

    if isinstance(destination, Address):
        transaction_destination = TransactionDestination(amount, destination['id'])

    # if we have all the parts then do the transaction
    if isinstance(transaction_source, TransactionSource) and isinstance(transaction_destination,
                                                                        TransactionDestination):
        transaction_request = TransactionRequest(source=transaction_source, destinations=[transaction_destination])
        logger.info("Transaction: {0}".format(transaction_request.to_json()))
        response = api.transact(transaction_request)
        if response.status == 'success':
            return True
        else:
            return False
    else:
        logger.error("Sorry, could not make sense of inputs ")
        return False


def find_genesis_wallet(api) -> Wallet:
    """ Find a wallet with funds

    Args:
        api(Theseus.WalletAPI): a wallet api object to use

    Returns:
          Wallet: a wallet with funds

    """
    wallets = api.fetch_wallet_list(balance_filter='GT[30000000]')

    # return the first wallet from a dict keyed by id
    return wallets.popitem()[1]
