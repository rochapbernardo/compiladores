# Uso

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py tests/main.zen --transpile --tree
```

## Compilar e rodar o código C gerado:

```sh
gcc code.c -o code
./code
```

# Exemplo

## Código criado (de acordo com a gramática)
```
func main()-> void {
  func teste(int a) -> int {
    return a
  }
  func teste2(int z) -> int {
    return z
  }
  float y = 3.14
  str message = "Hello"
  bool test = true
  bool test1 = false
  int[] quant_pessoas
  int[5] vagas 
  str[3] nomes = {"José", "João", "Maria"}
  int idade = 10
  int x = 3
  teste(1)
  teste2(1)
  if (idade != 18) {
    return true
  } elif (idade >= 16) {
      return false
  } else {
      return false
  }
  for (int i = 0; i < 10; i++) {
    int x = 1 + i
  }
  while (x < 5) {
    x = x + 1
  }
}
``` 

## Código transpilado (C)
```c
#include <stdbool.h>

int teste2(int z) {
    return z;
}

int teste(int a) {
    return a;
}

int main() {
    float y = 3.14;
    const char* message = "Hello";
    bool test = true;
    bool test1 = false;
    int quant_pessoas[10];
    int vagas[5];
    char* nomes[3] = { "José", "João", "Maria" };
    int idade = 10;
    int x = 3;
    teste(1);
    teste2(1);
    if (idade != 18) {
        return true;
    } else if (idade >= 16) {
        return false;
    } else {
        return false;
    }
    for (int i = 0; i < 10; i++) {
        int x = 1 + i;
    }
    while (x < 5) {
        x = x + 1;
    }
    return 0;
}
``` 

# Alterações

## TreeIndenter

- Método declarado de acordo com as definições de property da classe Indenter.

## Compiler

- Faz uso da variável `img_path` no método `tree_to_png`.

## CodeTranspiler

- Como os imports variam de acordo com o código a ser transpilado, a transpilação de código e dos imports são processadas separadamente e reunidas ao final.
