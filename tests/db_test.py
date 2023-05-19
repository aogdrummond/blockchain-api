class TestDatabaseTasks:

    def test_persist_on_database(self,db):        
       
        address = "example_address"
        crypto = "BTC"
        db.persist_on_database(address, crypto)
        db.cursor.execute("SELECT address FROM crypto_address WHERE address = %s", (address,))
        result = db.cursor.fetchone()
        assert result[0] == address

    def test_list_all_addresses(self,db):
        addresses = db.list_all_addresses()

        assert isinstance(addresses, list)
        assert len(addresses) > 1

    def test_retrieve_address(self,db):
        address_id = 1
        address = db.retrieve_address(address_id)

        assert isinstance(address, str)
