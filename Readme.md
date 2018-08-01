**Theseus**

Theseus battled and overcame foes that were identified with an archaic religious and social order , he was responsible for the synoikismos ("dwelling together") of ancient greece and of course was good at taking direction from illustrious engineers.


**What does it do ?**

This tool is a python3 module and supporting code that provides a testing framework for cardano based tools.

Theseus provides:
   * Cardano wallet API Control  
   * Daedalus Wallet Control
   * Utilities for generating test data
   * Logging
   * Test Dependency packaging and delivery
   * Inline Documentation

Coming soon:
   * SSH tunnels to access remote instances
   * remote installation of Daedalus


**How do i use it ?**

Heres a basic example of some code to create an arbitrary amount of wallets on a local node

    import Theseus
    import Daedalus

    daedalus = daedalus.API()

    for i in range(0, wallet_count):
        phrase = generate_menmonic('english')
        walletname = generate_walletname()

        wallet = Wallet(walletname, phrase)

        if daedalus.create_wallet(walletname, phrase)
            print("Created Wallet: {0}").format(wallet.dump())
            
**Is there documentation**

Yes , there is inline documentation 
     cd sphinx
     make html
     <webbrowser> build/html/index.html
     
 for more formats such as latex and pdf you can find the options at make help


**How is it distributed ?**

The simplest way to make use of theseus is when its compiled into a egg file , this 
is similar to a jar file in that its a zip of the files with a little bit of magic to make it runnable.

***Build the egg***

    python3 setup.py bdist_egg
    
An egg file should be made in the dist folder, eventually this wil be a CI process.

***Install the eggs and its dependencies in virtualenv (doesnt contaminate your OS)***    
    
    virtualenv theseus -p python3
    cd theseus
    source bin/activate
    python3 easy_install -f "path/to/file.egg"