import time
import typing
import unittest2
import shutil
import nose

from Theseus import Daedalus, Secrets, Wallet, generate_mnemonic, generate_walletname, get_logger


class TestWalletCreateDelete(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.secrets = Secrets()
        cls.daedalus = Daedalus(**cls.secrets.get('Daedalus'))

    @classmethod
    def tearDownClass(cls):
        cls.daedalus.tunnel.stop_tunnel()

    def setUp(self):
        self.logger = get_logger(self._testMethodName)
        self.logger.info(self._testMethodName + ' - ' + self._testMethodDoc)

    @unittest2.skip
    def test_01_delete_all_wallets(self):
        """ Delete all wallets on this backend """
        for wallet in self.daedalus.wallets:
            self.logger.info("Deleting wallet: {0}".format(wallet))
            response = self.daedalus.delete_wallet(wallet)
            self.assertTrue(response, msg="wallet deleted")

    def test_02_create_wallets(self):
        """ Create and Delete 5 wallets with alphannumeric names"""
        wallet_count = 5
        standoff = 3
        for i in range(wallet_count):
            phrase = generate_mnemonic('english')
            walletname = generate_walletname()

            wallet = self.daedalus.create_wallet(name=walletname, phrase=phrase)
            self.assertIsInstance(wallet, Wallet, msg="Made a wallet")

            print(wallet.dump())

            time.sleep(standoff)

            delete_response = self.daedalus.delete_wallet(wallet)
            self.assertTrue(delete_response, msg="wallet deleted successfully")

    def test_03_create_evil_wallets(self):
        """ Create and Delete 5 wallets with complex characters in their names """
        wallet_count = 5
        standoff = 3
        for i in range(wallet_count):
            phrase = generate_mnemonic('english')
            walletname = generate_walletname(evil=1)

            wallet = self.daedalus.create_wallet(name=walletname, phrase=phrase)
            self.assertIsInstance(wallet, Wallet, msg="Made a wallet")

            time.sleep(standoff)

            delete_response = self.daedalus.delete_wallet(wallet)
            self.assertTrue(delete_response, msg="wallet deleted successfully")
