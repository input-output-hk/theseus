import os
import random
import mnemonic
import string


def generate_menmonic(language):
    """ Generate Mnemonic: Creates insecure random nmemonics for testing

    Args:
        language (str): defaults to english , all bip languages are supported.

    Notes:
        These values MUST not be used for wallets with real ADA as they are
        not securely generated and could be predictable.
    """
    phrase_generator = mnemonic.Mnemonic(language)

    # make some insecure entropy
    strength_bits = 128
    entropy = os.urandom(strength_bits // 8)

    # make a phrase from it
    return phrase_generator.to_mnemonic(entropy)


def generate_walletname(evil=0, length=8):
    """ Generate Walletname: Creates wallet names of varying lengths and evilness

    Args:
        evil (int): 1 = alphanumeric , 2 = punctuation , 3 = any printable charecter
        length (int): length of wallet name

    Notes:

        Python string constants are used to create the charecter lists
        https://docs.python.org/3.4/library/string.html
    """
    # configurable levels of evil content for wallet names
    if evil == 0:
        string_options = string.ascii_uppercase + string.digits
    if evil == 1:
        string_options = string.punctuation
    if evil == 2:
        string_options = string.printable

    return ''.join(random.choices(string_options, k=length))