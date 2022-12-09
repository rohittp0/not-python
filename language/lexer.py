from dataclasses import dataclass

from language.constants import TokenType
from language.errors.lexing_error import ExpectedCharacterError, InvalidCharacterError, UnknownTokenError


@dataclass()
class Token:
    text: str
    kind: TokenType

    def __repr__(self):
        return f"Token({self.kind}:{self.text})"

    @classmethod
    def check_if_keyword(cls, tok_text):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tok_text and 100 <= kind.value < 200:
                return kind


class Lexer:
    def __init__(self, source):
        self.source = source + '\n'
        self.curChar = ''
        self.curPos = -1
        self.next_char()

    def next_char(self):
        self.curPos += 1

        if self.curPos < len(self.source):
            self.curChar = self.source[self.curPos]
        else:
            self.curChar = None

    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    def skip_whitespace(self):
        while self.curChar in [' ', '\t', '\r']:
            self.next_char()

    def skip_comment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.next_char()

    def parse_operators(self):
        if self.curChar == '+':
            return Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            return Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            return Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            return Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.next_char()
                return Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                return Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.next_char()
                return Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                return Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Check whether this is token is < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.next_char()
                return Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                return Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.next_char()
                return Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                raise ExpectedCharacterError('!=', self.curChar, self.curPos)

    def parse_literals(self):
        if self.curChar == '\"':
            self.next_char()
            startPos = self.curPos

            while self.curChar != '\"':
                self.next_char()

            tokText = self.source[startPos: self.curPos]  # Get the substring.
            return Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == '.':
                self.next_char()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit():
                    raise ExpectedCharacterError('digit', self.peek(), self.curPos)
                while self.peek().isdigit():
                    self.next_char()

            tokText = self.source[startPos: self.curPos + 1]
            return Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            startPos = self.curPos
            while self.peek().isalnum():
                self.next_char()

            tokText = self.source[startPos: self.curPos + 1]
            keyword = Token.check_if_keyword(tokText)
            if keyword is None:  # Identifier
                return Token(tokText, TokenType.IDENT)
            else:  # Keyword
                return Token(tokText, keyword)

    def parse_special_symbols(self):
        if self.curChar == '\n':
            return Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar is None:
            return Token('', TokenType.EOF)

    def get_token(self) -> Token:
        self.skip_whitespace()
        self.skip_comment()

        token = self.parse_special_symbols() or self.parse_operators() or self.parse_literals()

        if token is None:
            raise UnknownTokenError(self.curChar, self.curPos)

        self.next_char()
        return token
