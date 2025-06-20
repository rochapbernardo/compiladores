from lark import Lark, tree, UnexpectedInput
from lark.indenter import Indenter

class TreeIndenter(Indenter):
  NL_type = '_NL'
  OPEN_PAREN_types = []
  CLOSE_PAREN_types = []
  INDENT_type = '_INDENT'
  DEDENT_type = '_DEDENT'
  tab_len = 4

class Compiler:
    def __init__(self):
        with open ("grammar.lark", "r") as grammar_file:
            grammar = grammar_file.read()

        self.parser = Lark(grammar, start="program", parser="lalr", postlex=TreeIndenter())

    def parse(self, code):
        return self.parser.parse(code)
    
    def tree_to_png(self, code, img_path="code.png"):
        ast = self.parse(code)
        tree.pydot__tree_to_png(ast, "code.png")  