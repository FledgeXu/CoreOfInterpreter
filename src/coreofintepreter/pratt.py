from dataclasses import dataclass
from enum import Enum
from typing import Callable
from src.coreofintepreter.types import (
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
            TokenType.NUMBER: TokenRule(self.number, None, Precedence.NONE),
            TokenType.PLUS: TokenRule(None, self.binary, Precedence.TERM),
            TokenType.MINUS: TokenRule(self.unary, self.binary, Precedence.TERM),
            TokenType.STAR: TokenRule(None, self.binary, Precedence.FACTOR),
            TokenType.SLASH: TokenRule(None, self.binary, Precedence.FACTOR),
            TokenType.LEFT_PARENT: TokenRule(self.grouping, None, Precedence.UNARY),
            TokenType.RIGHT_PARENT: TokenRule(None, None, Precedence.NONE),
            TokenType.EOF: TokenRule(None, None, Precedence.NONE),
            TokenType.SEMICOLON: TokenRule(None, None, Precedence.NONE),
        }

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

    def get_rule(self, token: Token) -> TokenRule:
        rule = self.rules.get(token.type)
        if not rule:
            raise ValueError(f"{token}'s rule is None")
        return rule

    def number(self) -> Expression:
        token = self.take()
        if token.type != TokenType.NUMBER:
            raise ValueError(
                f"{token.lexeme} should be {TokenType.NUMBER}, instead of {token.type}"
            )
        return NumberExpression(token)

    def grouping(self) -> Expression:
        self.advance()
        expr = self.expression()
        self.consume(TokenType.RIGHT_PARENT)
        return expr

    def unary(self) -> Expression:
        op = self.take()
        expr = self.expression(self.get_rule(op).precedence.value)
        if op.type != TokenType.MINUS:
            raise ValueError(
                f"{op.lexeme} should be {TokenType.MINUS}, instead of {op.type}"
            )
        return UnaryExpression(op, expr)

    def binary(self) -> Expression:
        op = self.take()
        return self.expression(self.get_rule(op).precedence.value + 1)

    def expression(self, precedence: float = Precedence.DEFAULT.value) -> Expression:
        prefix = self.get_rule(self.peek()).prefix
        if not prefix:
            raise ValueError(f"Can not found prefix rule for {self.peek()}")
        expr = prefix()

        while precedence <= self.get_rule(self.peek()).precedence.value:
            op = self.peek()
            infix = self.get_rule(op).infix
            if not infix:
                raise ValueError(f"Can not found infix rule for {self.peek()}")
            expr = BinaryExpression(op, expr, infix())
        return expr

    def expression_statement(self) -> Statement:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON)
        return Statement(expr)

    # The start of story
    def parse(self) -> list[Statement]:
        statements = list()
        while not self.is_at_end():
            statements.append(self.expression_statement())
        return statements
