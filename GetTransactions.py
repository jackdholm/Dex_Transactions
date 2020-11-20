import api_key_config
import TransactionList
import sys
import csv

rowNames = ["Timestamp", "Asset Traded", "Cost", "Transaction Fee", "Amount Traded", "Asset Received", "Amount Received"]

if len(sys.argv) < 2:
    print ("Address argument required")
    exit()

address = str(sys.argv[1])
if len(sys.argv) >= 3 and len(str(sys.argv[2])) > 0:
    filename = str(sys.argv[2])
else:
    filename = "Transaction_List.csv"

txList = TransactionList.GetTransactions(address, api_key_config.API_KEY)

with open(filename, "w", newline="") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(rowNames)
    for row in txList:
        writer.writerow(row)
