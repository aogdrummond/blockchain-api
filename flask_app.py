import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from db_connector import persist_address, list_addresses, retrieve_address_from_id
from cryptography import generate_address_to_crypto

load_dotenv()
app = Flask(__name__)

@app.route("/")
def hello_world() -> str:
    """
    Hello World route.

    Returns:
        str: A greeting message.
    """
    return "Hello, World!"

@app.route("/api/generate", methods=["POST"])
def generate_address() -> str:
    """
    Generates an address for the given cryptocurrency.

    Request Body:
        crypto_currency (str): The cryptocurrency symbol.

    Returns:
        str: The generated address.
    """
    data = request.get_json()
    crypto_currency = data.get("crypto_currency")
    if crypto_currency:
        address = generate_address_to_crypto(crypto_currency)
        persist_address(address, crypto_currency)
        return jsonify({"address": address}), 201
    else:
        return jsonify({"error": "Missing crypto_currency parameter"}), 400

@app.route("/api/list", methods=["GET"])
def list_address() -> str:
    """
    Lists all addresses.

    Returns:
        str: The list of addresses.
    """
    addresses = list_addresses()
    return jsonify({"addresses": addresses})

@app.route("/api/addresses/<address_id>", methods=["GET"])
def retrieve_address(address_id: str) -> str:
    """
    Retrieves the address for the given address ID.

    Args:
        address_id (str): The address ID.

    Returns:
        str: The retrieved address.
    """
    address = retrieve_address_from_id(address_id)
    if address:
        return jsonify({"address": address})
    else:
        return jsonify({"error": "Address not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("API_PORT"))
    host = os.environ.get("API_HOST")
    app.run(host=host, port=port)
