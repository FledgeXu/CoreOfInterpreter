from src.coreofintepreter.types import (
    BinaryExpression,
    Expression,
    NumberExpression,
    Token,
    TokenType,
    UnaryExpression,
    Statement,
)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.__current = 0

    def peek(self, offset=0) -> Token:
        if not self.is_at_end(offset):
            return self.__tokens[self.__current + offset]
        return Token(TokenType.EOF, "", None, 0)

    def previous(self) -> Token:
        return self.peek(-1)

    def advance(self) -> None:
        self.__current += 1

    def take(self) -> Token:
        token = self.peek()
        self.advance()
        return token

    def is_at_end(self, offset=0) -> bool:
        return self.__tokens[self.__current + offset].type == TokenType.EOF

    def match(self, *types: TokenType) -> bool:
        token = self.peek()
        if token.type in types:
            self.advance()
            return True
        return False

    def consume(self, type: TokenType) -> None:
        token = self.peek()
        if token.type == type:
            self.advance()
            return
        raise ValueError(f"{token.lexeme} should be {type}, instead of {token.type}")

    def number(self):
        token = self.take()
        if token.type != TokenType.NUMBER:
            raise ValueError(
                f"{token.lexeme} should be {TokenType.NUMBER}, instead of {token.type}"
            )
        return NumberExpression(token)

    def primary(self) -> Expression:
        if self.match(TokenType.LEFT_PARENT):
            expr = self.term()
            self.consume(TokenType.RIGHT_PARENT)
            return expr
        return self.number()

    def unary(self) -> Expression:
        if self.match(TokenType.MINUS):
            op = self.previous()
            return UnaryExpression(op, self.unary())
        return self.primary()

    def factor(self) -> Expression:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            right = self.unary()
            expr = BinaryExpression(op, expr, right)
        return expr

    def term(self) -> Expression:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpression(op, expr, right)
        return expr

    def expression_statement(self) -> Statement:
        expr = self.term()
        self.consume(TokenType.SEMICOLON)
        return Statement(expr)

    # The start of story
    def parse(self) -> list[Statement]:
        statements = list()
        while not self.is_at_end():
            statements.append(self.expression_statement())
        return statements
