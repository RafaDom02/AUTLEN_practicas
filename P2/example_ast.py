import ast
import inspect
from ast_utils import *


def test_ast(hola: int, mi_lista: list):
    for i in range(0, 20):
        for j in range(0, 100):
            if i % 2 == 0 and j % 2 == 0:
                for k in [2, 4, 5, 6, 3, 1, 34, 75]:
                    print(k)


def test_ast2():
    for i in range(0, 20):
        print(i)
    for i in range(0, 20):
        print(i)
    for i in range(0, 20):
        print(i)


def print_if_pos(num):
    if num > 0:
        print(num)


def fun3(x):
    num = x+2
    if num > 0:
        print(num)


def fun4(p):
    for a in [10, 20, 30]:
        print(a)
        for b in [1, 2, 3]:
            print(2*a+b)
    for x in range(10):
        print(x)
    for i, x in enumerate([10, 20, 30]):
        print(i, x)

if __name__ == "__main__":
    counter = ASTNestedForCounter()
    dot = ASTDotVisitor()

    source = inspect.getsource(print_if_pos)
    my_ast = ast.parse(source)
    print("Test de ASTDotVisitor --> mirar graphic.dot")

    source = inspect.getsource(test_ast)
    my_ast = ast.parse(source)
    print("For's anidados de test1: ", counter.visit(my_ast))

    source = inspect.getsource(test_ast2)
    my_ast = ast.parse(source)
    print("For's anidados de test2: ", counter.visit(my_ast))

    print("Test de ASTReplaceVar")
    source = inspect.getsource(fun3)
    my_ast = ast.parse(source)
    print(source)
    repl = ASTReplaceVar("num", ast.Constant(0))
    repl.visit(my_ast)
    print(ast.unparse(my_ast))

    print("\nTest de ASTUnroll")
    unroll = ASTUnroll()
    source = inspect.getsource(fun4)
    my_ast = ast.parse(source)
    unroll.visit(my_ast)
    print(ast.unparse(my_ast))
