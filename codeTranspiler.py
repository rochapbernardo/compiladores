#visitar os nos da arvore, Interpreter para visitar a arvore top-down
from lark.visitors import Interpreter

class CodeTranspiler(Interpreter):
    def __init__(self):
        super().__init__()

        #guardar as strings das linhas geradas
        self.output = []

        #para poder identar o codigo em C
        self.indent_level = 0

        #salvar as variaveis e funcoes
        self.globals = {
            'variables':{},
            'functions':{}
        }
    
    #funcao para emitir texto dentro do output
    def emit(self, line):
        #calcular o identacao
        ident = '    ' * self.indent_level
        self.output.append(f"{ident}{line}")

    def program(self, tree):
        self.emit("#include <stdio.h>")
        self.visit_children(tree)

    def function(self, tree):
        name, parameters, fn_type, *block = tree.children
        #prepocess
        name = name.value
        parameters = self.visit_children(parameters)
        fn_type = self.visit_children(fn_type)[0]

        for blocks in block:
            self.visit_children(blocks)

        print(name)
        print(parameters)
        print(fn_type)
        print(block)
        exit(0)

    def type(self, tree):
        return tree.children[0].value

    #metodo para retornar a lista
    def transpile(self, ast):
        #visitar os nos
        self.visit(ast)
        return "\n".join(self.output)
