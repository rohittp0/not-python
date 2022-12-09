class InvalidTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"Invalid token '{self.token}'"


class ExpectedTokenError(Exception):
    def __init__(self, expected_token, token):
        self.expected_token = expected_token
        self.__cause__ = InvalidTokenError(token)

    def __str__(self):
        return f"{self.__cause__}\nExpected '{self.expected_token}'"


class UndefinedVariableError(Exception):
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return f"Undefined variable '{self.variable}'"
