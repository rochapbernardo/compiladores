from lark import Lark, tree

grammar = None
with open("grammar.lark") as g:
    grammar = g.read()

parser = Lark(grammar, start="program", parser="lalr")

code = r"""
func add(int a, int b) -> int {
    return a + b
}
"""

ast = parser.parse(code)

tree.pydot__tree_to_png(ast, "function.png")
