from message_types import SimpleString, ErrorString
from message_types import SimpleInteger
from message_types import RespArray
from exceptions import RespProtocolError
from typing import Optional

def simple_parse_resp(message: str, index: int) -> tuple[str, int]:
    i = index
    parsed_text = ""
    while i < len(message):
        if message[i] == '\r' and i < len(message)-1:
            if message[i+1] == '\n':
                return (parsed_text, i+2)
        else:
            parsed_text += message[i]
            i += 1
    return (parsed_text, i)

def bulk_string_parse_resp(message: str, index: int) -> tuple[SimpleString, int]:
    i = index
    string_length_str, i = simple_parse_resp(message, i)
    try:
        string_length = int(string_length_str)
    except ValueError as exc:
        raise RespProtocolError(f"Invalid array length: {string_length_str!r}") from exc
    
    string_text, i = simple_parse_resp(message, i)
    if len(string_text) <= string_length:
        return (SimpleString(string_text), i)
    else:
        raise RespProtocolError("Bulk string is longer than its defined length.")

def parser_resp(message: str, i: int, *, array_length: Optional[int] = None) -> list[any]:
    if len(message) < 0:
        raise ValueError("Message to parse with RESP is empty.")
    
    result = []
    while i < len(message):
        if array_length is not None and len(result) == array_length:
            break

        match message[i]:
            case "+":
                parsed, i = simple_parse_resp(message, i+1)
                result.append(SimpleString(parsed))
            case "-":
                parsed, i = simple_parse_resp(message, i+1)
                result.append(ErrorString(parsed))
            case ":":
                parsed, i = simple_parse_resp(message, i+1)
                result.append(SimpleInteger(parsed))
            case "$":
                parsed, i = bulk_string_parse_resp(message, i+1)
                result.append(parsed)
            case "*":
                array_length_str, i = simple_parse_resp(message, i+1)
                try:
                    array_length = int(array_length_str)
                except ValueError as exc:
                    raise RespProtocolError(f"Invalid array length: {array_length_str!r}") from exc

                parsed_array, i = parser_resp(message, i, array_length=array_length)
                result.append(RespArray(parsed_array)) 
            case _:
                pass
        i += 1
    return result, i