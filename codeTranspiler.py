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



    # Início
    # self.visit(ast) chama este método
    def program(self, tree) -> None:
        """Visitor for the top-level program rule."""
        self.emit_import("stdio.h")
        self.visit_children(tree)






