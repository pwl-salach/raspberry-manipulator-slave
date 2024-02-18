from typing import Protocol


class ControlsHandler(Protocol):
    
    def listen_for_input(self) -> None: ...
    
    def handle_input(self, control: str) -> None: ...
