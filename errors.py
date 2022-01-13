"""
All custom errors collected here
"""


class BaseError(Exception):
    message = ""
    name = ""

    def __init__(self, message=None, *args, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    @property
    def error_message(self):
        return self.message.format(**self.kwargs)

    def __str__(self):
        return  "{}:{}".format(self.name or self.__class__.__name__, self.error_message)


class ProductNotFoundInDosator(BaseError):
    message = "Product '{product}' not found in current controller"