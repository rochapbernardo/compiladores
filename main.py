import argparse
from compiler import Compiler

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog="Zen Compiler",
    description="A Simple Compiler"
  )
  parser.add_argument("code_path")
  parser.add_argument("--tree", action='store_true')
  args = parser.parse_args()

  with open(args.code_path, "r") as code_file:
    code = code_file.read()

  compiler = Compiler()
  if args.tree:
    compiler.tree_to_png(code)
    