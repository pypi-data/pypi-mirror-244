from .message import ErrorMessage


class PAIGException(Exception):
    """
    Base class for all PAIG exceptions.
    """

    def __init__(self, message, **kwargs):
        """
        Initialize a PAIGException instance.

        Args:
            message (str): The error message.
        """
        super().__init__(PAIGException.format_message(message, **kwargs))

    @staticmethod
    def format_message(template, **kwargs):
        return template.format(**kwargs)


class AccessControlException(PAIGException):
    """
    Custom exception for access control violations.
    """
    def __init__(self, error_message: str):
        super().__init__(ErrorMessage.PAIG_ACCESS_DENIED.format(error_message=error_message))
