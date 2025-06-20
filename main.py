from lark import Lark, tree, UnexpectedInput
from lark.indenter import Indenter

with open ("grammar.lark", "r") as grammar_file:
  grammar = grammar_file.read()

code = r'''
func (int a, int b) {
    return a + b
}
'''
class TreeIndenter(Indenter):
  NL_type = '_NL'
  OPEN_PAREN_types = []
  CLOSE_PAREN_types = []
  INDENT_type = '_INDENT'
  DEDENT_type = '_DEDENT'
  tab_len = 2


try:
  parser = Lark(grammar, start="program", parser="lalr", postlex=TreeIndenter())
  ast = parser.parse(code)
  tree.pydot__tree_to_png(ast, "code.png")
except UnexpectedInput as u:
  mensagem = "Erro sintático (Linha: {}, Coluna: {}) - Valor esperado: {}, Valor recebido: {}".format(u.line, u.column, u.expected, u.token)
  print(mensagem)