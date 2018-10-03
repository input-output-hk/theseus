Theseus package
===============

*"Theseus battled and overcame foes that were identified with an archaic religious and social order: “This was a major cultural transition, like the making of the new Olympia by Hercules”*

Theseus is a system for orchestrating test scenarios with Daedalus and other IOHK projects.

Heres an example showing wallet creation on a local instance.

.. code-block:: python3

    import Theseus
    import Daedalus

    daedalus = daedalus()

    for i in range(0, wallet_count):
        phrase = generate_menmonic('english')
        walletname = generate_walletname()

        wallet = Wallet(walletname, phrase)

        if daedalus.create_wallet(walletname, phrase)
            print("Created Wallet: {0}").format(wallet.dump())


By default the daedalus object will connect to a local wallet API running on a cardano-node on 127.0.0.1:8090.

if you want to control a remote instance of daedalus then just forward the ports with ssh first.


Subpackages
-----------

.. toctree::
    Cardano
    Common
    Daedalus
    Logging
    Protocols
    Secrets
    Time

Module contents
---------------

.. automodule:: Theseus
    :members:
    :undoc-members:
    :show-inheritance:
