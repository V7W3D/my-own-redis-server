from message_types import SimpleString, ErrorString
from message_types import SimpleInteger
from exceptions import RespProtocolError

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
    string_length, i = simple_parse_resp(message, i)
    string_length = int(string_length)
    string_text, i = simple_parse_resp(message, i)
    if len(string_text) <= string_length:
        return (SimpleString(string_text), i)
    else:
        raise RespProtocolError("Bulk string is longer than its defined length.")

def parser_resp(message: str) -> list[any]:
    if len(message) < 0:
        raise ValueError("Message to parse with RESP is empty.")
    
    i = 0
    result = []
    while i < len(message):
        match message[i]:
            case "+":
                parsed_result, i = simple_parse_resp(message, i+1)
                result.append(SimpleString(parsed_result))
            case "-":
                parsed_result, i = simple_parse_resp(message, i+1)
                result.append(ErrorString(parsed_result))
            case ":":
                parsed_result, i = simple_parse_resp(message, i+1)
                result.append(SimpleInteger(parsed_result))
            case "$":
                parsed_result, i = bulk_string_parse_resp(message, i+1)
                result.append(parsed_result)
            case "*":
                pass
            case _:
                pass
        i += 1
    return result