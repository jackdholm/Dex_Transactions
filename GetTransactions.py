import api_key_config
import TransactionList
import sys
import csv

def PrintRow(row):
    for i in row[0:len(row)-1]:
        print(i, end = ",")
    print(row[len(row)-1])

rowNames = ["Timestamp", "Asset Traded", "Cost", "Transaction Fee(ETH)", "Asset Received", "Amount Received"]

if len(sys.argv) < 2:
    print ("Address argument required")
    exit()

address = str(sys.argv[1])
filename = "Transaction_List.csv"
printStd = False
printFile = True

i = 2
while i < len(sys.argv):
    if str(sys.argv[i]) == "--filename":
        i += 1
        if i < len(sys.argv):
            filename = str(sys.argv[i])
    elif str(sys.argv[i]) == "--print":
        printStd = True
    elif str(sys.argv[i]) == "--nofile":
        printFile = False
    i += 1
    
txList = TransactionList.GetTransactions(address, api_key_config.API_KEY)

if printStd:
    PrintRow(rowNames)
    for row in txList:
        PrintRow(row)
if printFile:
    with open(filename, "w", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(rowNames)
        for row in txList:
            writer.writerow(row)
