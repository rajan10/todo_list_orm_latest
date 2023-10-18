# Throw Early, Catch Late
class NoUserInDatabase(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthenticationFailed(Exception):
    def __init__(self, message):
        super().__init__(message)


class HomePageException(Exception):
    def __init__(self, message):
        super().__init__(message)
