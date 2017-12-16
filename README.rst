pubg.py
=======

.. image:: https://img.shields.io/pypi/v/pubg.py.svg
   :target: https://pypi.python.org/pypi/pubg.py
.. image:: https://readthedocs.org/projects/pubgpy/badge/?version=latest
   :target: https://readthedocs.org/projects/pubgpy/badge/?version=latest


wrapper for https://pubgtracker.com/site-api api using aiohttp


Installing
----------

.. code:: sh

    python3 -m pip install pubg.py


or you can install from github via

.. code:: sh

    $python3 -m pip install git+https://github.com/datmellow/pubg.py


Quick Example
-------------

.. code:: py

    import pubg
    import asyncio



    async def myfunc():
        client = pubg.PubGClient("token")
        user_data = await client.get_user("NickName")
        user_match_history = await client.get_match_history(user_data)
        return user_data,user_match_history


    if __name__ == '__main__':
        asyncio.get_event_loop().run_until_complete(myfunc())

Note that in Python 3.4 you use ``@asyncio.coroutine`` instead of ``async def`` and ``yield from`` instead of ``await``.


Requirements
------------

* Python 3.4.2+
* ``aiohttp`` library

Usually pip will install aiohttp with the library