from typing import Any

from gbaims.packapp.core.errors import PackappError


class BerglerError(PackappError):
    pass


class InvalidOrForbiddenBerglerError(BerglerError):
    message = "Invalid or forbidden method call. Result: {result}"

    def __init__(self, result: Any) -> None:
        super().__init__(result=result)


class ClientBerglerError(BerglerError):
    message = "The request could not be fulfilled By Bergler servers [{code}] {msg}"

    def __init__(self, code: str, msg: str) -> None:
        super().__init__(code=code, msg=msg)


class ServerBerglerError(BerglerError):
    message = "Bergler server failed to handle an apparently valid request [{fault}] {document}"

    def __init__(self, fault: Any, document: Any) -> None:
        super().__init__(fault=fault, document=document)


class UnknownBerglerError(BerglerError):
    message = "An unknown error has ocurred while trying to connect to Bergler. Result: {result}"

    def __init__(self, result: Any) -> None:
        super().__init__(result=result)
