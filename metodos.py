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