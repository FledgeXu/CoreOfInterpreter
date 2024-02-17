from src.coreofintepreter.types import Token, TokenType


OpsType: dict[str, TokenType] = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "(": TokenType.LEFT_PARENT,
    ")": TokenType.RIGHT_PARENT,
    ";": TokenType.SEMICOLON,
}


class Lexer:
    def __init__(self, source: str) -> None:
        self.__source = source
        self.__start = 0
        self.__end = 0
        self.__line = 1

    def take(self) -> str:
        char = self.peek()
        self.advance()
        return char

    def peek(self) -> str:
        if not self.is_at_end():
            return self.__source[self.__end]
        return ""

    def advance(self) -> None:
        if self.peek() == "\n":
            self.__line += 1
        self.__end += 1

    def is_at_end(self) -> bool:
        return not self.__end < len(self.__source)

    def parse(self) -> Token | None:
        char = self.take()
        match char:
            case space if space.isspace():
                return None
            case "+" | "-" | "*" | "/" | "(" | ")" | ";" as op:
                return Token(OpsType[op], op, None, self.__line)
            case number if number.isdigit():
                while not self.is_at_end() and self.peek().isdigit():
                    self.advance()

                if not self.is_at_end() and self.peek() == ".":
                    self.advance()
                    while not self.is_at_end() and self.peek().isdigit():
                        self.advance()
                lexeme = self.__source[self.__start : self.__end]
                return Token(TokenType.NUMBER, lexeme, float(lexeme), self.__line)
            case _:
                raise ValueError(f"{self.__line}:{char} is illegal symbol")

    # Start of the story
    def scan(self) -> list[Token]:
        tokens = list()
        while not self.is_at_end():
            if token := self.parse():
                tokens.append(token)
            self.__start = self.__end
        tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return tokens
