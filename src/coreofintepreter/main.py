import sys
from coreofintepreter.pratt import Pratt
from coreofintepreter.interpreter import Interpreter

from coreofintepreter.lexer import Lexer
from coreofintepreter.parser import Parser
from coreofintepreter.generator import Generator
from coreofintepreter.vm import VirtualMachine


def repl():
    while True:
        try:
            source_code = input("> ")
            run(source_code)
        except EOFError:
            break


def run_file(path: str):
    with open(path, "r") as source_file:
        run(source_file.read())


def run(source_code: str):
    try:
        lexer = Lexer(source_code.strip())
        tokens = lexer.scan()
        # parser = Parser(tokens)
        parser = Pratt(tokens)
        statements = parser.parse()
        generator = Generator(statements)
        chunk = generator.generate()
        vm = VirtualMachine(chunk)
        vm.run()
        # interpreter = Interpreter(statements)
        # for result in interpreter.cal():
        #     print(result)
    except ValueError as exc:
        print(exc)


def main():
    if len(sys.argv) == 1:
        repl()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print("Usage: cal [path]")
