import json

import requests

import Theseus.Daedalus


class API:
    def __init__(self, hostname='127.0.0.1:8090', version='1', ssl_verify=False):
        self._hostname = hostname
        self._version = version
        self._ssl_verify = ssl_verify

        self.logger = Theseus.Daedalus.get_logger('API')

        self.json_headers = {
            'Accept': 'application/json;charset=utf-8',
            'Content-Type': 'application/json; charset=utf-8'
        }

        self._wallets = []
        self.logger.info('Connecting to Daedalus: {0}'.format(hostname))
        self.fetch_wallet_list()

    # TODO: add dump to file option

    @property
    def wallets(self):
        return self._wallets

    def restore_wallet(self, name , phrase, password=False, assurance="strict"):
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
        self.create_wallet(name, phrase, password, assurance, operation='restore')

    def create_wallet(self, name, phrase, password=False, assurance="strict", operation='create'):
        """ Create a Wallet: Creates a wallet via the daedalus api using the supplied credentials

        Args:
            name (str): Wallet name
            phrase (str): Passphrase words seperated by spaces
            password (str): optional spending password
            assurance (str): assurance level strict or normal
            operation (str): create or restore , defaults to create
        Returns:
            Daedalus.Wallet object

        Notes:
            The created wallet object will also be appended to the local wallet cache.
        """
        # make payload structure for request
        payload = {}
        payload['operation'] = operation
        payload['backupPhrase'] = phrase.split()
        payload['assuranceLevel'] = assurance
        payload['name'] = name
        if password:
            payload['spendingPassword'] = password

        url = "https://{0}/api/v{1}/wallets".format(self._hostname, self._version)

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
                wallet = Theseus.Daedalus.Wallet(id=response_payload['id'], name=name, passphrase=phrase, assurance=assurance, balance=response_payload['balance'])
                self.wallets.append(wallet)
                return wallet

    def delete_wallet(self, wallet):
        """ Delete a wallet: Deletes a wallet from daedalus and the local wallet cache

        Args:
            wallet (Daedalus.Wallet): Wallet to delete

        Returns:
            boolean : True if wallet was deleted.
        """
        url = "https://{0}/api/v{1}/wallets/{2}".format(self._hostname, self._version, wallet.id)
        self.logger.info("Deleting wallet: {0}".format(wallet.name))
        response = requests.delete(url, verify=self._ssl_verify, headers=self.json_headers)

        if response.status_code == 204:
            self.logger.info("Wallet deleted: {0}".format(wallet.name))
            return True
        else:
            self.logger.info("Wallet deletion failed: {0} returned {1}".format(wallet.name, response.status_code))
            return False

    def delete_all_wallets(self):
        """ Delete all the wallets: Deletes all the wallets from daedalus and the local wallet cache"""
        for wallet in self.daedalus.wallets:
            self.daedalus.delete_wallet(wallet.id)

    def fetch_wallet_list(self, id_filter=False, balance_filter=False, sort_by=False, page=1, per_page=10):
        """ Fetch a list of wallets: Queries the daedalus wallet and updates the local wallet cache

        Args:
            id_filter (str): Filter specification for wallet IDs
            balance_filter (str): Filter specification for wallet balances
            sort_by (str) : sort specification for wallet listing

        Returns:
            List: a list of Daedalus.Walled objects that where found

        Notes:
            TODO: this only fetches 10 because its not using pagination
            Specification syntax can be found at https://cardanodocs.com/technical/wallet/api/v1/

        """
        parameters = {}
        parameters['page'] = page
        parameters['per_page'] = per_page
        if id_filter:
            parameters['id'] = id_filter
        if balance_filter:
            parameters['balance'] = balance_filter
        if sort_by:
            parameters['sort_by'] = sort_by

        url = "https://{0}/api/v{1}/wallets".format(self._hostname,self._version)

        self.logger.debug("Fetching Wallet Listing: Url: '{0}' JSON: '{1}'".format(url,parameters))
        response = requests.get(url, verify=self._ssl_verify, headers=self.json_headers, params=parameters)

        if response.status_code == 200:
            wallet_data = response.json()
            wallets = wallet_data['data']
            self.logger.info('Fetched data on {0} wallets'.format(len(wallets)))

            # if we have filters don't update the cache , its a user query
            if id_filter or balance_filter or sort_by:
                return wallets
            else:
                self._wallets.clear()
                for wallet in wallets:
                    fresh = Theseus.Daedalus.Wallet(id=wallet['id'], name=wallet['name'], balance=wallet['balance'])
                    self._wallets.append(fresh)
        else:
            self.logger.info('Wallet listed fetch failed: {0}'.format(response.status_code))
            return {}  # an empty list

    def dump_wallets(self):
        for wallet in self.wallets:
            self.logger.info('Wallet Cache Dump:')
            self.logger.info(wallet.dump())

    def transact(self, transaction_request):
        url = "https://{0}/api/v{1}/transactions".format(self._hostname, self._version)

        response = requests.post(url, verify=self._ssl_verify, headers=self.json_headers, data=transaction_request.to_json())

        if response.status_code == 200:
            tr = Theseus.Daedalus.TransactionResponse(response.content)
            return tr
        else:
            print("Error: {0}".format(response.content))