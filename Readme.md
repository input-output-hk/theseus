**Theseus**

Theseus battled and overcame foes that were identified with an archaic religious and social order , he was responsible for the synoikismos ("dwelling together") of ancient greece and of course was good at taking direction from illustrious engineers.


**What does it do ?**

This tool is a python3 module and supporting code that provides a testing framework for cardano based tools.

Theseus provides:
   * Cardano Wallet API Control  
   * Daedalus Wallet Control
   * Utilities for generating test data
   * Logging
   * Test Dependency packaging and delivery
   * Inline Documentation
   * SSH tunnels to access remote instances

WIP
   * Faucet withdrawals and returns  
   
Coming soon:
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
            
This will connect to a local instance on 127.0.0.1:8090.

If you want to control a remote installation an ssh tunnel will be created automatically.

    daedaus.API(host='remotehost' port=1234)

        
**Is there documentation**

Yes , there is inline documentation with the code , it can be extracted with sphinx to make external documentation.

     cd sphinx
     make html
     
 Your documentation will be viewable at ***sphinx/build/html/index.html***
     
 Documentation can be output in other formats such as latex and pdf , run make help for details.


**How is it distributed ?**

The simplest way to make use of theseus is when its compiled into a egg file , this 
is similar to a jar file in that its a zip of the files with a little bit of magic to make it runnable.

***Build the egg***

    python3 setup.py bdist_egg
    
An egg file should be made in the dist folder, eventually this wil be a CI process.

***Install the eggs and dependencies***

  This is best done in a virtualenv which is a private store of python libraries that 
  doesnt contaminate your OS or give you versioning conflicts. These setup and activate
  a virtualenv for theseus.
    
    virtualenv theseus -p python3
    cd theseus
    source bin/activate
  
  This will install the dependencies of the egg file and make it availble for use.
  
    python3 easy_install -f "path/to/file.egg"
