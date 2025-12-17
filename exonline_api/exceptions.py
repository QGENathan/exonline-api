class APIError(Exception):
    """Base class for API-related exceptions."""
    pass

class AuthenticationError(APIError):
    """Raised when authentication with the API fails."""
    pass