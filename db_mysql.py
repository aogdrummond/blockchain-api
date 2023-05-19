import os
import tools
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

class DbCursor:

    def __init__(self,host,user,password,database) -> None:

        self.connect(host,user,password,database)

    def connect(self,host,user,password,database):

        self.mydb = mysql.connector.connect(host=host, 
                                        user=user, 
                                        password=password,
                                        database=database)
        self.cursor = self.mydb.cursor()

    def persist_on_database(self,address:str,crypto:str):
        query = "INSERT INTO crypto_address (address, crypto_currency) "
        query += f"VALUES ('{address}','{crypto}')"
        self.cursor.execute(query)
        self.mydb.commit()
        return 
    
    def list_all_addresses(self):

        query = "SELECT address FROM crypto_address "
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        if response:
            return tools.flatten_list(response)
    
    def retrieve_address(self,id:int)->str:

        query = "SELECT address FROM crypto_address "
        query += f"WHERE id = {id}"
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        if response:
            return response[0][0]
    



# """
# CREATE TABLE crypto_address(id INTEGER NOT NULL AUTO_INCREMENT,
# 							address VARCHAR(256) NOT NULL,
# 							crypto_currency VARCHAR(64) NOT NULL,
# 							created_date DATETIME NOT NULL DEFAULT NOW(),
# 							PRIMARY KEY (id)
# """