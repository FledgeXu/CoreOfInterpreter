from dataclasses import dataclass
from enum import Enum
from typing import Callable
from coreofintepreter.types import (
    BinaryExpression,
    Expression,
    NumberExpression,
    Token,
    TokenType,
    UnaryExpression,
    Statement,
)


class Precedence(Enum):
    NONE = 0
    DEFAULT = 1
    TERM = 1
    FACTOR = 2
    UNARY = 3


@dataclass
class TokenRule:
    prefix: None | Callable[[], Expression]
    infix: None | Callable[[], Expression]
    precedence: Precedence


class Pratt:
    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.__current = 0
        self.rules: dict[TokenType, TokenRule] = {
            TokenType.NUMBER: TokenRule(self.__number, None, Precedence.NONE),
            TokenType.PLUS: TokenRule(None, self.__binary, Precedence.TERM),
            TokenType.MINUS: TokenRule(self.__unary, self.__binary, Precedence.TERM),
            TokenType.STAR: TokenRule(None, self.__binary, Precedence.FACTOR),
            TokenType.SLASH: TokenRule(None, self.__binary, Precedence.FACTOR),
            TokenType.LEFT_PARENT: TokenRule(self.__grouping, None, Precedence.UNARY),
            TokenType.RIGHT_PARENT: TokenRule(None, None, Precedence.NONE),
            TokenType.EOF: TokenRule(None, None, Precedence.NONE),
            TokenType.SEMICOLON: TokenRule(None, None, Precedence.NONE),
        }

    def __peek(self, offset=0) -> Token:
        if not self.__is_at_end(offset):
            return self.__tokens[self.__current + offset]
        return Token(TokenType.EOF, "", None, 0)

    def __advance(self) -> None:
        self.__current += 1

    def __take(self) -> Token:
        token = self.__peek()
        self.__advance()
        return token

    def __is_at_end(self, offset=0) -> bool:
        return self.__tokens[self.__current + offset].type == TokenType.EOF

    def __consume(self, type: TokenType) -> None:
        token = self.__peek()
        if token.type == type:
            self.__advance()
            return
        raise ValueError(f"{token.lexeme} should be {type}, instead of {token.type}")

    def __get_rule(self, token: Token) -> TokenRule:
        rule = self.rules.get(token.type)
        if not rule:
            raise ValueError(f"{token}'s rule is None")
        return rule

    def __number(self) -> Expression:
        token = self.__take()
        if token.type != TokenType.NUMBER:
            raise ValueError(
                f"{token.lexeme} should be {TokenType.NUMBER}, instead of {token.type}"
            )
        return NumberExpression(token)

    def __grouping(self) -> Expression:
        self.__advance()
        expr = self.__expression()
        self.__consume(TokenType.RIGHT_PARENT)
        return expr

    def __unary(self) -> Expression:
        op = self.__take()
        expr = self.__expression(self.__get_rule(op).precedence.value)
        if op.type != TokenType.MINUS:
            raise ValueError(
                f"{op.lexeme} should be {TokenType.MINUS}, instead of {op.type}"
            )
        return UnaryExpression(op, expr)

    def __binary(self) -> Expression:
        op = self.__take()
        return self.__expression(self.__get_rule(op).precedence.value + 1)

    def __expression(self, precedence: float = Precedence.DEFAULT.value) -> Expression:
        prefix = self.__get_rule(self.__peek()).prefix
        if not prefix:
            raise ValueError(f"Can not found prefix rule for {self.__peek()}")
        expr = prefix()

        while precedence <= self.__get_rule(self.__peek()).precedence.value:
            op = self.__peek()
            infix = self.__get_rule(op).infix
            if not infix:
                raise ValueError(f"Can not found infix rule for {self.__peek()}")
            expr = BinaryExpression(op, expr, infix())
        return expr

    def __expression_statement(self) -> Statement:
        expr = self.__expression()
        self.__consume(TokenType.SEMICOLON)
        return Statement(expr)

    # The start of story
    def parse(self) -> list[Statement]:
        statements = list()
        while not self.__is_at_end():
            statements.append(self.__expression_statement())
        return statements
