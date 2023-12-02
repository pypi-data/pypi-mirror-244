import pytest
from async_pyarrow.flight import connect as async_connect
import pyarrow as pa
from pyarrow import flight
import pandas as pd


class ExampleServer(flight.FlightServerBase):
    def do_get(self, context, ticket):
        data = [{'column1': 1, 'column2': 1.1},
                {'column1': 2, 'column2': 2.2},
                {'column1': 3, 'column2': 3.3}]
        table = pa.Table.from_pandas(pd.DataFrame(data))
        return flight.RecordBatchStream(table)


@pytest.fixture
def flight_server():
   with ExampleServer() as server:
        yield server

@pytest.mark.asyncio
async def test_async_flight_client(flight_server):
    # Use the client and server in the same test
    client = async_connect(f'localhost:{flight_server.port}')
    get_call = client.do_get(flight.Ticket(ticket=b"test"))
    table = await get_call.read_all()
    assert table.num_rows == 3
    assert table.num_columns == 2
