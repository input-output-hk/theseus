import requests
import Theseus
from typing import Dict

# this hasn't been run yet , the captcha is getting in the way
# it may need to be replaced by a specific wallet containing funds for tests


class Faucet:
    def __init_(self, network: str='TestNet'):

        self._faucet_base_url = str
        self.logger = Theseus.get_logger('faucet_{0}'.format(network))

        if network == 'TestNet':
            self._faucet_base_url = 'https://cardano-faucet.cardano-testnet.iohkdev.io'
        else:
            self.logger.error('Only testnet has a faucet at the moment')

    def withdraw(self, adddress):
        """ Withdraw - request a transfer of funds from the faucet to your wallet

        Args:
            adddress(str): the wallet address to transfer to

        Returns:
            FaucetResponse: the response data from the faucet

        """
        captcha = 'string'
        payload: Dict[str, str] = {
            'addresss': adddress,
            'g-recaptcha-response': captcha
        }
        response = requests.post(self._faucet_base_url + '/withdraw', data=payload)

        if response.status_code == 200:
            return Theseus.TransactionResponse(response.text)
        else:
            return Theseus.TransactionResponse('"status": "failed"')

    def get_return_address(self):
        """ Get return address - gets a fresh return address for returning your test ada

        Returns:
            str: a return address or an empty string
        """
        response = requests.get(self._faucet_base_url + '/return-address')

        if response.status_code == 200:
            return response.text
        else:
            return ''
