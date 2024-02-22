from coreofintepreter.types import (
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

    def __peek(self, offset=0) -> Token:
        if not self.__is_at_end(offset):
            return self.__tokens[self.__current + offset]
        return Token(TokenType.EOF, "", None, 0)

    def __previous(self) -> Token:
        return self.__peek(-1)

    def __advance(self) -> None:
        self.__current += 1

    def __take(self) -> Token:
        token = self.__peek()
        self.__advance()
        return token

    def __is_at_end(self, offset=0) -> bool:
        return self.__tokens[self.__current + offset].type == TokenType.EOF

    def __match(self, *types: TokenType) -> bool:
        token = self.__peek()
        if token.type in types:
            self.__advance()
            return True
        return False

    def __consume(self, type: TokenType) -> None:
        token = self.__peek()
        if token.type == type:
            self.__advance()
            return
        raise ValueError(f"{token.lexeme} should be {type}, instead of {token.type}")

    def __number(self):
        token = self.__take()
        if token.type != TokenType.NUMBER:
            raise ValueError(
                f"{token.lexeme} should be {TokenType.NUMBER}, instead of {token.type}"
            )
        return NumberExpression(token)

    def __primary(self) -> Expression:
        if self.__match(TokenType.LEFT_PARENT):
            expr = self.__term()
            self.__consume(TokenType.RIGHT_PARENT)
            return expr
        return self.__number()

    def __unary(self) -> Expression:
        if self.__match(TokenType.MINUS):
            op = self.__previous()
            return UnaryExpression(op, self.__unary())
        return self.__primary()

    def __factor(self) -> Expression:
        expr = self.__unary()
        while self.__match(TokenType.STAR, TokenType.SLASH):
            op = self.__previous()
            right = self.__unary()
            expr = BinaryExpression(op, expr, right)
        return expr

    def __term(self) -> Expression:
        expr = self.__factor()
        while self.__match(TokenType.PLUS, TokenType.MINUS):
            op = self.__previous()
            right = self.__factor()
            expr = BinaryExpression(op, expr, right)
        return expr

    def __expression_statement(self) -> Statement:
        expr = self.__term()
        self.__consume(TokenType.SEMICOLON)
        return Statement(expr)

    # The start of story
    def parse(self) -> list[Statement]:
        statements = list()
        while not self.__is_at_end():
            statements.append(self.__expression_statement())
        return statements
