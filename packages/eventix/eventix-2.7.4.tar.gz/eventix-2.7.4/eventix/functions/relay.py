from lsrestclient import LsRestClient

from eventix.exceptions import backend_exceptions
from eventix.functions.errors import raise_errors
from eventix.pydantic.relay import RelayModel
from eventix.pydantic.task import TaskModel


class RelayManager(object):
    relays: dict =  {}

    @classmethod
    def add_relay(cls, relay: RelayModel):
        cls.relays[relay.namespace] = relay

    @classmethod
    def try_relay(cls, task: TaskModel) -> TaskModel | None:
        relay = cls.relays.get(task.namespace, None)
        if relay is None:
            return None
        else:
            client = LsRestClient(relay.url, name=f"relay-{relay.namespace}")
            r = client.post('/task', body=task.model_dump())
            with raise_errors(r, backend_exceptions):
                return TaskModel.model_validate_json(r.content)
