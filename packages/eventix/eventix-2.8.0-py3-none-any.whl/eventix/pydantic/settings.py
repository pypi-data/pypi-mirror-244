import os
from typing import Literal

from pydantic_settings import BaseSettings

BackendNames = Literal["mongodb", "couchdb"]


class EventixSettings(BaseSettings):
    eventix_backend: BackendNames
    eventix_relay_config: str = os.path.abspath(os.path.join(__file__, "../../../relay.yaml"))
