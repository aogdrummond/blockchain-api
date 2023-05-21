from controller import generate_address_to_crypto, list_addresses, retrieve_address, persist_address
import json

def lambda_handler(event, context):

    data = json.loads(event["body"])
    crypto_currency = data.get("crypto_currency")
    if crypto_currency:
        address = generate_address_to_crypto(crypto_currency)
        persist_address(address, crypto_currency)
        
        return {
        'statusCode': 201,
        'body': json.dumps({"address": address})
    }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Hello from Lambda!')
        }

