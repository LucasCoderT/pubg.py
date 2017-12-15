class BadArgument(Exception):
    def __init__(self, argument):
        super().__init__("{0} is not a valid argument".format(argument))
