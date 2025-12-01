# Projeto 2 – Cálculo Numérico

Aplicação em Python desenvolvida para a disciplina de Cálculo Numérico da
Universidade Federal do Vale do São Francisco (UNIVASF), referente ao **Projeto 2**.

O objetivo do programa é resolver problemas clássicos de engenharia usando métodos
numéricos, organizados nos quatro tópicos do projeto:

1. Sistemas de equações lineares – métodos diretos  
2. Sistemas de equações lineares – métodos iterativos (Gauss-Seidel)  
3. Interpolação polinomial 
4. Integração numérica (Regra do Trapézio e Regra de Simpson repetidas)  

O código foi estruturado para permitir **reutilização**: com a mesma base,
é possível resolver outros problemas do mesmo tipo apenas trocando os dados de entrada.

---

## Funcionalidades

- Resolução de sistemas lineares por métodos diretos (ex.: eliminação de Gauss, etc.).
- Resolução de sistemas lineares por métodos iterativos (Gauss-Seidel).
- Interpolação polinomial (formas de Lagrange/Newton).
- Integração numérica usando Regra do Trapézio e Regra de Simpson, na forma repetida.
- Organização modular do código, facilitando a inclusão de novos problemas.
- Possibilidade de reutilizar as rotinas numéricas com diferentes conjuntos de dados.
- Botão settar para automaticamente colocar os dados do problema resolvido pela equipe

---

## Estrutura do Projeto

```text
Calculo_Numerico-Projeto2/
├── main.py          # Ponto de entrada da aplicação
├── metodos.py       # Implementação dos métodos numéricos
├── auxiliares.py    # Funções de apoio (validação, formatação, etc.)
├── MyWidgets.py     # Componentes de interface (widgets) utilizados no programa
└── ...              # Outros arquivos e recursos auxiliares

main.py: coordena a execução, interação com o usuário e chamada das funções dos outros módulos.

metodos.py: concentra as rotinas de Cálculo Numérico (sistemas lineares, interpolação, integração, etc.).

auxiliares.py: contém funções auxiliares para leitura/tratamento de dados, mensagens de erro e suporte geral.

MyWidgets.py: reúne os componentes de interface utilizados para facilitar a entrada de dados e a exibição de resultados.
