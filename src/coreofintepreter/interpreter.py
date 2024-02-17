from src.coreofintepreter.types import (
    BinaryExpression,
    Expression,
    NumberExpression,
    Statement,
    TokenType,
    UnaryExpression,
)


class Interpreter:
    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements

    def eval(self, expr: Expression) -> float:
        match expr:
            case binary if isinstance(binary, BinaryExpression):
                left = self.eval(binary.left)
                right = self.eval(binary.right)
                match binary.op.type:
                    case TokenType.PLUS:
                        return left + right
                    case TokenType.MINUS:
                        return left - right
                    case TokenType.STAR:
                        return left * right
                    case TokenType.SLASH:
                        return left / right
                    case _:
                        raise ValueError(f"{binary.op} is not correct binary operator")
            case unary if isinstance(unary, UnaryExpression):
                result: float = self.eval(unary.expr)
                if unary.op.type != TokenType.MINUS:
                    raise ValueError(f"{unary.op} is not correct unary operator")
                return -result
            case number if isinstance(number, NumberExpression):
                if not number.value.literal:
                    raise ValueError(f"{number}'s value is None")
                return number.value.literal

        raise ValueError(f"{expr} is not implemented")

    def cal(self) -> list[float]:
        result = list()
        for statement in self.statements:
            result.append(self.eval(statement.expr))
        return result
