
# IMPORTANTE: Importa apenas as funções auxiliares que serão usadas pela Eliminação de Gauss
from auxiliares import somar_linhas, trocar_linhas

# --- Algoritmo Principal: Eliminação de Gauss ---

def eliminacao_gauss(sistema):
    """
    Resolve um sistema linear pelo método de Eliminação de Gauss com Pivoteamento Parcial.
    """
    n = len(sistema)
    TOLERANCIA = 1e-10 
    sistema_copia = [linha[:] for linha in sistema] 

    # === Passo 1: Eliminação e Triangularização (Com Pivoteamento) ===
    for i in range(n):
        
        # 1. Pivoteamento Parcial
        max_valor = abs(sistema_copia[i][i])
        max_linha = i
        for k in range(i + 1, n):
            if abs(sistema_copia[k][i]) > max_valor:
                max_valor = abs(sistema_copia[k][i])
                max_linha = k

        if max_valor < TOLERANCIA:
            return "Erro: Sistema singular ou mal-condicionado (Pivô zero)."

        # Troca as linhas, usando a função de auxiliares.py
        if max_linha != i:
            trocar_linhas(sistema_copia, i, max_linha)

        # 2. Eliminação dos elementos abaixo do pivô
        for k in range(i + 1, n):
            fator = sistema_copia[k][i] / sistema_copia[i][i]
            
            # Operação Elementar, usando a função de auxiliares.py
            somar_linhas(sistema_copia, k, i, -fator)
            
            # CORREÇÃO CRÍTICA DE PRECISÃO:
            sistema_copia[k][i] = 0.0

    # === Passo 2: Substituição Retroativa ===
    
    if abs(sistema_copia[n-1][n-1]) < TOLERANCIA:
        return "Erro: Sistema indeterminado ou inconsistente (pivô final zero)."
        
    solucao = [0.0] * n

    for i in range(n - 1, -1, -1):
        soma = 0.0
        for j in range(i + 1, n):
            soma += sistema_copia[i][j] * solucao[j]

        solucao[i] = (sistema_copia[i][n] - soma) / sistema_copia[i][i]
        
    return solucao

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