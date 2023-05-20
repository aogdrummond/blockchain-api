import db_connector
from cryptography import KeyManager, CurrenciesEncrypter

def generate_address_to_crypto(crypto_symbol: str) -> str:
    """
    Generates an address for the given cryptocurrency symbol.

    Args:
        crypto_symbol (str): The cryptocurrency symbol.

    Returns:
        str: The generated address for the given cryptocurrency.
    """
    crypto_symbol = crypto_symbol.upper()
    key_parser = KeyManager()
    encrypter = CurrenciesEncrypter()
    return encrypter.generate_address(crypto_symbol, key_parser.private_key)

def persist_address(address:str,crypto_currency):
    """
    Gerar
    """
    db_connector.persist_address_on_db(address,crypto_currency)


def list_addresses():
    """
    Gerar
    """
    return db_connector.list_addresses_from_db()
    
def retrieve_address(id:int):
    """
    Gerar
    """
    address = db_connector.retrieve_address_from_id(id)
    return address