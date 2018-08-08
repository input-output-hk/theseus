import Theseus
import unittest2


class BigSpender(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.daedalus = Theseus.Daedalus.API(port=8094)   # testnet only !
        cls.faucet = Theseus.Faucet()

    def test_01_create_wallets(self):
        self.wallet_one = self.daedalus.create_wallet()
        self.assertIsInstance(self.wallet_one, Theseus.Daedalus.Wallet, "Created first wallet")

        self.wallet_two = self.daedalus.create_wallet()
        self.assertIsInstance(self.wallet_one, Theseus.Daedalus.Wallet, "Created first wallet")

    def test_02_create_receiving_addresses(self):
        self.wallet_one_response = self.daedalus.create_address(Theseus.AddressRequest(self.wallet_one))
        self.assertEqual(self.wallet_one_response.status, 'success', 'Wallet one address requested')
        self.wallet_one_address = self.wallet_one_response.data.id

        self.wallet_two_response = self.daedalus.create_address(Theseus.AddressRequest(self.wallet_two))
        self.assertEqual(self.wallet_two_response.status, 'success', 'Wallet two address requested')
        self.wallet_two_address = self.wallet_two_response.data.id

    def test_03_withdraw_funds_from_faucet(self):
        wallet_one_withdraw_response = self.faucet.withdraw(self.wallet_one_address)
        self.assertEqual(wallet_one_withdraw_response.status, 'success', msg="Wallet one withdraw succeeded")

        # might need to wait for 5 seconds here for the faucet rate limiting

        wallet_two_withdraw_response = self.faucet.withdraw(self.wallet_two_address)
        self.assertEqual(wallet_two_withdraw_response.status, 'success', msg="Wallet two withdraw succeeded")

    def test_04_spending_spree(self):
        # update the list of wallets in the cache to reflect new balances BUT it doesn't update my wallet objects ?
        self.daedalus.fetch_wallet_list()

        # make some spending loops

    def test_05_send_back_to_faucet(self):
        faucet_address = self.faucet.get_return_address()
        self.assertNotEqual(faucet_address, '', msg="a faucet address was returned")

        faucet_destination_one = Theseus.TransactionDestination(amount=self.wallet_one.balance, address=faucet_address)
        faucet_source_one = Theseus.TransactionSource(account_id=self.wallet_one.account, wallet_id=self.wallet_one.id)
        return_transaction_one = Theseus.TransactionRequest(source=faucet_source_one,
                                                            destinations=faucet_destination_one)
        self.assertEqual(return_transaction_one.status, 'success',
                         msg="{0} was returned to the faucet from wallet one".format(self.wallet_one.balance))

        faucet_destination_two = Theseus.TransactionDestination(amount=self.wallet_two.balance, address=faucet_address)
        faucet_source_two = Theseus.TransactionSource(account_id=self.wallet_two.account, wallet_id=self.wallet_two.id)
        return_transaction_two = Theseus.TransactionRequest(source=faucet_source_two,
                                                            destinations=faucet_destination_two)

        self.assertEqual(return_transaction_two.status, 'success',
                 msg="{0} was returned to the faucet from wallet two".format(self.wallet_two.balance))
