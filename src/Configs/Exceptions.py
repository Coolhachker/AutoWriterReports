class InvalidAuthToken(Exception):
    def __init__(self, message):
        super(InvalidAuthToken, self).__init__(message)


class AuthError(Exception):
    def __init__(self, message):
        super(AuthError, self).__init__(message)
