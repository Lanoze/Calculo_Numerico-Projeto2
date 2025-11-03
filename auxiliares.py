# auxiliares.py

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

def trocar_linhas(sistema, linha_i, linha_j):
    """Implementa a OEL: Troca a linha i pela linha j no sistema."""
    sistema[linha_i], sistema[linha_j] = sistema[linha_j], sistema[linha_i]
    return sistema