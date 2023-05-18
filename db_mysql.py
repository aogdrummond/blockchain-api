import os
import tools
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

mydb = mysql.connector.connect(host=os.environ.get("DB_HOST"), 
                               user=os.environ.get("DB_USER"), 
                               password=os.environ.get("DB_PASSWORD"),
                               database=os.environ.get("DB_NAME"))
cursor = mydb.cursor()

class DbCursor:

    def __init__(self) -> None:

        self.cursor = cursor

    def persist_on_database(self,address:str,crypto:str):
        query = "INSERT INTO crypto_address (address, crypto_currency) "
        query += f"VALUES ('{address}','{crypto}')"
        self.cursor.execute(query)
        mydb.commit()
        return 
    
    def list_all_addresses(self):

        query = "SELECT address FROM crypto_address "
        self.cursor.execute(query)
        response = cursor.fetchall()
        if response:
            return tools.flatten_list(response)
    
    def retrieve_address(self,id:int)->str:

        query = "SELECT address FROM crypto_address "
        query += f"WHERE id = {id}"
        self.cursor.execute(query)
        response = cursor.fetchall()
        if response:
            return response[0][0]
    



# """
# CREATE TABLE crypto_address(id INTEGER NOT NULL AUTO_INCREMENT,
# 							address VARCHAR(256) NOT NULL,
# 							crypto_currency VARCHAR(64) NOT NULL,
# 							created_date DATETIME NOT NULL DEFAULT NOW(),
# 							PRIMARY KEY (id)
# """