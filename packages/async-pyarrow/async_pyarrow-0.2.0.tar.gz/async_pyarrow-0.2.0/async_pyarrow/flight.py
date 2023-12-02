import grpc
import pyarrow as pa
import struct
from .Flight_pb2_grpc import FlightServiceStub
from .Flight_pb2 import Ticket


class AsyncGetCall():
    def __init__(self, call):
        self.call = call

    async def read_all(self):
        schema = None
        batches = []

        # Ensure self.client.do_get returns an asynchronous iterator
        async for data in self.call:
            token = b'\xff\xff\xff\xff'
            # 4 bytes: message length (little-endian)
            length = struct.pack('<I', len(data.data_header))
            buf = pa.py_buffer(token + length + data.data_header + data.data_body)
            message = pa.ipc.read_message(buf)
            if schema is None:  # first read schema
                schema = pa.ipc.read_schema(buf)
            else:  # then read all the record batches
                batch = pa.ipc.read_record_batch(message, schema)
                batches.append(batch)

        table = pa.Table.from_batches(batches, schema=schema)

        return table


class AsyncFlightClient():
    def __init__(self, stub):
        self.stub = stub

    def do_get(self, ticket) -> AsyncGetCall:
        # Use StreamStreamCall for bidirectional streaming
        call = self.stub.DoGet(Ticket(ticket=ticket.ticket))
        return AsyncGetCall(call)


async def connect(connection_str) -> AsyncFlightClient:
    channel = grpc.aio.insecure_channel(connection_str)
    stub = FlightServiceStub(channel)
    return AsyncFlightClient(stub)
