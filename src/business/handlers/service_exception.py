class ServiceException(Exception):
    def __init__(self, message, error_code: int) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.error_message= message