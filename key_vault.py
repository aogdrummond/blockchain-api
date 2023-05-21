import os
import boto3
import json
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


def recover_from_s3() -> str:
    """
    Recovers the private key from the S3 bucket.

    Returns:
        str: The recovered private key if successful, otherwise None.
    """
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY
    )

    object_key = "keys/private_key.json"

    try:
        response = session.client("s3").get_object(Bucket=BUCKET_NAME, Key=object_key)
    except ClientError as error:
        logger.warning(error)
        return {}

    metadata = response["ResponseMetadata"]
    if metadata["HTTPStatusCode"] == 200:
        keys = response["Body"].read().decode("utf-8")
        logger.warning("Private key recovered.")
        return json.loads(keys)
    else:
        return None


def persist_on_s3(key: str, crypto_currency: str) -> None:
    """
    Persists the private key on the S3 bucket.

    Args:
        key (str): The private key to persist.
        crypto_currency (str): The cryptocurrency associated with the key.
    """
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY
    )
    object_key = "keys/private_key.json"

    try:
        response = session.client("s3").get_object(Bucket=BUCKET_NAME, Key=object_key)
        keys = (
            json.loads(response["Body"].read().decode("utf-8"))
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200
            else {}
        )
    except:
        keys = {}

    if keys.get(crypto_currency):
        return None
    else:
        keys[crypto_currency] = key

    response = session.client("s3").put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=json.dumps(keys),
        ContentType="application/json",
        Expires=datetime.now() + timedelta(days=1),
    )

    metadata = response["ResponseMetadata"]
    if metadata["HTTPStatusCode"] == 200:
        logger.info("Key saved successfully.")
    else:
        logger.warning("There was an error while persisting.")