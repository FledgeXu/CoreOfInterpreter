from coreofintepreter.types import (
    Chunks,
    Expression,
    NumberExpression,
    Operations,
    BinaryExpression,
    Statement,
    TokenType,
    UnaryExpression,
    Code,
)

from collections import deque


class Generator:
    def __init__(self, statements: list[Statement]) -> None:
        self.__statements = statements
        self.__operations: Chunks = deque()

    def __generate_code(self, expr: Expression):
        match expr:
            case BinaryExpression(op, left_expr, right_expr):
                self.__generate_code(left_expr)
                self.__generate_code(right_expr)
                match op.type:
                    case TokenType.PLUS:
                        self.__operations.append(Code(Operations.ADD, None))
                    case TokenType.MINUS:
                        self.__operations.append(Code(Operations.MINUS, None))
                    case TokenType.STAR:
                        self.__operations.append(Code(Operations.MULTIPLY, None))
                    case TokenType.SLASH:
                        self.__operations.append(Code(Operations.DIV, None))
                    case _:
                        raise ValueError(f"{op} is not correct binary operator")
            case UnaryExpression(op, expr):
                self.__generate_code(expr)
                if op.type != TokenType.MINUS:
                    raise ValueError(f"{op} is not correct unary operator")
                self.__operations.append(Code(Operations.NEGATIVE, None))
            case NumberExpression(value):
                if not value.literal:
                    raise ValueError(f"{value}'s value is None")
                self.__operations.append(Code(Operations.CONSTANTS, value.literal))
        return self.__operations

    def generate(self) -> Chunks:
        for statement in self.__statements:
            self.__generate_code(statement.expr)
            self.__operations.append(Code(Operations.RETURN, None))
        return self.__operations
