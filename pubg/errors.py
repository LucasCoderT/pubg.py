class BadArgument(Exception):
    """
    Exception raised when passing invalid search parameters
    """
    def __init__(self, argument):
        super().__init__("{0} is not a valid argument".format(argument))


class BaseException(Exception):
    """
    Exception raised when the api returns anything abnormal
    """
    def __init__(self, response):
        self.code = response['code']
        self.error = response['error']
        super().__init__(self.error)
