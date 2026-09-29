from dataclasses import dataclass
from message_types import SimpleString, SimpleInteger

@dataclass
class RespArray:
    value: list[SimpleString | SimpleInteger]