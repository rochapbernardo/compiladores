from lark import Lark, tree, UnexpectedInput
from lark.indenter import Indenter
from codeTranspiler import CodeTranspiler

#classe para fazer a identacao e quebra de linha do codigo grammar.lark
class TreeIndenter(Indenter):
  NL_type = '_NL'
  OPEN_PAREN_types = []
  CLOSE_PAREN_types = []
  INDENT_type = '_INDENT'
  DEDENT_type = '_DEDENT'
  tab_len = 4

class Compiler:

    def __init__(self):
        #abrir e ler a gramatica lark criada
        with open ("grammar.lark", "r") as grammar_file:
            grammar = grammar_file.read()

        #criar um parser a partir da gramatica usando o Lark (biblioteca de analise sintatica)
        self.parser = Lark(grammar, start="program", parser="lalr", postlex=TreeIndenter())
        self.transpiler = CodeTranspiler()

    #retorna o resultado da chamada
    def parse(self, code):
        return self.parser.parse(code)
    
    #metodo para gerar a imagem da arvore
    def tree_to_png(self, code, img_path="code.png"):
        ast = self.parse(code)
        tree.pydot__tree_to_png(ast, "code.png")
    
    #metodo para gerar o codigo em C
    def transpile(self, code, c_path="code.c"):
        ast = self.parse(code)
        transpiled_code = self.transpiler.transpile(ast)
        #gravar o codigo C em um arquivo
        with open(c_path, "w") as c_file:
            c_file.write(transpiled_code)