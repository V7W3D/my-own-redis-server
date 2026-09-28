from message_types import SimpleString, ErrorString
from message_types import SimpleInteger

def simple_parse_resp(message: str, index: int) -> tuple[str, int]:
    i = index
    result = ""
    while i < len(message):
        if message[i] == '\r' and i < len(message)-1:
            if message[i+1] == '\n':
                return (result, i+2)
        else:
            result += message[i]
            i += 1
    return result

def parser_resp(message: str) -> list[any]:
    if len(message) < 0:
        raise ValueError("Message to be RESP parsed is empty.")

    i = 0
    result = []
    while i < len(message):
        match message[i]:
            case "+":
                parsed_text, i = simple_parse_resp(message, i+1)
                result.append(SimpleString(parsed_text))
            case "-":
                parsed_text, i = simple_parse_resp(message, i+1)
                result.append(ErrorString(parsed_text))
            case ":":
                parsed_text, i = simple_parse_resp(message, i+1)
                result.append(SimpleInteger(parsed_text))
            case "$":
                pass
            case "*":
                pass
            case _:
                pass
        i += 1
    return result