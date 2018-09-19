import time
import typing
import unittest2
import shutil

from Theseus import Daedalus, Secrets, Wallet, generate_mnemonic, generate_walletname


class TestWalletCreateDelete(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.secrets = Secrets()
        cls.username = cls.secrets.get('Daedalus')['username']
        cls.host = cls.secrets.get('Daedalus')['host']

        cls.daedalus = Daedalus(ssh_tunnel=True, username=cls.username, host=cls.host)
        cls.logger = Daedalus.get_logger('hatred')

    def test_01_delete_all_wallets(self):
        for wallet in self.daedalus.wallets:
            self.logger.info("Deleting wallet: {0}".format(wallet))
            response = self.daedalus.delete_wallet(wallet)
            self.assertTrue(response, msg="wallet deleted")

    def test_02_create_wallets(self):
        wallet_count = 5
        standoff = 3
        for i in range(0, wallet_count):
            phrase = generate_mnemonic('english')
            walletname = generate_walletname()

            wallet = self.daedalus.create_wallet(name=walletname, phrase=phrase)
            self.assertIsInstance(wallet, Wallet, msg="Made a wallet")

            print(wallet.dump())

            time.sleep(standoff)

            delete_response = self.daedalus.delete_wallet(wallet)
            self.assertTrue(delete_response, msg="wallet deleted successfully")

    @unittest2.skip
    def test_03_create_evil_wallets(self):
        wallet_count = 10
        standoff = 3
        for i in range(0, wallet_count):
            phrase = Daedalus.generate_menmonic('english')
            walletname = Daedalus.generate_walletname(evil=2)

            wallet = self.daedalus.create_wallet(name=walletname, phrase=phrase)
            self.assertIsInstance(wallet, Wallet, msg="Made a wallet")

            time.sleep(standoff)

            delete_response = self.daedalus.delete_wallet(wallet)
            self.assertTrue(delete_response, msg="wallet deleted successfully")
