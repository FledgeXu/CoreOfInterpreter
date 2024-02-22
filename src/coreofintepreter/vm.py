from coreofintepreter.types import Chunks, Operations, Code


class VirtualMachine:
    def __init__(self, chunk: Chunks) -> None:
        self.__chunk = chunk
        self.stack: list[float] = list()

    def __execute(self):
        code = self.__chunk.popleft()

        match code:
            case Code(Operations.CONSTANTS, data):
                if not isinstance(data, float):
                    raise ValueError(f"{data} is not a number")
                self.stack.append(data)
            case Code(Operations.NEGATIVE, _):
                self.stack.append(-self.stack.pop())
            case Code(Operations.ADD, _):
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            case Code(Operations.MINUS, _):
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            case Code(Operations.MULTIPLY, _):
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            case Code(Operations.DIV, _):
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a / b)
            case Code(Operations.RETURN, _):
                print(self.stack.pop())

    def run(self):
        while self.__chunk:
            self.__execute()
