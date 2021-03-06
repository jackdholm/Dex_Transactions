import requests
import json
import datetime

class TransactionPair:
    complete = False
    _sent = {}
    _received = {}
    @property
    def sent(self):
        return self._sent
    @sent.setter
    def sent(self, value):
        self._sent = value
        if len(self._sent) > 0 and len(self.received) > 0:
            self.complete = True
    @property
    def received(self):
        return self._received
    @received.setter
    def received(self, value):
        self._received = value
        if len(self._sent) > 0 and len(self._received) > 0:
            self.complete = True

def MakeDict(address, *lists):
    transactions = {}
    combined = []
    for l in lists:
        combined += l
    for i in combined:

        if 'isError' in i and i['isError'] == '1':
            continue
        hash = i['hash']
        if hash not in transactions:
            transactions[hash] = TransactionPair()
        if i['from'] == address.lower():
            transactions[hash].sent = i.copy()
        else:
            transactions[hash].received = i.copy()
    return transactions
def GetTransactions(address, apiKey):
    responseParams = dict(module = "account", apikey = apiKey, address = address, startblock = "0", endblock = "99999999", sort = "asc", action  = "txlist")
    responseERCParams = dict(module = "account", apikey = apiKey, address = address, startblock = "0", endblock = "99999999", sort = "asc", action  = "tokentx")
    response = requests.get("https://api.etherscan.io/api", params = responseParams)
    responseERC = requests.get("https://api.etherscan.io/api", params = responseERCParams)
    
    output = json.loads(response.text)
    outputERC = json.loads(responseERC.text)
    ercList = outputERC['result']
    transactionList = output['result']
    print("status: ", output['status'])
    if not transactionList:
        return []
    TxList = MakeDict(address, transactionList, ercList)
    outputList = []
    for i in TxList:
        if TxList[i].complete:
            timeStamp = datetime.datetime.utcfromtimestamp(int(TxList[i].sent['timeStamp']))
            if 'tokenSymbol' in TxList[i].sent:
                assetTraded = TxList[i].sent['tokenSymbol']
            else:
                assetTraded = 'ETH'
            if 'tokenSymbol' in TxList[i].received:
                assetReceived = TxList[i].received['tokenSymbol']
            else:
                assetReceived = 'ETH'
            cost = int(TxList[i].sent['value']) / 1000000000000000000
            gasPrice = int(TxList[i].sent['gasPrice']) / 1000000000000000000
            transactionFee = gasPrice * int(TxList[i].sent['gasUsed'])
            amountTraded = cost + transactionFee
            amountReceived = int(TxList[i].received['value']) / 1000000000000000000
            outputList.append([timeStamp, assetTraded, cost, transactionFee, amountTraded, assetReceived, amountReceived])

    return outputList
