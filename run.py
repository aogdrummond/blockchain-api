import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from db_connector import persist_address, list_addresses, retrieve_address_from_id
from cryptography import generate_address_to_crypto
from flask_restx import Api, Resource

load_dotenv()
app = Flask(__name__)
api = Api(app, title = "Blockchain API", version="1.0",prefix="/api-blockchain")
api.namespace="Teste"

@api.route("/")
class HelloWorld(Resource):
    def get(self):
        """
        Hello World route.

        Returns:
            str: A greeting message.
        """
        return "Hello, World!"


@api.route("/generate")
class GenerateAddress(Resource):
    def post(self):
        """
        Generates an address for the given cryptocurrency, accordig to the proper method
        applied in each case.

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
            return {"address": address}, 201
        else:
            return {"error": "Missing crypto_currency parameter"}, 400


@api.route("/list")
class ListAddresses(Resource):
    def get(self):
        """
        Lists all addresses currently stored in the database.

        Returns:
            str: The list of addresses.
        """
        addresses = list_addresses()
        return jsonify({"addresses": addresses})


@api.route("/addresses/<address_id>")
class RetrieveAddress(Resource):
    def get(self, address_id):
        """
        Retrieves the address stored in the database with the given address ID
        in the dB.

        Args:
            address_id (str): The address ID.

        Returns:
            str: The retrieved address.
        """
        
        address = retrieve_address_from_id(address_id)
        if address:
            return {"address": address}
        else:
            print("teste")
            return {"error": "Address not found"}, 404


if __name__ == "__main__":
    port = int(os.environ.get("API_PORT"))
    app.run(port=port, debug=True)