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
