from lark.lexer import Token
from lark.tree import Tree
from lark.visitors import Interpreter


class CodeTranspiler(Interpreter):
    def __init__(self):
        super().__init__()
        self.imports = []
        self.functions = []
        self.main_function = []
        self.output_buffer = []
        self.indent_level = 0

    def __default__(self, tree):
        """
        Default visitor for any node that doesn't have a specific method.
        This will help us see the structure of the AST.
        """
        print(f"DEBUG: Visiting unhandled node -> {tree.data}")
        return self.visit_children(tree)

    def statements(self, tree):
        """Visitor for a statements block."""
        self.visit_children(tree)

    def type(self, tree):
        """Processes a type node and returns the C equivalent as a string."""
        type_token = tree.children[0]
        type_map = {
            "TYPE_INT": "int",
            "TYPE_FLOAT": "float",
            "TYPE_VOID": "void",
            "TYPE_BOOLEAN": "bool",
            "TYPE_STRING": "char*",
        }
        if type_map[type_token.type] == "bool":
            self._emit_import("stdbool.h")
        if type_token.type in type_map:
            return type_map[type_token.type]
        elif type_token.value in type_map:
            return type_map[type_token.value]
        return "/* unknown type */"

    def log_expr(self, tree):
        """
        Visitor for a logical expression.
        """
        if len(tree.children) > 1 and isinstance(tree.children[1], Token):
            left = self.visit(tree.children[0])
            op = tree.children[1].value
            right = self.visit(tree.children[2])
            return f"{left} {op} {right}"
        return self.visit(tree.children[0])

    def rel_expr(self, tree):
        """
        Visitor for a relational expression.
        """
        if len(tree.children) > 1 and isinstance(tree.children[1], Token):
            left = self.visit(tree.children[0])
            op = tree.children[1].value
            right = self.visit(tree.children[2])
            op_map = {"<>": "!="}
            c_op = op_map.get(op, op)
            return f"{left} {c_op} {right}"
        return self.visit(tree.children[0])

    def expr(self, tree):
        """
        Visitor for an arithmetic expression (addition/subtraction).
        """
        if len(tree.children) > 1 and isinstance(tree.children[1], Token):
            left = self.visit(tree.children[0])
            op = tree.children[1].value
            right = self.visit(tree.children[2])
            return f"{left} {op} {right}"
        return self.visit(tree.children[0])

    def term(self, tree):
        """
        Visitor for a term in an expression (multiplication/division).
        """
        return self.expr(tree)

    def factor(self, tree):
        """Visitor for a factor. Passes through to the actual value."""
        return self.visit(tree.children[0])

    def value(self, tree):
        """
        Visitor for a value, which can be a literal, an identifier, or another expression.
        """
        child = tree.children[0]
        if isinstance(child, Token):
            return child.value
        else:
            return self.visit(child)

    def literal(self, tree):
        """Visitor for a literal value (int, float, string)."""
        literal_token = tree.children[0]
        return literal_token.value

    def structures(self, tree):
        """Visitor for the 'structures' wrapper rule."""
        self.visit_children(tree)

    def struct(self, tree):
        """Visitor for the 'struct' wrapper rule."""
        self.visit_children(tree)

    def struct_cond(self, tree):
        """
        Visitor for a full if-elif-else conditional structure.
        This method handles the entire chain to get the C-style formatting correct.
        """
        if_condition = self.visit(tree.children[0])
        if_block = tree.children[1]
        self._emit_code(f"if ({if_condition}) {{")
        self.indent_level += 1
        self.visit(if_block)
        self.indent_level -= 1
        remaining_clauses = tree.children[2:]
        for clause in remaining_clauses:
            if clause.data == "elif_":
                elif_condition = self.visit(clause.children[0])
                elif_block = clause.children[1]
                self._emit_code(f"}} else if ({elif_condition}) {{")
                self.indent_level += 1
                self.visit(elif_block)
                self.indent_level -= 1
            elif clause.data == "else_":
                else_block = clause.children[0]
                self._emit_code("} else {")
                self.indent_level += 1
                self.visit(else_block)
                self.indent_level -= 1
        self._emit_code("}")

    def elif_(self, tree):
        """Visitor for the 'elif' rule, which becomes 'else if' in C."""
        condition = self.visit(tree.children[0])
        self._emit_code(f"else if ({condition}) {{")
        self.indent_level += 1
        self.visit(tree.children[1])
        self.indent_level -= 1
        self._emit_code("}")

    def else_(self, tree):
        """Visitor for the 'else' rule."""
        self._emit_code("else {")
        self.indent_level += 1
        self.visit(tree.children[0])
        self.indent_level -= 1
        self._emit_code("}")

    def increm_decrem(self, tree):
        """
        Visitor for increment/decrement expressions (e.g., i++, i--).
        Returns the expression as a string.
        """
        var_name = tree.children[0].value
        operator = "++"
        if len(tree.children) > 1:
            operator = tree.children[1].value
        return f"{var_name}{operator}"

    def assign_expr(self, tree):
        """
        Visitor for an assignment statement.
        e.g., x = x + i
        """
        var_name = tree.children[0].value
        expression = self.visit(tree.children[1])
        self._emit_code(f"{var_name} = {expression};")

    def struct_rep(self, tree):
        """Visitor for the repetition structure wrapper rule (for, while)."""
        self.visit_children(tree)

    def while_(self, tree):
        """Visitor for a while loop."""
        _condition = self.visit(tree.children[0])
        _block = tree.children[1]
        _signature = f"while ({_condition})"
        self._emit_code(_signature + " {")
        self.indent_level += 1
        self.visit(_block)
        self.indent_level -= 1
        self._emit_code("}")

    def for_(self, tree):
        """Visitor for a C-style for loop."""
        init_node = tree.children[0]
        init_type = self.visit(init_node.children[0])
        init_name = init_node.children[1].value
        init_value = self.visit(init_node.children[2])
        initialization = f"{init_type} {init_name} = {init_value}"
        condition = self.visit(tree.children[1])
        step = self.visit(tree.children[2])
        block = tree.children[3]
        self._emit_code(f"for ({initialization}; {condition}; {step}) {{")
        self.indent_level += 1
        self.visit(block)
        self.indent_level -= 1
        self._emit_code("}")

    def return_(self, tree):
        """Visitor for a return statement."""
        value = self.visit(tree.children[0])
        if value in ["0", "1", "true", "false"]:
            self._emit_import("stdbool.h")
        self._emit_code(f"return {value};")

    def array_list(self, tree):
        """
        Processes a list of literals for array initialization.
        e.g., {"José", "João", "Maria"}
        """
        values = [self.visit(child) for child in tree.children]
        return ", ".join(values)

    def array(self, tree: Tree):
        """
        Visitor for an array declaration.
        If an array is declared without a size or initializer,
        it defaults to a size of 10.
        """
        c_type = self.visit(tree.children[0])
        array_size = None
        var_name = None
        initial_values = None
        for child in tree.children[1:]:
            if isinstance(child, Token):
                if child.type == "ID":
                    var_name = child.value
                elif child.type == "LITERAL_INT":
                    array_size = child.value
            elif isinstance(child, Tree) and child.data == "array_list":
                initial_values = self.visit(child)
        if initial_values:
            size_str = array_size if array_size is not None else ""
            self._emit_code(
                f"{c_type} {var_name}[{size_str}] = {{ {initial_values} }};"
            )
        elif array_size is not None:
            self._emit_code(f"{c_type} {var_name}[{array_size}];")
        else:
            default_size = 10
            self._emit_code(f"{c_type} {var_name}[{default_size}];")

    def variable(self, tree):
        """
        Visitor for a variable declaration.
        Handles both declaration-only and declaration with initialization.
        AST rule: variable: type ID (log_expr)?
        """
        c_type = self.visit(tree.children[0])
        var_name = tree.children[1].value
        if len(tree.children) > 2:
            initial_value = self.visit(tree.children[2])
            self._emit_code(
                f"{'const ' if c_type == 'char*' else ''}{c_type} {var_name} = {initial_value};"
            )
        else:
            self._emit_code(f"{c_type} {var_name};")

    def parameters(self, tree):
        """Visit each child node (which are expressions)"""
        args = [self.visit(child) for child in tree.children]
        return ", ".join(args)

    def parameter_def(self, tree):
        """Processes a single parameter definition (e.g., 'int a')."""
        c_type = self.visit(tree.children[0])
        param_name = tree.children[1].value
        return f"{c_type} {param_name}"

    def parameters_def_list(self, tree):
        """Processes a list of parameter definitions."""
        param_list = [self.visit(child) for child in tree.children]
        return ", ".join(param_list)

    def parameters_def(self, tree):
        """Processes the main parameter block."""
        if tree.children:
            return self.visit(tree.children[0])
        return ""

    def declarations(self, tree):
        """Visitor for the 'declarations' rule."""
        self.visit_children(tree)

    def function_call(self, tree):
        """Visitor for a function call statement."""
        function_name = tree.children[0].value
        param_str = ""
        if len(tree.children) > 1:
            param_str = self.visit(tree.children[1])
        self._emit_code(f"{function_name}({param_str});")

    def function(self, tree) -> None:
        """
        Visitor for a function declaration. This now handles nested functions
        by isolating the buffer AND indentation level for each function.
        """
        is_main = tree.children[0].value == "main"
        parent_buffer_backup = self.output_buffer
        parent_indent_backup = self.indent_level
        self.output_buffer = []
        self.indent_level = 0
        token_function_name = tree.children[0]
        token_function_params = tree.children[1]
        token_function_return_type = tree.children[2]
        token_function_return_block = tree.children[3]
        return_type = self._map_type(token_function_return_type)
        if is_main:
            return_type = "int"
        _signature = f"{return_type} {token_function_name.value}"
        _params = f"({self.visit(token_function_params)})"
        self._emit_code(_signature + _params + " {")
        self.indent_level += 1
        self.visit(token_function_return_block)
        if is_main and return_type == "int":
            self._emit_code("return 0;")
        self.indent_level -= 1
        self._emit_code("}\n")
        if is_main:
            self.main_function.extend(self.output_buffer)
        else:
            self.functions = self.output_buffer + self.functions
        self.output_buffer = parent_buffer_backup
        self.indent_level = parent_indent_backup

    def block(self, tree) -> None:
        """Visitor for a block of statements."""
        self.visit_children(tree)

    # Início
    # self.visit(ast) chama este método
    def program(self, tree) -> None:
        """Visitor for the top-level program rule."""
        self.visit_children(tree)

    def _emit_code(self, line, indent=True):
        """Appends transpiled code to the current output buffer."""
        if indent:
            indent_str = "    " * self.indent_level
            self.output_buffer.append(f"{indent_str}{line}")
        else:
            self.output_buffer.append(line)

    def _emit_import(self, module: str) -> None:
        """Appends transpiled import statements to self.imports"""
        import_statement = f"#include <{module}>"
        if import_statement not in self.imports:
            self.imports.append(import_statement)

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

    def _transpile(self, ast):
        """Starts the transpilation process and assembles the final code."""
        self.visit(ast)
        _imports = "\n".join(self.imports) + "\n"
        _functions_str = "\n".join(self.functions)
        _main_str = "\n".join(self.main_function)
        final_code = []
        if self.imports:
            final_code.append(_imports)
        if self.functions:
            final_code.append(_functions_str)
        if _main_str:
            final_code.append(_main_str)
        return "\n".join(final_code)
