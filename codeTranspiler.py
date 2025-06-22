from lark.visitors import Interpreter


class CodeTranspiler(Interpreter):
    def __init__(self):
        super().__init__()
        self.output = []
        self.imports = []
        self.indent_level = 0

    def emit_code(self, line, indent=True):
        if indent:
            indent_str = "    " * self.indent_level
            self.output.append(f"{indent_str}{line}")
        else:
            self.output.append(line)

    def emit_import(self, module: str) -> None:
        """Adds import modules."""
        # TODO: verificar se já não existe
        import_statement = f"#include <{module}>"
        self.imports.append(import_statement)

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
    # Início
    # self.visit(ast) chama este método
    def program(self, tree) -> None:
        """Visitor for the top-level program rule."""
        self.emit_import("stdio.h")
        self.visit_children(tree)

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
