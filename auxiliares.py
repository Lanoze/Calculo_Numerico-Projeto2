# auxiliares.py
from numexpr import evaluate
from math import e,pi
# --- Funções Auxiliares (OELs) --- 

def somar_linhas(sistema, linha_destino, linha_origem, escalar):
    """
    Implementa a operacao elementar de linha: L_destino = L_destino + escalar * L_origem
    """
    n_colunas = len(sistema[0])
    for j in range(n_colunas):
        sistema[linha_destino][j] = sistema[linha_destino][j] + escalar * sistema[linha_origem][j]
    return sistema

def multiplicar_linha_por_escalar(sistema, linha_i, escalar):
    """
    Implementa a OEL: L_i = escalar * L_i (Opcional, mas completa as OELs)
    """
    if escalar == 0:
        return "Erro: Não é permitido multiplicar linha por escalar zero."
    
    for j in range(len(sistema[0])):
        sistema[linha_i][j] *= escalar
    return sistema

def trocar_linhas(sistema: list[list[float]], linha_i: int, linha_j: int):
    """Implementa a OEL: Troca a linha i pela linha j no sistema."""
    sistema[linha_i], sistema[linha_j] = sistema[linha_j], sistema[linha_i]
    return sistema



def avaliar_expressao(func: str, valor_x: float) -> float:
    func = func.lower() #Torna todos os caracteres minúsculos
    variavel = {'x': valor_x}
    resultado = evaluate(func, local_dict=variavel, global_dict={}).item()
    return resultado


def formatar_expression(expression: str) -> str:
    sign = ('+', '-', '*', '/', ')')

    special_funcs = {'&':'arcsin','¨':'arccos','§':'arctan',
                     '@': 'exp', '$': 'sin', '#': 'cos', '%': 'tan','!': 'log'}  # Transformar isso num dicionário e usar num loop para substituir
    constantes = ('π', 'e')
    expression = expression.strip().lower()

    # Retorna os asteriscos duplos
    expression = expression.replace('^', '**')
    expression = expression.replace('pi', 'π')
    # expression = expression.replace('cosec','(1/sin)')
    # expression = expression.replace('csc', '(1/sin)')
    # expression = expression.replace('sec', '(1/cos)')
    expression = expression.replace('sen', 'sin')
    expression = expression.replace('ln', 'log')
    expression = expression.replace('tg', 'tan')
    expression = expression.replace('atan', 'arctan')
    expression = expression.replace('acos', 'arccos')
    expression = expression.replace('asin', 'arcsin')
    expression = expression.replace('e**', 'exp')

    for key, value in special_funcs.items():
        expression = expression.replace(value, key)
    #expression = expression.replace('exp', '@')

    expression = expression.replace('²', '**2')
    expression = expression.replace('³', '**3')

    # Remove espaços em branco
    expression = expression.replace(' ', '')
    final_expression = ""
    last_char = '?'
    for char in expression:
        if ((char.isalpha() and last_char.isdigit()) or (char.isdigit() and last_char.isalpha()) or (
                last_char == ')' and char not in sign) or (char in special_funcs and last_char.isalnum())
                or (char in constantes and last_char.isalnum()) or (last_char in constantes and char.isalnum())):
            final_expression += '*'
        final_expression += char
        last_char = char

    final_expression = final_expression.replace('e', str(e))

    for key, value in special_funcs.items():
        final_expression = final_expression.replace(key + 'x', key + '(x)')
        final_expression = final_expression.replace(key, value)

    final_expression = final_expression.replace('π', str(pi))
    print(final_expression)

    return final_expression

if __name__ == "__main__":
    # char = '§'
    # print(f"'{char}' é alfa: {char.isalpha()}\n'{char}' é num: {char.isdigit()}")
    print(evaluate("arctan(3)"))