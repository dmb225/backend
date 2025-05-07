from typing import Any, Optional


class ResponseTypes:
    PARAMETERS_ERROR = "ParametersError"
    RESOURCE_ERROR = "ResourceError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"


class ResponseFailure:
    def __init__(self, type_: str, message: str | Exception) -> None:
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg: str | Exception) -> str:
        if isinstance(msg, Exception):
            return f"{msg.__class__.__name__}: {msg}"
        return msg

    @property
    def value(self) -> dict[str, str]:
        return {"type": self.type, "message": self.message}

    def __bool__(self) -> bool:
        return False


class ResponseSuccess:
    def __init__(self, value: Optional[list[Any]] = None):
        self.type = ResponseTypes.SUCCESS
        self.value = value

    def __bool__(self) -> bool:
        return True


def build_response_from_invalid_request(invalid_request: Any) -> ResponseFailure:
    message = "\n".join([f"{err['parameter']}: {err['message']}" for err in invalid_request.errors])
    return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, message)
