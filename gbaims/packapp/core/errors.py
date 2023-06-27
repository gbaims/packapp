from typing import Any

# Errors are unexpected / unknown errors that usually represents a bug in code
# Failures are expected errors that could be handled in code flow


class PackappError(Exception):
    message: str

    def __init__(self, **kwargs: Any) -> None:
        self.args = tuple(kwargs.values())
        self.__dict__ = kwargs

    def __str__(self) -> str:
        return self.message.format(**self.__dict__)

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        args = [f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in self.__dict__.items()]
        return f"{cls}({', '.join(args)})"


class InconsistencyError(PackappError):
    message = "{entity} {value} is not consistent at this time"

    def __init__(self, entity: str, value: Any) -> None:
        super().__init__(entity=entity, value=value)


class ValidationError(PackappError):
    message = "{msg}"

    def __init__(self, msg: str) -> None:
        super().__init__(msg=msg)
