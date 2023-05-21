import os
from controller import generate_address_to_crypto, list_addresses, retrieve_address, persist_address
import json

def lambda_handler(event, context):
    print(f"Event {event}")
    address_id = int(event['pathParameters']['address_id'])
    address = retrieve_address(address_id)
    if address:
        return {"address": address}
    else:
        return {"error": f"Address Id {address_id} not found"}, 400