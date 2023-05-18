"""
Manter esse trecho genérico para que possa chamar mysql
elasticsearch ou o que seja...
"""
from db_mysql import DbCursor

cursor = DbCursor()

def persist_address(address:str,crypto_currency):

    cursor.persist_on_database(address,crypto_currency) 
    return "Return message of success of not"

def list_addresses()->list:

    addresses = cursor.list_all_addresses()
    return addresses

def retrieve_address_from_id(id:int)->str:

    address = cursor.retrieve_address(id)
    return address