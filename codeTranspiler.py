from lark.visitors import Interpreter


class CodeTranspiler(Interpreter):
    def __init__(self):
        super().__init__()
        self.output = []
        self.imports = []
        self.indent_level = 0

    
    #funcao para emitir texto dentro do output
    def emit(self, line):
        #calcular o identacao
        ident = '    ' * self.indent_level
        self.output.append(f"{ident}{line}")

    def program(self, tree):
        self.emit("#include <stdio.h>\n")
        self.visit_children(tree)

    def function(self, tree):
        name, parameters, fn_type, *block = tree.children
        #prepocess
        name = name.value
        parameters = self.visit_children(parameters)[0]
        fn_type = self.visit_children(fn_type)[0]

        #emit function
        self.emit(f"{fn_type} {name}({self.parameters_to_str(parameters)}) {{")
        self.indent_level += 1

        #emit block
        for blocks in block:
            self.visit_children(blocks)

        self.indent_level -= 1
        self.emit(f"}}")

        #print(parameters)
        #exit(0)

    def parameters_to_str(self, parameters):
        parameters_str = ""
        
        for i, p in enumerate(parameters):
            parameters_str += f"{p['type']} {p['id']}"
            if i+1 != len(parameters):
                parameters_str += ","

        return parameters_str

    def parameters_def_list(self, tree):
        return self.visit_children(tree)
    
    def parameter_def(self, tree):
        return {
            'type': self.visit_children(tree.children[0])[0].value,
            'id': tree.children[1].value
        }

    def type(self, tree):
        return tree.children[0].value

    #metodo para retornar a lista
    def transpile(self, ast):
        #visitar os nos
        self.visit(ast)
        return "\n".join(self.output)
