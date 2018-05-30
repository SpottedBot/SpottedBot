from spotteds.facebook_page_tools import page_graph
import json


class BaseMessage:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.data = list(kwargs.keys())

    def payload(self, **kwargs):
        payload = {}
        for key, value in kwargs.items():
            payload[key] = json.dumps(value)
        for key in self.data:
            payload[key] = json.dumps(getattr(self, key)) if not isinstance(getattr(self, key), str) else getattr(self, key)
        return payload

    def send(self, endpoint, connection, **kwargs):
        page_graph().put_object(endpoint, connection, **self.payload(**kwargs))

    async def asend(self, endpoint, connection, **kwargs):
        await self.send(endpoint, connection, **kwargs)
