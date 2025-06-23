# Uso

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py examples/main_example.zen --transpile --tree
```

# Divergências

## TreeIndenter

- Método declarado de acordo com as definições de property da classe Indenter.

## Compiler

- Faz uso da variável `img_path` no método `tree_to_png`.

## CodeTranspiler

- Como os imports variam de acordo com o código a ser transpilado, a transpilação de código e dos imports são processadas separadamente e reunidas ao final.
