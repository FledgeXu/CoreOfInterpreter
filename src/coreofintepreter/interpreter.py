from coreofintepreter.types import (
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
            case BinaryExpression(op, left_expr, right_expr):
                left = self.eval(left_expr)
                right = self.eval(right_expr)
                match op.type:
                    case TokenType.PLUS:
                        return left + right
                    case TokenType.MINUS:
                        return left - right
                    case TokenType.STAR:
                        return left * right
                    case TokenType.SLASH:
                        return left / right
                    case _:
                        raise ValueError(f"{op} is not correct binary operator")
            case UnaryExpression(op, expr):
                result: float = self.eval(expr)
                if op.type != TokenType.MINUS:
                    raise ValueError(f"{op} is not correct unary operator")
                return -result
            case NumberExpression(value):
                if not value.literal:
                    raise ValueError(f"{value}'s value is None")
                return value.literal

        raise ValueError(f"{expr} is not implemented")

    def cal(self) -> list[float]:
        result = list()
        for statement in self.statements:
            result.append(self.eval(statement.expr))
        return result
