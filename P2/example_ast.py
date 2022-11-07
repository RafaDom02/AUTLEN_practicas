import ast
import inspect
from ast_utils import ASTNestedForCounter

def test_ast(hola: int, mi_lista: list):
    for i in range(0,20):
        for j in range (0,100):
            if i%2 == 0 and j%2 == 0:
                for k in [2,4,5,6,3,1,34,75]:
                    print(k)
def test_ast2():
    for i in range(0,20):
        print(i)
    for i in range(0,20):
        print(i)
    for i in range(0,20):
        print(i)



if __name__ == "__main__":
    counter = ASTNestedForCounter()

    source = inspect.getsource(test_ast)
    my_ast = ast.parse(source)
    print("For's anidados de test1: ", counter.visit(my_ast))
    
    source = inspect.getsource(test_ast2)
    my_ast = ast.parse(source)
    print("For's anidados de test2: ", counter.visit(my_ast))
    
    """"
    with open("test_ast.dot", "w") as f:
        f.write(ast.dump(my_ast,indent=4))
    """