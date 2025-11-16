
# IMPORTANTE: Importa apenas as funções auxiliares que serão usadas pela Eliminação de Gauss
from auxiliares import somar_linhas, trocar_linhas

# --- Algoritmo Principal: Eliminação de Gauss ---

def eliminacao_gauss(sistema: list[list[float]]):
    # if all(c == 0 for c in sistema[-1]):
    #     return "Erro, linha totalmente nula, impossível de aplicar o método de Gauss"
    sistema_passo_a_passo = []
    sistema_passo_a_passo.append(sistema)
    for index in range(len(sistema)-1):
        # if all(c == 0 for c in sistema[index]):
        #     return "Erro, linha totalmente nula, impossível de aplicar o método de Gauss"
        # Procura o maior pivô absoluto e sua linha
        pivo = sistema[index][index]
        linha_maior_pivo = index
        for index2 in range(index+1,len(sistema)):
            if abs(sistema[index2][index]) > abs(pivo):
                pivo = sistema[index2][index]
                linha_maior_pivo = index2
        #Deixa o try except cuidar disso
        # if pivo == 0:
        #     return "Erro, coluna totalmente nula, impossível de aplicar o método de Gauss"

        #Troca a linha pelo maior pivô, para realizar o maior pivoteamento parcial
        trocar_linhas(sistema, linha_maior_pivo, index)
        for index2 in range(index+1,len(sistema)):
            m = -sistema[index2][index]/pivo
            somar_linhas(sistema, index2, index, m)
            # if all(c == 0 for c in sistema[index2]):
            #     return "Erro, equações linearmente dependentes, o sistema não tem solução única"
        sistema_passo_a_passo.append(sistema)
        print(f"Sistema no índice {index}:")
        print(sistema)
    #O sistema já está completo, agora é só pegar os resultados
    resultado = []
    #debug_variable = len(sistema)
    for i, elemento in enumerate(reversed(sistema)):
        equacao_reversa = elemento[::-1]
        #print(f"Índice reverso {i}: {equacao_reversa}")
        soma_numerador = equacao_reversa[0]
        for j in range(1, i+1):
            soma_numerador -= (equacao_reversa[j] * resultado[j-1])
        resultado.append(soma_numerador/equacao_reversa[1+i])
        # print(f"X{debug_variable} = {resultado[i]}")
        # debug_variable -= 1
    #Os resultados vão de X1 até Xn
    resultado.reverse()
    #print(f"Ao fim do processo: {resultado}")
    return resultado



        # # O elemento de maior valor absoluto passa a ser o pivô da linha atual (especificada por "index")
        # trocar_linhas(sistema,index,indice_maior_pivo)
        # pivo = sistema[index][index] #O pivo sempre esta na diagonal principal
        # for j in range(index+1, len(sistema)):
        #

# ----- implementar método de Gauss-Seidel -----#

def gauss_seidel(sistema, max_iter=100, tol=1e-6):

    n = len(sistema)
    TOLERANCIA_ZERO = 1e-12

    A = [linha[:] for linha in sistema]
    x = [0.0] * n

    for i in range(n):
        if abs(A[i][i]) < TOLERANCIA_ZERO:
            return "Erro: elemento diagonal zero. Método de Gauss-Seidel não pode ser aplicado."

    for _ in range(max_iter):
        x_ant = x[:] 
        for i in range(n):
            soma1 = 0.0
            for j in range(i):
                soma1 += A[i][j] * x[j]

            soma2 = 0.0
            for j in range(i + 1, n):
                soma2 += A[i][j] * x_ant[j]

            x[i] = (A[i][n] - soma1 - soma2) / A[i][i]

        erro = max(abs(x[i] - x_ant[i]) for i in range(n))
        if erro < tol:
            return x

    return "Aviso: método de Gauss-Seidel não convergiu dentro do número máximo de iterações."


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