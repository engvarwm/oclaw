class OpenClawAdapterError(Exception):
    def __init__(self, error: str, message: str, status_code: int = 200):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class OpenClawUnavailableError(OpenClawAdapterError):
    def __init__(self, message: str, error: str = "openclaw_unavailable"):
        super().__init__(error=error, message=message)


class BadOpenClawResponseError(OpenClawAdapterError):
    def __init__(self, message: str, error: str = "bad_openclaw_response"):
        super().__init__(error=error, message=message)


class UnauthorizedError(OpenClawAdapterError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(error="unauthorized", message=message, status_code=401)
