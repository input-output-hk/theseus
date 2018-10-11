import json
#from typing import Dict, List, Iterable
import random
# hack to stop urlib3 complaining when we turn off SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests

#  import only the specific parts of theseus we need
from Theseus.Common.Wallet import Wallet
from Theseus.Common.Transaction import TransactionRequest, TransactionResponse
from Theseus.Protocols.SSHTunnel import SSHTunnel
from Theseus.Common.Address import AddressResponse, AddressRequest
from Theseus import get_logger
from Theseus.Common.Account import Account


class WalletAPI:
    """" WalletAPI - Provides access to the Wallet API

    This object will provide access to an instance of the Cardano Wallet API which can be provided by either a daedalus
    installation or a cardano node that is running a wallet backend.

    This interface is typically configured to be available on the loopback interface (127.0.0.1) for security purposes.

    Currently the use of SSH certificates is not enforced so ssl_verify is defaulted to False

    To access a remote instance you will need to use an SSH tunnel to forward the ports to make it accessible.

    Args:
        host(str): The Host/IP Address to connect to the API , default 127.0.0.1
        port(int): The Port number to connection the API , default 8090
        ssl_verify(bool): True to enable SSL Certificate verification , False to disable it, default False
        ssh_tunnel(bool): True to configure an SSH tunnel according to additional params
        username(str): The Username  for the SSH Connection
        ssh_port(int): THe SSH Port to connect to for the tunnel
        local_port(int): The local port to forward from, default 8090
        remote_port(int): The remote port to forward to, default 8090
        local_host(str): The local host name to forward from , default 127.0.0.1
        remote_host(str): The remote host name to forward to , default 127.0.0.1
        version(int): The API version number, default 1

    For more info on the SSHTunnel see the Theseus.Protocol.SSHTunnel documentation.
    The tunnel will stay up as long as this object is still in scope and will be closed down on exit.

    """
    def __init__(self, host: str='127.0.0.1', port: int=8090, ssl_verify: bool=False, ssh_tunnel: bool=True,
                 username: str = '@', ssh_port: int=22, local_port: int=8090, remote_port: int=8090,
                 local_host: str='127.0.0.1', remote_host: str='127.0.0.1', version: int = 1, automatic=True):
        self._host = host
        self._port = port

        self._ssl_verify = ssl_verify
        self._automatic = automatic
        self._ssh_tunnel = ssh_tunnel
        self._username = username
        self._local_port = local_port
        self._remote_port = remote_port
        self._local_host = local_host
        self._remote_host = remote_host

        self._version = version

        self.logger = self.get_logger("{0}:{1}".format(self._host, self._port))

        self.json_headers = {
            'Accept': 'application/json;charset=utf-8',
            'Content-Type': 'application/json; charset=utf-8'
        }

        # configure an SSH tunnel if we need one
        if ssh_tunnel is True:
            self.tunnel = SSHTunnel(username, host, ssh_port, local_port, remote_port)
            # if we are tunnelling then set the host and port must be local
            self._host = '127.0.0.1'
            # if we are tunneling the set the port to match the local_port of the ssh tunnel
            self._port = local_port

        # this is the wallet cache , a dict of Wallets keyed by name
        self._wallets = {}

        # this is node info cache
        self._node_info = dict

        # automatically populate wallet cache and get node info
        if self._automatic:
            self.logger.info('Connecting to WalletAPI')
            self.get_node_info()
            self.fetch_wallet_list()

    def __del__(self):
        try:
            if self.tunnel:
                self.tunnel.server.shutdown()
            else:
                self.logger.info('SSH tunnel seems to have died of natural causes')
        except Exception as e:
            self.logger.error('Exception stopping ssh tunnel: {0}'.format(e))

    @property
    def wallets(self):
        """" A Generator that iterates through the wallet cache"""
        for name in self._wallets.keys():
            yield self._wallets[name]

    def random_wallet(self) -> Wallet:
        """" Random Wallet: Chooses a random wallet from the wallet cache

        Returns:
            Theseus.Wallet: a random wallet or an error wallet.

        """
        if self._wallets.items():
            return random.sample(list(self._wallets.values()), 1)[0]
        else:
            self.logger.info('No wallets in cache')
            return Wallet(id='empty', type='error', name='no wallets in cache')

    def get_logger(self, name):
        """ Get Logger: get a logger handle with the right prefixes

        Args:
            name(str): the name of your logger handle

        Returns:
            logger: a Logger object

        """
        return get_logger(name)

    def restore_wallet(self, name: str, phrase: str, password: str, assurance: str="strict") -> Wallet:
        """ Restore a Wallet: Restores a wallet via the daedalus api using the supplied credentials

        This is actually just a create but for a wallet that already exists and with operation set to
        restore not create. If you try to create an existing wallet you will get an empty one.

        Args:
            name (str): Wallet name
            phrase (str): Passphrase words seperated by spaces
            password (str): optional spending password
            assurance (str): assurance level strict or normal

        Returns:
            Daedalus.Wallet object

        Notes:
            The created wallet object will also be appended to the local wallet cache.

        """
        return self.create_wallet(name, phrase, password, assurance, operation='restore')

    def create_wallet(self, name: str, phrase: str, password: str='', 
                      assurance: str="strict", operation: str='create') -> Wallet:
        """ Create a Wallet: Creates a wallet via the wallet api using the supplied credentials

        Args:
            name (str): Wallet name
            phrase (str): Passphrase words separated by spaces
            password (str): optional spending password
            assurance (str): assurance level strict or normal
            operation (str): create or restore , defaults to create

        Returns:
            Daedalus.Wallet object

        Notes:
            The created wallet object will also be appended to the local wallet cache.
            The accounts data will be fetched for this wallet automatically
            To check the status of the operation properly you need to read the status field of the wallet
            in the event of an error you the status will be 'error', the ID will be a status code and the name will be an error message

        """
        # make payload structure for request
        payload = dict(
            operation=operation,
            backupPhrase=phrase.split(),
            assuranceLevel=assurance,
            name=name
        )

        if password:
            payload['spendingPassword'] = password

        url = "https://{0}:{1}/api/v{2}/wallets".format(self._host, self._port, self._version)

        # make request
        self.logger.info("Creating Wallet: Name: '{0}' Phrase: '{1}'".format(name, phrase))
        response = requests.post(url, verify=self._ssl_verify, headers=self.json_headers, data=json.dumps(payload))

        self.logger.debug('Wallet {0} returned: {1}'.format(operation, response.status_code))

        # handle error conditions by returning an error wallet
        if response.status_code == 400:
            self.logger.error('Error: {0}'.format(response.text))
            return Wallet(id=str(response.status_code), type="error", name="Invalid body in request")

        if response.status_code == 415:
            self.logger.error('Error: {0}'.format(response.text))
            return Wallet(id=str(response.status_code), type="error", name="Unsupported Media Type")

        if response.status_code == 406:
            self.logger.error('Error: {0}'.format(response.text))
            return Wallet(id=str(response.status_code), type="error", name="Invalid Charset")

        # we should now be safe to process the json
        response_data = response.json()
        if response_data['status'] == 'success':
            if operation == 'restore':
                # Todo: watch the operation until the status is done , more important for restore ,
                self.logger.info('Restore status: {0}'.format(response_data['data']['syncState']))

            wallet = Wallet(**response_data['data'])
            wallet.account = self.get_accounts(wallet)
            self._wallets.update({wallet.id: wallet})
            return wallet

        if response_data['status'] == 'failure':
            return Wallet(id=response.status_code, type='error', name="Wallet creation failed in the backend")

    def delete_wallet(self, wallet: Wallet)-> bool:
        """ Delete a wallet: Deletes a wallet from daedalus

        Args:
            wallet (Wallet): Wallet to delete

        Returns:
            boolean : True if wallet was deleted.

        """
        url = "https://{0}:{1}/api/v{2}/wallets/{3}".format(self._host, self._port, self._version, wallet.id)
        self.logger.info("Deleting wallet: {0} {1}".format(wallet.name, url))
        response = requests.delete(url, verify=self._ssl_verify, headers=self.json_headers)

        if response.status_code == 204:
            self.logger.info("Wallet deleted: {0}".format(wallet.name))
            return True
        if response.status_code == 404:
            self.logger.error("Walled deletion: ID not found")
            return False

        self.logger.info("Wallet deletion failed: {0} returned {1}".format(wallet.name, response.status_code))
        return False

    def delete_all_wallets(self) -> bool:
        """ Delete all the wallets: Deletes all the wallets from daedalus and the local wallet cache"""
        #try:
        for name in self.wallets:
            self.logger.info('Deleting wallet: {0}'.format(self._wallets[name]))
            self.delete_wallet(self._wallets[name].id())

        # empty the wallet cache so its in sync
        self._wallets = dict
        return True

    def fetch_wallet_list(self, id_filter: str="", balance_filter: str="", sort_by: str="", page: int=1, per_page: int=50):
        """ Fetch a list of wallets: Queries the daedalus wallet and updates the local wallet cache

        Args:
            id_filter (str): Filter specification for wallet IDs
            balance_filter (str): Filter specification for wallet balances
            sort_by (str) : sort specification for wallet listing
            page (int) : which page of wallet listings to show, default 1
            per_page(int) : how many listings to show on a page, default 50

        Returns:
            Dict: a Dict of Daedalus.Wallet objects that where found keyed by ID

        Notes:
            Defaults to fetching 100 wallets to avoid having to use using pagination
            Specification syntax can be found at https://cardanodocs.com/technical/wallet/api/v1/

        """
        url = "https://{0}:{1}/api/v{2}/wallets?page={3};per_page={4}".format(
            self._host, self._port, self._version, page, per_page)

        if id_filter:
            url += ";id={0}".format(id_filter)

        if balance_filter:
            url += ";balance={0}".format(balance_filter)

        if sort_by:
            sort_by += ";sort_buy".format(sort_by)

        response = requests.Response

        self.logger.debug("Fetching Wallet Listing: Url: '{0}'".format(url))
        try:
            response = requests.get(url, verify=self._ssl_verify, headers=self.json_headers)
        except ConnectionRefusedError as e:
            self.logger.error('Connection Refused: {0} check the details and the ssh tunnel make sense'.format(e))

        self.logger.info('Wallet listing request status code: {0}'.format(response.status_code))
        if response.status_code == 400:
            self.logger.error('Error: {0}'.format(response.text))
            return {}

        if response.status_code == 200:
            wallet_data = response.json()
            self.logger.info('Fetched Wallet: ' + json.dumps(wallet_data['data'], default=lambda o: o.__dict__, sort_keys=True, indent=4))
            wallets = wallet_data['data']
            self.logger.info('Fetched data on {0} wallets'.format(len(wallets)))

            temp_wallets = {}
            for wallet in wallets:
                # create a wallet object with all the values as kwargs, the keys match
                fresh = Wallet(**wallet)
                fresh.account = self.get_accounts(fresh)
                temp_wallets.update({wallet['id']: fresh})

            if id_filter:
                return temp_wallets[id_filter]

            if balance_filter or sort_by:
                # if we have filters don't update the cache , its a user query
                return temp_wallets
            else:
                self._wallets = temp_wallets
                return temp_wallets

    def dump_wallets(self):
        """ Dump Wallets: dumps the contents of the wallet cache to the logs """
        for name, wallet in self._wallets.items():
            self.logger.info('Wallet Cache Dump:')
            self.logger.info(wallet.dump())

    def transact(self, transaction_request: TransactionRequest) -> TransactionResponse:
        """ Transact: sends your transaction request to the backend to make it happen

        Send a transaction Request to the backend to make a transaction happen.

        Args:
            transaction_request (TransactionRequest) : A Transaction Request to enact

        Returns:
            TransactionResponse: the transaction response

        Notes:
            You will allways get a transaction response object and the status code for the request will be logged.

        """
        url = "https://{0}:{1}/api/v{2}/transactions".format(self._host, self._port, self._version)

        response = requests.post(url, verify=self._ssl_verify, headers=self.json_headers,
                                 data=transaction_request.to_json())
        self.logger.info('Transaction request status code: {0}'.format(response.status_code))
        if response.status_code == 400:
            self.logger.error('Error: {0}'.format(response.text))
        return TransactionResponse(response.text)

    def create_address(self, address_request: AddressRequest) -> AddressResponse:
        """ Create Address: creates a new receive address

        Args:
            address_request(AddressRequest): the address request

        Returns:
            AddressResponse: the Address response

        Notes:
            You will always get a address response object and the status code for the request will be logged.
            Look at the status field in the returned object to detect if the request worked.

        """

        url = "https://{0}:{1}/api/v{2}/addresses".format(self._host, self._port, self._version)

        response = requests.post(url, verify=self._ssl_verify, headers=self.json_headers, data=address_request.to_json())
        self.logger.info('Create address request status code: {0}'.format(response.status_code))
        if response.status_code == 400:
            self.logger.error('Error: {0}'.format(response.text))

        return AddressResponse(response.text)

    def get_accounts(self, wallet: Wallet):
        """ Get Accounts: get a list of accounts owned by a wallet

        Args:
            wallet (Wallet): Wallet to find the account of

        Returns:
            List of Accounts: a populated instance of Account

        """

        accounts = []

        url = "https://{0}:{1}/api/v{2}/wallets/{3}/accounts".format(self._host, self._port, self._version, wallet.id)

        response = requests.get(url, verify=self._ssl_verify, headers=self.json_headers)
        if response.status_code == 200:
            raw_json = json.loads(response.text)
            if raw_json['status'] == 'success':
                # create objects of each of the accounts
                for data in raw_json['data']:
                    accounts.append(Account(**data))
                return accounts

            if raw_json['status'] == 'failure':
                self.logger.error('Error fetching accounts: {0}'.format(response.error))

    def get_node_info(self):
        """ Get Node Information: Fetch and log node status info

        This is run when we first connect to the node

        You can access the data from it at self._node_info

        The spec for this is here
        https://cardanodocs.com/technical/wallet/api/v1/#tag/Info

        """
        url = "https://{0}:{1}/api/v{2}/node-info".format(self._host, self._port, self._version)
        response = requests.get(url, verify=self._ssl_verify, headers=self.json_headers)
        if response.status_code == 200:
            self._node_info = json.loads(response.text)
            self.logger.info("Node info: \n {0}".format(json.dumps(self._node_info, default=lambda o: o.__dict__, sort_keys=True, indent=4)))

    def update_wallet(self, id, assuranceLevel=None, name=None):
        """ Update the wallet with correspending ID in the backend to match the supplied wallet object

        Args:
            id(str): the wallet ID to update
            assuranceLevel(str): the assuranceLevel to apply
            name(str): the name to apply

        Returns:
            Wallet: updated wallet in sync with the backend.

        """
        # fetch wallet with unique ID , will be first in list
        wallet_to_update = self.fetch_wallet_list(id_filter=id)

        url = "https://{0}:{1}/api/v{2}/wallets/{3}".format(self._host, self._port, self._version, id)
        update = {}

        if assuranceLevel and wallet_to_update.assuranceLevel != assuranceLevel:
            update['assuranceLevel'] = assuranceLevel
        else:
            update['assuranceLevel'] = wallet_to_update.assuranceLevel

        if name and wallet_to_update.name != name:
            update['name'] = name
        else:
            update['name'] = wallet_to_update.name

        #  update field on backend
        response = requests.put(url, verify=self._ssl_verify, headers=self.json_headers, data=json.dumps(update))
        self.logger.info('Update wallet request status code: {0}'.format(response.status_code))
        if response.status_code == 400:
            self.logger.error('Error: {0}'.format(response.text))

        if response.status_code == 200:
            parsed = response.json()
            if parsed['status'] == 'success':
                # if its successful
                return Wallet(**parsed['data'])

            if parsed['status'] in ['failed', 'error']:
                self.logger.error('Error updating wallet: {0}'.format(response.text))
                return Wallet(id=str(response.status_code), type="error", name=response.reason)


