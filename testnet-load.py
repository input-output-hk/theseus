import unittest2

from Theseus import Daedalus, Wallet, TransactionRequest, Source, Destination


class TestnetHeavy(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.daedalus = Daedalus.API()
        cls.logger = Daedalus.get_logger('TestnetHeavy')

    def test_01_list_wallets(self):
        for wallet in self.daedalus.wallets:
            self.assertIsInstance(wallet, Wallet)
            self.logger.info('Found wallet: {0} - {1}'.format(wallet.name, wallet.account))

    def test_02_send_loop(self):
        sending_account = 2147483648
        sending_wallet = "Ae2tdPwUPEZ4HPmZEzmLoWAYt9HFyATZAqtoZpGLprnzgdCaFnvW6QBm7re"
        #                 "DdzFFzCqrht1PyXfhi66ehsFsw1RrtdBf2DguajzQPq3uf6h1kbB8XptsGEvFWpLTPcee1wzRbxqfWhSNcKDCXqsjb36JniBf9R3xPSk"
        destination_wallet = "DdzFFzCqrhtBvacp9mvTJCrpW51shPLBxeshaajw9sE6rP1ZqJ2zuMsNfNvLHWRBsT6RsaBy6wM3RsGVa6nrogkCojcRu8HGfT5y1zP3"

        sendfrom = Source(sending_account, sending_wallet)
        sendto = Destination(1000000, destination_wallet)

        tr = TransactionRequest(source=sendfrom, destinations=[sendto])

        response = self.daedalus.transact(tr)
        self.logger.info(response.dump())


if __name__ == "__main__":
    unittest2.main()
