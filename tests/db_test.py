from db_mysql import DbCursor


class TestDatabaseTasks:
    def test_persist_on_database(self, db: DbCursor) -> None:
        """
        Test the `persist_on_database` method of DbCursor.

        Args:
            db (DbCursor): DbCursor instance.

        Returns:
            None
        """
        address = "example_address"
        crypto = "BTC"
        db.persist_on_database(address, crypto)
        db.cursor.execute(
            "SELECT address FROM crypto_address WHERE address = %s", (address,)
        )
        result = db.cursor.fetchone()
        assert result[0] == address

    def test_list_all_addresses(self, db: DbCursor) -> None:
        """
        Test the `list_all_addresses` method of DbCursor.

        Args:
            db (DbCursor): DbCursor instance.

        Returns:
            None
        """
        addresses = db.list_all_addresses()

        assert isinstance(addresses, list)
        assert len(addresses) > 1

    def test_retrieve_address(self, db: DbCursor) -> None:
        """
        Test the `retrieve_address` method of DbCursor.

        Args:
            db (DbCursor): DbCursor instance.

        Returns:
            None
        """
        address_id = 1
        address = db.retrieve_address(address_id)

        assert isinstance(address, str)