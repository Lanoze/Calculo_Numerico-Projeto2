
# IMPORTANTE: Importa apenas as funções auxiliares que serão usadas pela Eliminação de Gauss
from auxiliares import somar_linhas, trocar_linhas, multiplicar_linha_por_escalar
from copy import deepcopy


# --- Algoritmo Principal: Eliminação de Gauss ---

def eliminacao_gauss(sistema: list[list[float]]):
    sistema_passo_a_passo = []
    sistema_passo_a_passo.append(deepcopy(sistema))
    print("Sistema inicial:")
    print(sistema)
    for index in range(len(sistema)-1):
        pivo = sistema[index][index]
        linha_maior_pivo = index
        for index2 in range(index+1,len(sistema)):
            if abs(sistema[index2][index]) > abs(pivo):
                pivo = sistema[index2][index]
                linha_maior_pivo = index2
        trocar_linhas(sistema, linha_maior_pivo, index)

        for index2 in range(index+1,len(sistema)):
            m = -sistema[index2][index]/pivo
            somar_linhas(sistema, index2, index, m)
        sistema_passo_a_passo.append(deepcopy(sistema))
        print(f"Sistema no índice {index}:")
        print(sistema)
    #O sistema já está completo, agora é só pegar os resultados
    resultado = []
    for i, elemento in enumerate(reversed(sistema)):
        equacao_reversa = elemento[::-1]
        soma_numerador = equacao_reversa[0]
        for j in range(1, i+1):
            soma_numerador -= (equacao_reversa[j] * resultado[j-1])
        resultado.append(soma_numerador/equacao_reversa[1+i])
    resultado.reverse()
    return resultado

def eliminacao_jordan(sistema: list[list[float]]):
    sistema_passo_a_passo = []
    sistema_passo_a_passo.append(deepcopy(sistema))
    print("Sistema inicial:")
    print(sistema)
    #Diferente do de Gauss, é necessário ir até a última linha, para eliminar os elementos acima do pivô
    for index in range(len(sistema)):
        pivo = sistema[index][index]
        linha_maior_pivo = index
        for index2 in range(index + 1, len(sistema)):
            if abs(sistema[index2][index]) > abs(pivo):
                pivo = sistema[index2][index]
                linha_maior_pivo = index2

        # Troca a linha pelo maior pivô, para realizar o maior pivoteamento parcial
        trocar_linhas(sistema, linha_maior_pivo, index)

        #Zera elementos abaixo do pivô
        for index2 in range(index + 1, len(sistema)):
            m = -sistema[index2][index] / pivo
            somar_linhas(sistema, index2, index, m)
        #Zera elementos acima do pivô
        for index2 in range(index-1, -1, -1):
            m = -sistema[index2][index] / pivo
            somar_linhas(sistema, index2, index, m)
        sistema_passo_a_passo.append(deepcopy(sistema))
        print(f"Sistema no índice {index}:")
        print(sistema)
    # O sistema já está completo, agora é só pegar os resultados
    resultado = []
    for index in range(len(sistema)):
        divisor = sistema[index][index]
        multiplicar_linha_por_escalar(sistema, index, 1/divisor)
        resultado.append(sistema[index][-1])
    sistema_passo_a_passo.append(deepcopy(sistema))
    print("Sistema como matriz identidade:")
    print(sistema)
    return resultado

# ----- implementar métudo de Gauss-Seidel -----#

def gauss_seidel(sistema, max_iter=100, tol=1e-6,valores_iniciais=[]):
    if valores_iniciais:
        solucao = valores_iniciais #Caso o usuário tenha digitado
    else:
        solucao = [0]*len(sistema) #Caso o usuário não tenha digitado usa tudo 0
    solucao_passo_a_passo = []
    solucao_passo_a_passo.append(solucao.copy())

    #todo organizar as diagonais para verificar se tem alguma nula

    iteration = 1
    while True:
        #Equação de cada variável
        for i in range(len(sistema)):
            equacao = sistema[i]
            soma_numerador = equacao[-1]
            for j in range(len(equacao) - 1):
                if j != i:
                    soma_numerador -= (equacao[j] * solucao[j])
            solucao[i] = soma_numerador / equacao[i]
        print(f"Solução na iteração {iteration}:")
        print(solucao)
        solucao_passo_a_passo.append(solucao.copy())
        #Cálculo para achar a diferença relativa
        maior_diferenca = abs(solucao_passo_a_passo[iteration][0] - solucao_passo_a_passo[iteration-1][0])
        maior_variavel = abs(solucao_passo_a_passo[iteration][0])
        for j in range(1, len(solucao_passo_a_passo[0])):
            if abs(solucao_passo_a_passo[iteration][j] - solucao_passo_a_passo[iteration-1][j]) > maior_diferenca:
                maior_diferenca = abs(solucao_passo_a_passo[iteration][j] - solucao_passo_a_passo[iteration-1][j])
            if abs(solucao_passo_a_passo[iteration][j]) > maior_variavel:
                maior_variavel = abs(solucao_passo_a_passo[iteration][j])
        print(f"Diferença relativa foi {maior_diferenca/maior_variavel}")
        iteration += 1
        #Critério de saída
        if iteration > max_iter or maior_diferenca/maior_variavel <= tol:
            break

    if iteration > max_iter:
        return "Sistema não convergiu em iterações suficientes"
    else:
        print("Solução passo a passo de Gauss-Seidel:")
        print(solucao_passo_a_passo)
        return solucao

# ---- Implementando a Interpolação de Lagrange ---- #

def interpolacao_lagrange(X, Y, x_interpolar):
    """
    Calcula o valor interpolado P(x_interpolar) usando o método de Lagrange.
    """
    n = len(X)
    
    if n != len(Y):
        return "Erro: As listas de X e Y devem ter o mesmo número de pontos."

    P_x = 0.0
    
    for i in range(n):
        L_i_x = 1.0
        
        for j in range(n):
            if i != j:
                denominador = X[i] - X[j]
                if denominador == 0:
                    return f"Erro: Coordenada X repetida em X[{i}] e X[{j}]. Não é possível interpolar."
                
                L_i_x *= (x_interpolar - X[j]) / denominador
        
        P_x += L_i_x * Y[i]
        
    return P_x


# ---- Implementando a Interpolação de Newton (diferenças divididas) ---- #

def interpolacao_newton(X, Y, x_interpolar):
    """
    Calcula o valor interpolado P(x_interpolar) usando o método de Newton
    (Diferenças Divididas).
    """
    n = len(X)
    
    if n != len(Y):
        return "Erro: As listas de X e Y devem ter o mesmo número de pontos."

    # 1. Cria a Tabela de Diferenças Divididas (coeficientes)
    coeficientes = list(Y) 
    
    try:
        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                denominador = X[i] - X[i - j]
                if denominador == 0:
                    return f"Erro: Coordenada X repetida em X[{i}] e X[{i - j}]. Não é possível interpolar."

                coeficientes[i] = (coeficientes[i] - coeficientes[i - 1]) / denominador
                
    except Exception as e:
        return f"Erro no cálculo das Diferenças Divididas: {e}"

    # 2. Avaliação do Polinômio de Newton
    P_x = coeficientes[0]
    termo_produtorio = 1.0

    for i in range(1, n):
        termo_produtorio *= (x_interpolar - X[i - 1])
        P_x += coeficientes[i] * termo_produtorio
        
    return P_x

# Implementando Integração Numérica: Trapézio e Simpson Repetidas #

def integracao_trapezio(y_pontos: list[float],h: float) -> float:
   primeiro_termo = y_pontos.pop(0)
   ultimo_termo = y_pontos.pop()
   soma_intermediaria = 0
   for y in y_pontos:
       soma_intermediaria += y
   soma_intermediaria *= 2
   resultado = (h/2)*(primeiro_termo + soma_intermediaria + ultimo_termo)
   return resultado

def integracao_simpson(y_pontos: list[float],h: float) -> float:
    primeiro_termo = y_pontos.pop(0)
    ultimo_termo = y_pontos.pop()
    soma_par = 0
    soma_impar = 0
    ponto_impar = True
    for y in y_pontos:
        if ponto_impar:
            soma_impar += y
        else:
            soma_par += y
        ponto_impar = not ponto_impar
    soma_impar *= 4
    soma_par *= 2
    resultado = (h/3)*(primeiro_termo + soma_par + soma_impar + ultimo_termo)
    return resultado