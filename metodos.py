# ----- implementar eliminação de Gauss. -----#

# --- Funções Auxiliares (OELs) --- 

def somar_linhas(sistema, linha_destino, linha_origem, escalar):
    """
    Implementa a operacao elementar de linha: L_destino = L_destino + escalar * L_origem
    Esta função também cobre a OEL de multiplicar linha por escalar, se linha_origem for 
    zero e o escalar não for -1. No entanto, sua função primária é a soma.
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

def trocar_linhas(sistema, linha_i, linha_j):
    """Implementa a OEL: Troca a linha i pela linha j no sistema."""
    sistema[linha_i], sistema[linha_j] = sistema[linha_j], sistema[linha_i]
    return sistema

# --- Algoritmo Principal: Eliminação de Gauss ---

def eliminacao_gauss(sistema):
    """
    Resolve um sistema linear pelo método de Eliminação de Gauss com Pivoteamento Parcial.
    """
    n = len(sistema)
    # Tolerância crucial para lidar com números decimais e erros de ponto flutuante
    TOLERANCIA = 1e-10 

    # Cria uma cópia profunda para não modificar o sistema original
    sistema_copia = [linha[:] for linha in sistema] 

    # === Passo 1: Eliminação e Triangularização (Com Pivoteamento) ===
    for i in range(n):
        
        # 1. Pivoteamento Parcial (Para máxima estabilidade numérica)
        max_valor = abs(sistema_copia[i][i])
        max_linha = i
        for k in range(i + 1, n):
            if abs(sistema_copia[k][i]) > max_valor:
                max_valor = abs(sistema_copia[k][i])
                max_linha = k

        # Verifica se o pivô é zero ou muito próximo de zero
        if max_valor < TOLERANCIA:
            return "Erro: Sistema singular ou mal-condicionado (Pivô zero)."

        # Troca as linhas, se necessário (OEL 1)
        if max_linha != i:
            trocar_linhas(sistema_copia, i, max_linha)

        # 2. Eliminação dos elementos abaixo do pivô
        for k in range(i + 1, n):
            # Calcula o fator de eliminação (multiplicador)
            fator = sistema_copia[k][i] / sistema_copia[i][i]
            
            # Operação Elementar (OEL 2/4): L_k = L_k - fator * L_i
            # O fator é passado como negativo para subtrair
            somar_linhas(sistema_copia, k, i, -fator)
            
            # CORREÇÃO CRÍTICA DE PRECISÃO: Garante que o elemento que deveria ser zero seja 0.0
            # Isso elimina os resíduos de 1e-17 que causam erro no resultado final
            sistema_copia[k][i] = 0.0

    # === Passo 2: Substituição Retroativa ===
    
    # Verifica o último pivô
    if abs(sistema_copia[n-1][n-1]) < TOLERANCIA:
         return "Erro: Sistema indeterminado ou inconsistente (pivô final zero)."
        
    solucao = [0.0] * n

    for i in range(n - 1, -1, -1):
        soma = 0.0
        # Soma dos termos já calculados: sum(a_ij * x_j)
        for j in range(i + 1, n):
            soma += sistema_copia[i][j] * solucao[j]

        # Calcula a solução: x_i = (b_i - soma) / a_ii
        # A divisão por a_ii é equivalente a multiplicar a linha por 1/a_ii (OEL 2)
        solucao[i] = (sistema_copia[i][n] - soma) / sistema_copia[i][i]
        
    return solucao

# ----- implementar método de Gauss-Seidel -----#

def gauss_seidel(sistema, max_iter=100, tol=1e-6):

    n = len(sistema)
    TOLERANCIA_ZERO = 1e-12

    # Faz uma cópia para trabalhar
    A = [linha[:] for linha in sistema]

    # Vetor inicial (pode ser tudo zero)
    x = [0.0] * n

    # Verificação rápida de zeros na diagonal
    for i in range(n):
        if abs(A[i][i]) < TOLERANCIA_ZERO:
            return "Erro: elemento diagonal zero. Método de Gauss-Seidel não pode ser aplicado."

    for _ in range(max_iter):
        x_ant = x[:]  # guarda iteração anterior
        for i in range(n):
            soma1 = 0.0  # usa valores novos (j < i)
            for j in range(i):
                soma1 += A[i][j] * x[j]

            soma2 = 0.0  # usa valores antigos (j > i)
            for j in range(i + 1, n):
                soma2 += A[i][j] * x_ant[j]

            x[i] = (A[i][n] - soma1 - soma2) / A[i][i]

        # critério de parada: norma infinito da diferença
        erro = max(abs(x[i] - x_ant[i]) for i in range(n))
        if erro < tol:
            return x

    # Se não convergiu
    return "Aviso: método de Gauss-Seidel não convergiu dentro do número máximo de iterações."


# ---- Implementando a interpolação de Lagrange ---- #


def interpolacao_lagrange(X, Y, x_interpolar):
    """
    Calcula o valor interpolado P(x_interpolar) usando o método de Lagrange.
    
    Args:
        X (list): Lista de coordenadas x dos pontos de dados.
        Y (list): Lista de coordenadas y dos pontos de dados.
        x_interpolar (float): O ponto x no qual se deseja interpolar.

    Returns:
        float or str: O valor interpolado P(x_interpolar), ou uma string de erro.
    """
    n = len(X)
    
    if n != len(Y):
        return "Erro: As listas de X e Y devem ter o mesmo número de pontos."

    P_x = 0.0 # O valor final do polinômio P(x)
    
    # Soma dos termos y_i * L_i(x)
    for i in range(n):
        L_i_x = 1.0 # Inicializa o Polinômio Base de Lagrange L_i(x)
        
        # Cálculo do produtório de L_i(x)
        for j in range(n):
            if i != j:
                denominador = X[i] - X[j]
                if denominador == 0:
                    return f"Erro: Coordenada X repetida em X[{i}] e X[{j}]. Não é possível interpolar."
                
                # Multiplica os termos: (x - x_j) / (x_i - x_j)
                L_i_x *= (x_interpolar - X[j]) / denominador
        
        # Adiciona o termo ao polinômio total: L_i(x) * y_i
        P_x += L_i_x * Y[i]
        
    return P_x


# ---- Implemenatndo a interpolação de Newton (diferenças divididas) ---- #

def interpolacao_newton(X, Y, x_interpolar):
    """
    Calcula o valor interpolado P(x_interpolar) usando o método de Newton
    (Diferenças Divididas).
    
    Args:
        X (list): Lista de coordenadas x dos pontos de dados.
        Y (list): Lista de coordenadas y dos pontos de dados.
        x_interpolar (float): O ponto x no qual se deseja interpolar.

    Returns:
        float or str: O valor interpolado P(x_interpolar), ou uma string de erro.
    """
    n = len(X)
    
    if n != len(Y):
        return "Erro: As listas de X e Y devem ter o mesmo número de pontos."

    # 1. Cria a Tabela de Diferenças Divididas (coeficientes)
    coeficientes = list(Y) 
    
    try:
        for j in range(1, n): # Colunas da tabela
            for i in range(n - 1, j - 1, -1): # Linhas para calcular os novos termos
                denominador = X[i] - X[i - j]
                if denominador == 0:
                    return f"Erro: Coordenada X repetida em X[{i}] e X[{i - j}]. Não é possível interpolar."

                # Cálculo da Diferença Dividida e atualização
                coeficientes[i] = (coeficientes[i] - coeficientes[i - 1]) / denominador
                
    except Exception as e:
        return f"Erro no cálculo das Diferenças Divididas: {e}"

    # 2. Avaliação do Polinômio de Newton (P(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1) + ...)
    P_x = coeficientes[0] # b0 = f[x0]
    termo_produtorio = 1.0

    for i in range(1, n):
        # Atualiza o produtório: (x - x0)...(x - x_i-1)
        termo_produtorio *= (x_interpolar - X[i - 1])
        
        # Adiciona o próximo termo: b_i * (produtório)
        P_x += coeficientes[i] * termo_produtorio
        
    return P_x