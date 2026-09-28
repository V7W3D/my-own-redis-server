from dataclasses import dataclass

@dataclass
class SimpleString:
    value: str

@dataclass
class ErrorString:
    value: str

@dataclass
class SimpleInteger:
    value: int
