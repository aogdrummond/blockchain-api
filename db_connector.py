"""
Manter esse trecho genérico para que possa chamar mysql
elasticsearch ou o que seja...
"""
import os
from dotenv import load_dotenv
from db_mysql import DbCursor
load_dotenv()

cursor = DbCursor(host=os.environ.get("DB_HOST"),
                  user=os.environ.get("DB_USER") ,
                  password=os.environ.get("DB_PASSWORD"),
                  database=os.environ.get("DB_NAME"))

def persist_address_on_db(address:str,crypto_currency):

    cursor.persist_on_database(address,crypto_currency) 
    return "Return message of success of not"

def list_addresses_from_db()->list:

    addresses = cursor.list_all_addresses()
    return addresses

def retrieve_address_from_id(id:int)->str:

    address = cursor.retrieve_address(id)
    return address