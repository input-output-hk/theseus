import json
from typing import Dict, List, Iterable
import requests

#  import only the specific parts of theseus we need
from Theseus.Common.Wallet import Wallet
from Theseus.Common.Transaction import TransactionRequest, TransactionResponse
from Theseus.Protocols.SSHTunnel import SSHTunnel
from Theseus.Common.Address import AddressResponse, AddressRequest

# hack to stop urlib3 complaining when we turn off SSL warnings
import urllib3
urllib3.disable_warnings()


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
                 local_host: str='127.0.0.1', remote_host: str='127.0.0.1', version: int = 1):
        self._host = host
        self._port = port

        self._ssl_verify = ssl_verify

        self._ssh_tunnel = ssh_tunnel
        self._username = username
        self._local_port = local_port
        self._remote_port = remote_port
        self._local_host = local_host
        self._remote_host = remote_host

        self._version = version

        self.logger = self.get_logger(self.__class__.__name__)

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

        # this is the wallet cache , a Dict of Wallets
        self._wallets = List[Wallet]

        self.logger.info('Connecting to Daedalus')
        self.fetch_wallet_list()

    @property
    def wallets(self) -> Iterable[Wallet]:
        return self._wallets

    def get_logger(self):
        Theseus.get_logger
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
        """ Create a Wallet: Creates a wallet via the daedalus api using the supplied credentials

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

        if response.status_code == 201:
            response_data = response.json()
            if response_data['status'] == 'success':
                response_payload = response_data['data']
                if operation == 'restore':
                    self.logger.info('Restore status: {0}'.format(response_data['data']['syncState']))
                wallet = Theseus.Daedalus.Wallet(id=response_payload['id'], name=name, passphrase=phrase,
                                                 assurance=assurance, balance=response_payload['balance'])
                self.wallets.append(wallet)
                return wallet

    def delete_wallet(self, wallet: Wallet)-> bool:
        """ Delete a wallet: Deletes a wallet from daedalus

        Args:
            wallet (Daedalus.Wallet): Wallet to delete

        Returns:
            boolean : True if wallet was deleted.
        """
        url = "https://{0}:{1}/api/v{2}/wallets/{3}".format(self._host, self._port, self._version, wallet.id)
        self.logger.info("Deleting wallet: {0}".format(wallet.name))
        response = requests.delete(url, verify=self._ssl_verify, headers=self.json_headers)

        if response.status_code == 204:
            self.logger.info("Wallet deleted: {0}".format(wallet.name))
            return True
        else:
            self.logger.info("Wallet deletion failed: {0} returned {1}".format(wallet.name, response.status_code))
            return False

    def import_wallet(self, wallet_number: int=0)-> bool:
        """ Import Wallet: Import a poor wallet

        This is only available on cardano nodes

        Args:
            wallet_number (int) : Poor Key number (0-11)

        Returns:
            boolean: True if wallet is was imported
        """
        url = " https://{0}:{1}/api/internal/import-wallet".format(self._host, self._port)
        payload = dict(
            filePath="state-demo/genesis-keys/generated-keys/poor/key{0}.sk".format(wallet_number)
        )
        self.logger.info("Importing Poor Wallet: {0}".format(wallet_number))
        response = requests.post(url, verify=self._ssl_verify, headers=self.json_headers, data=json.dumps(payload))

        if response.status_code == 200:
            self.logger.info("Poor wallet was imported")
            return True
        else:
            self.logger.error("Error importing poor wallet: {0}".format(response.content))
            return False

    def delete_all_wallets(self) -> bool:
        """ Delete all the wallets: Deletes all the wallets from daedalus and the local wallet cache"""
        try:
            for wallet in self.wallets:
                self.delete_wallet(wallet.id)
            return True
        except Exception:
            return False

    def fetch_wallet_list(self, id_filter: str="", balance_filter: str="", sort_by: str="", page: int=1, per_page: int=10)-> List[Wallet]:
        """ Fetch a list of wallets: Queries the daedalus wallet and updates the local wallet cache

        Args:
            id_filter (str): Filter specification for wallet IDs
            balance_filter (str): Filter specification for wallet balances
            sort_by (str) : sort specification for wallet listing
            page (int) : which page of wallet listings to show, default 1
            per_page(int) : how many listings to show on a page, default 10

        Returns:
            List: a List of Daedalus.Wallet objects that where found

        Notes:
            TODO: this only fetches 10 because its not using pagination yet
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

        if response.status_code == 200:
            wallet_data = response.json()
            self.logger.info(wallet_data['data'])
            wallets = wallet_data['data']
            self.logger.info('Fetched data on {0} wallets'.format(len(wallets)))

            # if we have filters don't update the cache , its a user query
            if id_filter or balance_filter or sort_by:
                return wallets
            else:
                self._wallets = []
                for wallet in wallets:
                    fresh = Theseus.Daedalus.Wallet(id=wallet['id'], name=wallet['name'], balance=wallet['balance'])
                    self._wallets.append(fresh)
        else:
            self.logger.info('Wallet listed fetch failed: {0}'.format(response.status_code))
            return List[Wallet]  # an empty list

    def dump_wallets(self):
        """ Dump Wallets: dumps the contents of the wallet cache to the logs """
        for wallet in self.wallets:
            self.logger.info('Wallet Cache Dump:')
            self.logger.info(wallet.dump())

    def transact(self, transaction_request: TransactionRequest) -> TransactionResponse:
        """ Transact: sends your transaction request to the backend to make it happen

        Args:
            transaction_request (TransactionRequest) : A Transaction Request to enact

        Returns:
            TransactionResponse: the tran
        """
        url = "https://{0}:{1}/api/v{2}/transactions".format(self._host, self._port, self._version)

        response = requests.post(url, verify=self._ssl_verify, headers=self.json_headers,
                                 data=transaction_request.to_json())

        if response.status_code == 200:
            return TransactionResponse(response.text)
        else:
            return TransactionResponse("status:'failed'")

    def create_address(self, address_request: AddressRequest) -> AddressResponse:
        """ Create Address: creates a new receive address

        Args:
            address_request(AddressRequest): the address request

        Returns:
            AddressResponse: the Address resposne
        """

        url = "https://{0}:{1}/api/v{2}/addresses".format(self._host, self._port, self._version)

        response = requests.post(url, data=AddressRequest)
        if response.status_code == 200:
            return AddressResponse(response.text)
        else:
            return AddressResponse('"status":"error"')
        