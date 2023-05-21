import os
from controller import  list_addresses, retrieve_address, persist_address
import json

def lambda_handler(event, context):

    addresses = list_addresses()
    return {
        'statusCode': 200,
        'body': json.dumps({"addresses": addresses})}
    