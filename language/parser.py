from language.constants import TokenType, COMPARISON_TOKENS
from language.emitter import Emitter
from language.errors.parseing_error import ExpectedTokenError, InvalidTokenError, UndefinedVariableError
from language.lexer import Lexer, Token


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def type(self):
        return type(self.value)


class Parser:
    def __init__(self, lexer: Lexer, emitter: Emitter):
        self.lexer: Lexer = lexer
        self.emitter: Emitter = emitter

        self.cur_token: Token = lexer.get_token()
        self.peek_token: Token = lexer.get_token()

        self.symbols = set()

    def check_token(self, kind):
        return kind == self.cur_token.kind

    # Return true if the next token matches.
    def check_peek(self, kind):
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            raise ExpectedTokenError(kind, self.cur_token)
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def nl(self, throw=True):
        if throw:
            self.match(TokenType.NEWLINE)

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def primary(self):
        if self.check_token(TokenType.NUMBER):
            self.emitter.emit(self.cur_token.text)
            self.next_token()

        elif self.check_token(TokenType.IDENT):
            if self.cur_token.text not in self.symbols:
                raise UndefinedVariableError(self.cur_token.text)

            self.emitter.emit(self.cur_token.text)
            self.next_token()
        else:
            raise InvalidTokenError(self.cur_token)

    def unary(self):
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
        self.primary()

    def term(self):
        if self.check_peek(TokenType.MODULO):
            self.emitter.emit("(int)")

        self.unary()

        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH) or \
                self.check_token(TokenType.MODULO):
            self.emitter.emit(self.cur_token.text)

            if self.check_token(TokenType.MODULO):
                self.emitter.emit("(int)")

            self.next_token()
            self.unary()

    def expression(self):
        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.term()

    def comparison(self):
        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.cur_token.kind in COMPARISON_TOKENS:
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()
        else:
            raise ExpectedTokenError("comparison operator", self.cur_token)

        # Can have 0 or more comparison operator and expressions.
        while self.cur_token.kind in COMPARISON_TOKENS:
            self.emitter.emit(self.cur_token.text)
            self.next_token()
            self.expression()

    def control_statement(self, keyword):
        self.next_token()

        self.emitter.emit(f"{keyword}(")
        self.comparison()

        self.nl(throw=False)

        self.match(TokenType.LBRACE)
        self.emitter.emit_line("){")

        self.nl(throw=False)

        # Zero or more statements in the loop body.
        while not self.check_token(TokenType.RBRACE):
            self.statement()

        self.match(TokenType.RBRACE)
        self.emitter.emit_line("}")

    def statement(self):
        if self.check_token(TokenType.PRINT):
            self.next_token()
            self.emitter.emit(f"std::cout")

            while not self.check_token(TokenType.NEWLINE):
                if self.check_token(TokenType.STRING):
                    self.emitter.emit(f"<<\"{self.cur_token.text}\"")
                    self.next_token()
                else:
                    self.emitter.emit("<<")
                    self.expression()

            self.emitter.emit_line(";")

        elif self.check_token(TokenType.IF):
            self.control_statement("if")
            self.nl(throw=False)

            if self.check_token(TokenType.ELSE):
                self.next_token()
                self.emitter.emit("else ")

                if self.check_token(TokenType.IF):
                    return self.statement()
                else:
                    self.nl(throw=False)

                    self.match(TokenType.LBRACE)
                    self.emitter.emit_line("{")

                    self.nl(throw=False)

                    while not self.check_token(TokenType.RBRACE):
                        self.statement()

                    self.match(TokenType.RBRACE)
                    self.emitter.emit_line("}")
            else:
                return

        elif self.check_token(TokenType.WHILE):
            self.control_statement("while")

        elif self.check_token(TokenType.LET):
            self.next_token()

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line("float " + self.cur_token.text + ";")

            self.emitter.emit(self.cur_token.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.expression()
            self.emitter.emit_line(";")

        elif self.check_token(TokenType.INPUT):
            self.next_token()
            self.emitter.emit("std::cin")

            while not self.check_token(TokenType.NEWLINE):
                if self.cur_token.text not in self.symbols:
                    self.symbols.add(self.cur_token.text)
                    self.emitter.header_line("float " + self.cur_token.text + ";")

                self.emitter.emit(f">>{self.cur_token.text}")
                self.match(TokenType.IDENT)

            self.emitter.emit_line(";")
        elif self.check_token(TokenType.RETURN):
            self.next_token()
            self.emitter.emit("return ")
            self.expression()
            self.emitter.emit_line(";")
        else:
            raise InvalidTokenError(self.cur_token)
        # Newline.
        self.nl()

    def program(self):
        self.emitter.header_line("#include <iostream>")
        self.emitter.header_line("int main(int argc, char *argv[]){")

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

        self.emitter.write_file()
