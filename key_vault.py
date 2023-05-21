import os
import logging
from db_mysql import DbCursor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cursor = DbCursor(host=os.environ.get("DB_HOST"),
                  user=os.environ.get("DB_USER") ,
                  password=os.environ.get("DB_PASSWORD"),
                  database=os.environ.get("DB_NAME"))

def recover_from_s3():
    
    return cursor.retrieve_private_key()

def persist_on_s3(private_key):
    
    cursor.persist_private_key(private_key)

