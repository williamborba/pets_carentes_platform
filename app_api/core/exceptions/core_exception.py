from typing import Optional


class CoreException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message

        super().__init__(self.message)
