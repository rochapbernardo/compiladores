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

    def transpile(self, ast):
        """Starts the transpilation process."""
        self.visit(ast)
        return f"{'\n'.join(self.imports)}\n\n{'\n'.join(self.output)}"

    def type(self, tree):
        """Processes a type node and returns the C equivalent as a string."""
        type_token = tree.children[0]
        type_map = {
            "TYPE_INT": "int",
            "TYPE_FLOAT": "float",
            "TYPE_VOID": "void",
            "TYPE_BOOL": "bool",
            "TYPE_STR": "char*",
        }
        if type_token.type in type_map:
            return type_map[type_token.type]
        elif type_token.value in type_map:
            return type_map[type_token.value]
        return "/* unknown type */"

    def _map_type(self, type_node):
        """Maps custom language types to C types."""
        type_name = type_node.children[0].value
        type_map = {
            "void": "void",
            "int": "int",
            "float": "float",
            "bool": "bool",
            "str": "char*",
        }
        return type_map.get(type_name, "/* unknown type */")

    # Início
    # self.visit(ast) chama este método
    def program(self, tree) -> None:
        """Visitor for the top-level program rule."""
        self.emit_import("stdio.h")
        self.visit_children(tree)






