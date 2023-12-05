class AuthError(Exception):
    """AuthError: Exception for authentication error"""

    pass

class ModelNotFoundError(Exception):
    """ModelNotFoundError: Exception for model not found"""

    pass


class ModelLoadError(Exception):
    """ModelLoadError: Exception for model load error"""

    pass


class ModelGenerateError(Exception):
    """LocalModelGenerateError: Exception for local model generation error"""

    pass