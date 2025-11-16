# Projeto 2 – Cálculo Numérico

Aplicação em Python desenvolvida para a disciplina de Cálculo Numérico da
Universidade Federal do Vale do São Francisco (UNIVASF), referente ao **Projeto 2**.

O objetivo do programa é resolver problemas clássicos de engenharia usando métodos
numéricos, organizados nos quatro tópicos do projeto:

1. Sistemas de equações lineares – métodos diretos  
2. Sistemas de equações lineares – métodos iterativos (Gauss-Seidel)  
3. Interpolação polinomial e ajuste por mínimos quadrados  
4. Integração numérica (Regra do Trapézio e Regra de Simpson repetidas)  

O código foi estruturado para permitir **reutilização**: com a mesma base,
é possível resolver outros problemas do mesmo tipo apenas trocando os dados de entrada.

---

## Funcionalidades

- Resolução de sistemas lineares por métodos diretos (ex.: eliminação de Gauss, etc.).
- Resolução de sistemas lineares por métodos iterativos (Gauss-Seidel).
- Interpolação polinomial (formas de Lagrange/Newton) e regressão por mínimos quadrados.
- Integração numérica usando Regra do Trapézio e Regra de Simpson, na forma repetida.
- Organização modular do código, facilitando a inclusão de novos problemas.
- Possibilidade de reutilizar as rotinas numéricas com diferentes conjuntos de dados.

---

## Estrutura do Projeto


main.py: coordena a execução, interação com o usuário e chamada das funções dos outros módulos.

metodos.py: concentra as rotinas de Cálculo Numérico (sistemas lineares, interpolação, integração, etc.).

auxiliares.py: contém funções auxiliares para leitura/tratamento de dados, mensagens de erro e suporte geral.

MyWidgets.py: reúne os componentes de interface utilizados para facilitar a entrada de dados e a exibição de resultados.

Requisitos

Python 3.10+ (recomendado)

Bibliotecas padrão da linguagem e demais dependências listadas no projeto

Se houver um arquivo requirements.txt, instale as dependências com:

pip install -r requirements.txt

Como executar

Clone este repositório:

git clone https://github.com/Lanoze/Calculo_Numerico-Projeto2.git
cd Calculo_Numerico-Projeto2


(Opcional, mas recomendado) Crie e ative um ambiente virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate


Instale as dependências (se houver):

pip install -r requirements.txt


Execute o programa:

python main.py

Uso

Ao executar main.py, o usuário tem acesso às funcionalidades do projeto.

Cada rotina numérica foi escrita para aceitar novos conjuntos de dados, permitindo
reutilizar o código com problemas de mesma natureza (mesma estrutura de equações, tabelas de pontos, etc.).

Os dados podem ser ajustados diretamente no código ou, dependendo da implementação,
informados via interface/entrada interativa.

Adaptação aos problemas da disciplina

Este projeto foi pensado para ser usado com os problemas propostos no enunciado da
atividade complementar da disciplina, tais como:

Sistemas de produção (mistura de materiais) modelados por sistemas lineares.

Circuitos elétricos e treliças resolvidos por métodos iterativos.

Dados experimentais para interpolação e ajuste de curvas.

Cálculo de áreas em perfis de rios, lagos e navios via integração numérica.

Basta ajustar as matrizes, vetores e tabelas de dados nos pontos apropriados do
código para aplicar as rotinas já implementadas.
