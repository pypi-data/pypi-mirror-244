# Simple Arrow Flight Asyncio Client 

currently, [pyarrow](https://arrow.apache.org/docs/python/index.html) package only supports sync api, at least in terms of `do_get`. In order to use pyarrow flight in an asyncio application, we will have to use the `concurrent.futures.ThreadPoolExecutor`. 

`async_pyarrow` adds asyncio support for `do_get`.

```python
    from async_pyarrow.flight import connect as async_connect
    client = async_connect(f'localhost:50051')
    get_call = client.do_get(flight.Ticket(ticket=b"test"))
    table = await get_call.read_all()
```


caveat: the code assumes the format of the arrow flight tables, hence will break if the format ever changes. 

## install 

```cmd
pip install async_pyarrow
```