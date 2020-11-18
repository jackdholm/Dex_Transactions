import api_key_config
import TransactionList
import sys

if len(sys.argv) < 2:
    print ("Address argument required")
    exit()
address = str(sys.argv[1])
print(address)
txList = TransactionList.GetTransactions(address, api_key_config.API_KEY)
for i in txList:
    print(i)
