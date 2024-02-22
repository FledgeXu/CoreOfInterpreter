from dataclasses import dataclass
from enum import Enum, auto
from typing import Deque


class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LEFT_PARENT = auto()
    RIGHT_PARENT = auto()
    SEMICOLON = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: float | None
    line: int


class Expression:
    pass


@dataclass
class BinaryExpression(Expression):
    op: Token
    left: Expression
    right: Expression


@dataclass
class UnaryExpression(Expression):
    op: Token
    expr: Expression


@dataclass
class NumberExpression(Expression):
    value: Token


@dataclass
class Statement:
    expr: Expression


class Operations(Enum):
    CONSTANTS = auto()
    NEGATIVE = auto()
    ADD = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIV = auto()
    RETURN = auto()


@dataclass
class Code:
    Op: Operations
    data: float | None


Chunks = Deque[Code]
