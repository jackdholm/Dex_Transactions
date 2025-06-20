import api_config
import TransactionList
import csv
import io
import base64
import json

filename = "Transaction_List.csv"
def lambda_handler(event, context):
    try:
        rowNames = ["Timestamp", "Asset Traded", "Cost", "Transaction Fee(ETH)", "Asset Received", "Amount Received"]
        params = event.get("queryStringParameters") or {}
        address = params.get("address")
        if address == None or address == "":
            return {
                'Access-Control-Allow-Origin': api_config.ORIGIN,
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'GET',
                'statusCode': 400,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({"error": "Address argument required"})
            }
            
        txList = TransactionList.GetTransactions(address, api_config.API_KEY)
        
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(rowNames)
        for row in txList:
            writer.writerow(row)

        csv_bytes = csv_buffer.getvalue().encode('utf-8')
        csv_b64 = base64.b64encode(csv_bytes).decode('utf-8')

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': api_config.ORIGIN,
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename="{filename}"'
            },
            'body': csv_b64,
            'isBase64Encoded': True
        }
    except Exception as e:
        # Return error details for debugging
        return {
            'statusCode': 500,
            'headers': { 
                'Access-Control-Allow-Origin': api_config.ORIGIN,
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({ "error": str(e) })
        }