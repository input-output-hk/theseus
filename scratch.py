import Theseus
from Theseus import Daedalus

wallet_count = 20
wallet_name_length = 8

daedalus = Daedalus.API()

print(daedalus.dump_wallets())

#daedalus.restore_wallet('amias-iohk-2', 'reason gesture feel enforce vacant tissue couch knife bid culture wink mutual')

source = Daedalus.Source(wallet_id='Ae2tdPwUPEZHxSxjJ6Ce4D5ze8Q816mudmZQNsTr8sf9LVtJJRjJSxQwD7N', account_id=2147483648)

dests = []
dests.append(Daedalus.Destination(amount=5, address='Ae2tdPwUPEZJ2tpSsipDrKG6bdakTv1WHxN1Pwt3eEYEhR93nUsA9bMwzkt'))

treq = Daedalus.TransactionRequest(source, dests)

print(treq.to_json())

tres = daedalus.transact(treq)

print('TRES:{0}'.format(tres.dump()))
# tr = Daedalus.TransactionResponse('tr_id','cr_name',5,[],[],[],)
#
# print("Dump: {0}".format(tr.dump()))
# print("Json: {0}".format(tr.to_json()))
#
# dests = []
#
# for i in range(0, 5):
#     dests.append(Daedalus.Destination(i, 'dest-wallet-{0}'.format(i)))
#
# source = Daedalus.Source('1093120398120938', 'l3432kl4j324i32u4oi32u4o2iu3oi2o4iu23o')
# treq = Daedalus.TransactionRequest(source, dests, 'group', 'spend')
#
# print("Dump: {0}".format(treq.dump()))
# print("Json: {0}".format(treq.to_json()))
#
#


#wallet = daedalus.restore_wallet('amias-iohk-1', 'army elevator flash faint exotic ten calm one hunt volcano machine mystery')

#while True:
#    wallet = daedalus.create_wallet(Daedalus.generate_walletname(), Daedalus.generate_menmonic('english'))
#    time.sleep(3)
#    daedalus.delete_wallet(wallet)

#for wallet in daedalus.wallets:
#    daedalus.delete_wallet(wallet)
#    print("Deleted: {0}".format(wallet))


#for i in range(0, wallet_count):
#    phrase = generate_menmonic('english')
#    walletname = generate_walletname()
#
#    wallet = Wallet(walletname, phrase)
#
#    response = daedalus.create_wallet(walletname, phrase)
#    print ("Response: \n {0}".format(response.text))