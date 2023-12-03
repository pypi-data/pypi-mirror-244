import asyncio
import os
import unittest

from dotenv import load_dotenv

from capsphere.data.db import DbQueryService, DbQueryServiceAsync
from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.connector.postgres.pg_connection import PostgresConnectorAsync

load_dotenv()

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@unittest.skip("just testing connection")
class TestExecutor(unittest.TestCase):
    connector = PostgresConnector()

    def test_postgres_executor(self):
        executor_service = DbQueryService(self.connector)
        data = executor_service.execute("SELECT * FROM test_table")

    def test_mysql_executor(self):
        pass


class TestConnectionAsync(unittest.IsolatedAsyncioTestCase):
    async def test_postgres_executor_async(self):
        connector_async = PostgresConnectorAsync()
        executor_service = DbQueryServiceAsync(connector_async)
        async with connector_async.get_connection_async():
            data = await executor_service.execute_async("SELECT * FROM test_table")



