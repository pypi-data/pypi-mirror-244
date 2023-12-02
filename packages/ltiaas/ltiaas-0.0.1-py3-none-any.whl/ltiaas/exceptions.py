class LTIaaSClientError(Exception):
    error: str
   
    def __str__(self) -> str:
        return self.error


class LtikSessionRequired(LTIaaSClientError):
    error = 'The requested endpoint requires an "ltik" session'


class LTIaaSClientAPIError(LTIaaSClientError):
    status_code: int
    details: dict

    def __init__(self, status_code: int, error: str, details: dict):
        super().__init__()
        self.status_code = status_code
        self.error = error
        self.details = details

    def __str__(self) -> str:
        return f'{self.error} ({self.status_code}) - Details: {self.details}'
