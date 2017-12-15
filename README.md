

wrapper for https://pubgtracker.com/site-api api using aiohttp

``Requires python 3.4.2+``
```Requires aiohttp```



```python
import pubg
import asyncio


@asyncio.coroutine
def myfunc():
    client = pubg.PubGClient("token")
    user_data = yield from client.get_user("NickName")
    user_match_history = yield from client.get_match_history(user_data)
    return user_data,user_match_history


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(myfunc())
```