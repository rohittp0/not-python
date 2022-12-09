class InvalidCharacterError(Exception):
    def __init__(self, character, position):
        self.character = character
        self.position = position

    def __str__(self):
        return f"Invalid charector '{self.character}' at position {self.position}"


class ExpectedCharacterError(Exception):
    def __init__(self, expected_character, character, position):
        self.expected_character = expected_character
        self.position = position
        self.__cause__ = InvalidCharacterError(character, position)

    def __str__(self):
        return f"{self.__cause__}\nExpected '{self.expected_character}'"


class UnknownTokenError(Exception):
    def __init__(self, token, position):
        self.token = token
        self.position = position

    def __str__(self):
        return f"Unknown token '{self.token}' at position {self.position}"
