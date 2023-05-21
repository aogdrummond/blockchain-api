import mysql.connector
from typing import List
from dotenv import load_dotenv

load_dotenv()


class DbCursor:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        """
        Initializes a DbCursor object.

        Args:
            host (str): The host of the database.
            user (str): The username for database authentication.
            password (str): The password for database authentication.
            database (str): The name of the database.
        """
        self.connect(host, user, password, database)

    def connect(self, host: str, user: str, password: str, database: str) -> None:
        """
        Connects to the database.

        Args:
            host (str): The host of the database.
            user (str): The username for database authentication.
            password (str): The password for database authentication.
            database (str): The name of the database.
        """
        self.mydb = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.mydb.cursor()

    def persist_on_database(self, address: str, crypto: str) -> None:
        """
        Persists an address and cryptocurrency in the database.

        Args:
            address (str): The address to persist.
            crypto (str): The cryptocurrency associated with the address.
        """
        query = "INSERT INTO crypto_address (address, crypto_currency) "
        query += f"VALUES ('{address}','{crypto}')"
        self.cursor.execute(query)
        self.mydb.commit()

    def list_all_addresses(self) -> List[str]:
        """
        Lists all addresses from the database.

        Returns:
            List[str]: A list of addresses stored in the database.
        """
        query = "SELECT address FROM crypto_address "
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        if response:
            return flatten_list(response)

    def retrieve_address(self, id: int) -> str:
        """
        Retrieves an address from the database based on the given ID.

        Args:
            id (int): The ID of the address.

        Returns:
            str: The retrieved address.
        """
        query = "SELECT address FROM crypto_address "
        query += f"WHERE id = {id}"
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        if response:
            return response[0][0]


def flatten_list(original_list: List[List]) -> List:
    """
    Flatten a list of lists by extracting the first element from each sublist.

    Args:
        original_list (List[List]): The original list of lists.

    Returns:
        List: The flattened list containing the first element from each sublist.
    """
    flat_list = []
    for element in original_list:
        flat_list.append(element[0])

    return flat_list
