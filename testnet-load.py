import unittest2

from Theseus import Daedalus, Wallet, TransactionRequest, TransactionSource, TransactionDestination


class TestnetHeavy(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.daedalus = Daedalus.API(host='127.0.0.1', port='8090')
        cls.logger = Daedalus.get_logger('TestnetHeavy')

    def test_01_list_wallets(self):
        for wallet in self.daedalus.wallets:
            self.assertIsInstance(wallet, Wallet)
            self.logger.info('Found wallet: {0} - {1}'.format(wallet.name, wallet.account))

    @unittest2.skip('')
    def test_02_send_one(self):

        # this is amias wallet on testnet
        sending_account = 2147483648
        sending_wallet = "Ae2tdPwUPEZ4HPmZEzmLoWAYt9HFyATZAqtoZpGLprnzgdCaFnvW6QBm7re"

        # this is alans wallet on testnet
        destination_wallet = "DdzFFzCqrhtBvacp9mvTJCrpW51shPLBxeshaajw9sE6rP1ZqJ2zuMsNfNvLHWRBsT6RsaBy6wM3RsGVa6nrogkCojcRu8HGfT5y1zP3"

        sendfrom = TransactionSource(sending_account, sending_wallet)
        sendto = TransactionDestination(1000000, destination_wallet)

        tr = TransactionRequest(source=sendfrom, destinations=[sendto])
        response = self.daedalus.transact(tr)

        self.logger.info(response.dump())

    @unittest2.skip('')
    def test_03_send_hundred(self):
        iterations = 100

        # this is amias wallet on testnet
        sending_account = 2147483648
        sending_wallet = "Ae2tdPwUPEZ4HPmZEzmLoWAYt9HFyATZAqtoZpGLprnzgdCaFnvW6QBm7re"

        # this is alans wallet on testnet
        destination_wallet = "DdzFFzCqrhtBvacp9mvTJCrpW51shPLBxeshaajw9sE6rP1ZqJ2zuMsNfNvLHWRBsT6RsaBy6wM3RsGVa6nrogkCojcRu8HGfT5y1zP3"

        sendfrom = TransactionSource(sending_account, sending_wallet)
        sendto = TransactionDestination(1000000, destination_wallet)

        for count in range(iterations):
            self.logger.info('Sending transaction {0} of {1}'.format(count, iterations))
            tr = TransactionRequest(source=sendfrom, destinations=[sendto])
            response = self.daedalus.transact(tr)
            self.logger.info(response.dump())
            self.assertEqual(response.status, 'success', 'Transaction {0} of {1} succeeded'.format(count, iterations))

    def test_04_multi_destination(self):

        iterations = 50

        sending_account = 2147483648
        sending_wallet = "Ae2tdPwUPEZ4HPmZEzmLoWAYt9HFyATZAqtoZpGLprnzgdCaFnvW6QBm7re"

        destination_wallets = [
            'DdzFFzCqrhstAx8ivLGEbjAFvQK13qv5voWiX76qjGrwrjqgreJMm1HiUCJTikhrSWSuwLXZGRTbvd9JiKY2bBTRLq9uQVnSBnNkqior',
            'DdzFFzCqrhsw5bVPxezVx72LCzj4N3ySXHVnFJRn2XsivDZzHnBxkBQUxMtCWW2Q5k3mU1WJcMVxi6NEbcjZW7gk6TG4reEjBVmmzKyf',
            'DdzFFzCqrhtCXdLKrFeeAsYnbBuvjNLfM8moVuAWNuQBKkatboMHs6iSX9YnVQMbetSyyUuJXhJMoKYYUjfB4vvoka2YW8fi5zKhyVf7',
            'DdzFFzCqrhtBvacp9mvTJCrpW51shPLBxeshaajw9sE6rP1ZqJ2zuMsNfNvLHWRBsT6RsaBy6wM3RsGVa6nrogkCojcRu8HGfT5y1zP3'
        ]

        sendfrom = TransactionSource(sending_account, sending_wallet)
        sendto = []
        for dest_wallet in destination_wallets:
            sendto.append(TransactionDestination(1000000, dest_wallet))

        for count in range(iterations):
            self.logger.info('Sending multi transaction {0} of {1}'.format(count, iterations))

            tr = TransactionRequest(source=sendfrom, destinations=sendto)
            response = self.daedalus.transact(tr)
            self.logger.info(response.dump())

            self.assertEqual(response.status, 'success', 'Transaction {0} of {1} succeeded'.format(count, iterations))


# start unittest2 to run these tests
if __name__ == "__main__":
    unittest2.main()
