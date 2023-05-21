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
    key_parser = KeyManager(crypto_symbol)
    encrypter = CurrenciesEncrypter()
    return encrypter.generate_address(crypto_symbol, key_parser.private_key)


def persist_address(address: str, crypto_currency: str) -> None:
    """
    Persists the address and corresponding cryptocurrency in the database.

    Args:
        address (str): The address to persist.
        crypto_currency (str): The cryptocurrency associated with the address.

    Returns:
        None
    """
    db_connector.persist_address_on_db(address, crypto_currency)


def list_addresses() -> list:
    """
    Retrieves a list of all addresses stored in the database.

    Returns:
        list: A list of addresses.
    """
    return db_connector.list_addresses_from_db()


def retrieve_address(id: int) -> str:
    """
    Retrieves the address from the database based on the given ID.

    Args:
        id (int): The ID of the address in the database.

    Returns:
        str: The retrieved address.
    """
    address = db_connector.retrieve_address_from_id(id)
    return address