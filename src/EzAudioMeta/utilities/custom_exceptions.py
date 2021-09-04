class ExpectedTermination(Exception):
    '''
    Raised when an expected termination is encountered, like, when no
    tags where passed at all.
    '''

    def __init__(self, *args: object) -> None:

        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return str(self.message)
        else:
            return "Expected termination achieved."


class UnexpectedTermination(Exception):
    '''
    Raised when an unexpected termination is encountered, like another
    exception that impedes runtime execution (like a file not found).
    '''

    def __init__(self, *args: object) -> None:

        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:

        if self.message:
            return str(self.message)
        else:
            return "Unexpected temination achieved."
