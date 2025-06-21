import argparse
from compiler import Compiler

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog="Zen Compiler",
    description="A Simple Compiler"
  )
  parser.add_argument("code_path")
  parser.add_argument("--tree", action='store_true')
  parser.add_argument("--transpile", action='store_true')
  args = parser.parse_args()

  with open(args.code_path, "r") as code_file:
    code = code_file.read()

  compiler = Compiler()
  #perminte escolher se sera gerada a img da arvore
  if args.tree:
    compiler.tree_to_png(code)

  #codigo para transpilar e gerar um arquivo em C
  if args.transpile:
    compiler.transpile(code)
    