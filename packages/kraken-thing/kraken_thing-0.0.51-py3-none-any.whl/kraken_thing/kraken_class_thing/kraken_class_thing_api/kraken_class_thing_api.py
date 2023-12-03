
"""
Class ot interact with api
"""
import json
from kraken_thing.kraken_class_thing.kraken_class_thing_api import kraken_class_thing_api_methods as m
from kraken_thing import kraken_thing_methods as kr
import os

class Thing_api:

    def __init__(self, thing):

        self._thing = thing
        self._api_url = None

    @property
    def url(self):
        self._api_url = self._api_url if self._api_url else os.environ.get("API_URL")
        return self._api_url

    @url.setter
    def url(self, value):
        os.environ["API_URL"] = value
        self._api_url = value

    def get(self):
        """Retrieve record
        """
        content = m.get(self.url, self._thing.type, self._thing.id)
        record = kr.json.loads(content)
        return self._thing._db_load(record)

    def post(self):
        """Post record
        """
        record = self._thing._db_dump()
        content = kr.json.dumps(record)
        return m.post(self.url, content)
        
    def delete(self):
        """Retrieve record
        """
        return m.delete(self.url, self._thing.type, self._thing.id)

    async def get_async(self):
        """Retrieve record
        """
        content = await m.get_async(self.url, self._thing.type, self._thing.id)
        record = kr.json.loads(content)
        return self._thing._db_load(record)

    async def post_async(self):
        """Post record
        """
        record = self._thing._db_dump()
        content = kr.json.dumps(record)
        return await m.post_Async(self.url, content)
    
    async def delete_async(self):
        """Retrieve record
        """
        return await m.delete_async(self.url, self._thing.type, self._thing.id)
    