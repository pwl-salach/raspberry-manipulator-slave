from typing import Protocol


class Performer(Protocol):

    def update(self, **kwargs) -> None:
        ...

    def configure(self, **kwargs) -> None:
        ...
