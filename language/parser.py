from language.constants import TokenType, COMPARISON_TOKENS
from language.emitter import Emitter
from language.errors.parseing_error import ExpectedTokenError, InvalidTokenError, UndefinedVariableError
from language.lexer import Lexer, Token


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

    def nl(self):
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
        self.unary()
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.emitter.emit(self.cur_token.text)
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

    def statement(self):
        if self.check_token(TokenType.PRINT):
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.emitter.emit_line(f"printf(\"{self.cur_token.text}\");")
                self.next_token()
            else:
                self.emitter.emit("printf(\"%f\", (float)(")
                self.expression()
                self.emitter.emit_line("));")

        elif self.check_token(TokenType.IF):
            self.next_token()

            self.emitter.emit("if(")
            self.comparison()

            self.nl()
            self.emitter.emit_line("){")

            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emit_line("}")

        elif self.check_token(TokenType.WHILE):
            self.next_token()

            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.emitter.emit_line("){")

            self.nl()

            # Zero or more statements in the loop body.
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emit_line("}")

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

            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.header_line("float " + self.cur_token.text + ";")

            self.emitter.emit_line(f"scanf(\"%f\", &{self.cur_token.text});")
            self.match(TokenType.IDENT)
        else:
            raise InvalidTokenError(self.cur_token)
        # Newline.
        self.nl()

    def program(self):
        self.emitter.header_line("#include <stdio.h>")
        self.emitter.header_line("int main(void){")

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

        self.emitter.write_file()
