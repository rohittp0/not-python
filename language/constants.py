import enum


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    RETURN = 101
    ELSE = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    WHILE = 108
    NEW = 109
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    MODULO = 212
    EXP = 213
    # Brackets.
    LPAREN = 301
    RPAREN = 302
    LBRACE = 303
    RBRACE = 304
    LBRACKET = 305
    RBRACKET = 306


COMPARISON_TOKENS = [
    TokenType.EQEQ, TokenType.NOTEQ, TokenType.LT, TokenType.LTEQ, TokenType.GT, TokenType.GTEQ
]