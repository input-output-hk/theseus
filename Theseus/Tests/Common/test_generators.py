import Theseus
import unittest2


class TestTheseusGenerators(unittest2.TestCase):
    def setUp(self):
        self.logger = Theseus.get_logger(self._testMethodName)
        self.logger.info(self._testMethodName + ' - ' + self._testMethodDoc)

    def test_generate_and_check_mnemonics(self):
        """ Generate and check menemonic in each of the supported languages """

        languages = ['english']

        loops = range(100)

        all_mnemonics = {}

        for loop in loops:
            for language in languages:
                self.logger.info('Testing: loop={0} language={1}'.format(loop, language))

                # generate a set of  mnemonics
                phrase = Theseus.generate_mnemonic(language)

                # check the types are strings
                self.assertIsInstance(phrase, str, msg="Mnemonic list returned")

                # ensure they contain valid words
                self.assertTrue(Theseus.check_mnemonic(phrase), msg="Mnemonic passed validation")

                # use a dict to check we haven't seen this phrase before in this test run
                self.assertIsNone(all_mnemonics.get(phrase), msg="Phrase not encounted in this test")
                
                # add phrase to dict for comparison with other tests
                update = {phrase: Theseus.timestamp()}
                all_mnemonics.update(update)

    def test_generate_walletname(self):
        """ Generate a series of wallet names of varying lengths and evilness """
        evilness_modes = [0, 1, 2]
        lengths = [8, 256]
        loops = range(100)

        for loop in loops:
            for length in lengths:
                for mode in evilness_modes:
                    name = Theseus.generate_walletname(evil=mode, length=length)
                    self.logger.info("Testing: evil:{0} length:{1} loop:{2} \n name:{3}".format(mode, length, loop, name))
                    self.assertIsInstance(name, str, msg="Wallet name is a string")
                    self.assertEqual(len(name), length, msg="string is the right length")