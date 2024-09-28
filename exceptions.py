class InputException(BaseException):
    def __init__(self, message:str) -> None:
        self.message = message
        super().__init__(message)

class InsertException(BaseException):
    def __init__(self, message:str) -> None:
        self.message = message
        super().__init__(message)

class ColumnException(BaseException):
    def __init__(self, message:str) -> None:
        self.message = message
        super().__init__(message)

