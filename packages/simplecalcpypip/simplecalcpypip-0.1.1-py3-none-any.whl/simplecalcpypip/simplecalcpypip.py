def soma(a, b):
    """
    Retorna a soma de dois números.

    Parâmetros:
    - a (float ou int): O primeiro número.
    - b (float ou int): O segundo número.

    Retorna:
    - float ou int: A soma de a e b.
    """
    return a + b

def subtracao(a, b):
    """
    Retorna a diferença entre dois números.

    Parâmetros:
    - a (float ou int): O número do qual será subtraído.
    - b (float ou int): O número que será subtraído.

    Retorna:
    - float ou int: A diferença entre a e b.
    """
    return a - b

def multiplicacao(a, b):
    """
    Retorna o produto de dois números.

    Parâmetros:
    - a (float ou int): O primeiro fator.
    - b (float ou int): O segundo fator.

    Retorna:
    - float ou int: O produto de a e b.
    """
    return a * b

def divisao(a, b):
    """
    Realiza a divisão entre dois números.

    Parâmetros:
    - a (float ou int): O numerador.
    - b (float ou int): O denominador.

    Retorna:
    - float ou str: O resultado da divisão (ou mensagem de erro se b for zero).
    """
    if b != 0:
        return a / b
    else:
        return "Erro: divisão por zero"

def potencia(a, b):
    """
    Retorna a potência de a elevado a b.

    Parâmetros:
    - a (float ou int): A base.
    - b (float ou int): O expoente.

    Retorna:
    - float ou int: a elevado a b.
    """
    return a ** b

def raiz_quadrada(a):
    """
    Retorna a raiz quadrada de um número.

    Parâmetros:
    - a (float ou int): O número do qual a raiz quadrada será calculada.

    Retorna:
    - float ou str: A raiz quadrada de a (ou mensagem de erro se a for negativo).
    """
    if a >= 0:
        return a ** 0.5
    else:
        return "Erro: raiz quadrada de número negativo"

# Exemplos de uso:
# num1 = 10
# num2 = 5

# print(f"Soma: {soma(num1, num2)}")
# print(f"Subtração: {subtracao(num1, num2)}")
# print(f"Multiplicação: {multiplicacao(num1, num2)}")
# print(f"Divisão: {divisao(num1, num2)}")
# print(f"Potência: {potencia(num1, num2)}")
# print(f"Raiz Quadrada de {num1}: {raiz_quadrada(num1)}")
