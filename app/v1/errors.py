"""
All custom errors collected here
"""


class BaseError(Exception):
    """
    Base class for custom errors. Every error should be inherited from here.
    """

    message = ""
    name = ""

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    @property
    def error_message(self):
        return self.message.format(**self.kwargs)

    def __str__(self):
        return f"{self.name or self.__class__.__name__}:{self.error_message}"


class ProductNotFound(BaseError):
    """
    Exceptional. it shouldn't happen.
    """

    message = "Product '{product}' not found."


class ProductNotFoundInDosator(BaseError):
    """
    Exceptional. it shouldn't happen.
    """

    message = "Product '{product}' not found in current controller"


class ErrorReceiptConfiguration(BaseError):
    """
    Exceptional. it shouldn't happen.
    """

    message = "Error receipt configuration. Details: {details}"


class NotReadyForCooking(BaseError):
    """
    Exceptional. it shouldn't happen.
    """

    message = "Device not ready for cooking. Details: {details}"
