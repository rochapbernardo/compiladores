from lark import Lark, tree

grammar = None
with open("grammar.lark") as g:
    grammar = g.read()

parser = Lark(grammar, start="program", parser="lalr")

code = r"""
func add() -> bool {
    x = 10
    if (x < 10) {
        return 1
    }
    return 0
}
"""

ast = parser.parse(code)

tree.pydot__tree_to_png(ast, "indent.png")
