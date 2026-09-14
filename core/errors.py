class ApplicationError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class ValidationFailure(ApplicationError):
    def __bool__(self):
        return False
