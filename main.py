from metodos import eliminacao_gauss # Importa o método de cálculo.
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout,QMessageBox,QComboBox
)
from PySide6.QtCore import Qt

#Talvez devesse criar um arquivo só pra funções auxiliares
# def exibir_sistema(sistema):
#     print('')
#     for linha in range(len(sistema)):
#         for coluna in range(len(sistema[0])-1):
#             valor_atual = sistema[linha][coluna]
#             print(f"{valor_atual}*X{coluna}",end='  ')
#         print(f"= {sistema[linha][len(sistema[0])-1]}")

class MatrixApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solucionador de Sistema Linear")
        self.setGeometry(100, 100, 400, 300)

        # ### MUDANÇA FUNCIONAL: Inicializa como 3x3 + 1 para labels/coluna B
        self.num_rows = 4 #O número de linhas é igual ao de colunas porque tem os labels (Variáveis)
        self.num_cols = 4 #Geralmente num_cols seria igual a num_linhas+1
        self.MAX_VARIABLES = 10 #O número máximo de colunas é esse número + 1 (é uma constante)

        # 1. Nosso modelo de dados para armazenar os valores (começa vazio), não armazena as variáveis
        self.matrix_data = []
        # Manter uma referência aos widgets para fácil acesso
        self.matrix_widgets = []

        self.setup_ui()
        # Cria a matriz inicial (agora preenche self.matrix_data com "0")
        self.rebuild_matrix_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self) #Empilha verticalmente os elementos

        label_matrix_a = QLabel("Solucionador de sistema linear")
        label_matrix_a.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_matrix_a)

        self.matrix_grid_layout = QGridLayout()
        main_layout.addLayout(self.matrix_grid_layout,stretch=1) #stretch=1 deixa a matriz mais distante do label

        control_buttons_layout = QHBoxLayout() #Os botões aparecem horizontalmente
        control_buttons_layout.addStretch(1) #Adiciona inicialmente um espaço antes, e depois um no final

        btn_add = QPushButton("+")
        btn_add.setFixedSize(40, 40)
        btn_add.setObjectName("Aumentar")
        btn_add.clicked.connect(self.increase_dimensions)
        control_buttons_layout.addWidget(btn_add)

        btn_subtract = QPushButton("-")
        btn_subtract.setFixedSize(40, 40)
        btn_subtract.setObjectName("Diminuir")
        btn_subtract.clicked.connect(self.decrease_dimensions)
        control_buttons_layout.addWidget(btn_subtract)

        control_buttons_layout.addStretch(1) #Ajuda a centralizar os botões, é parecido com um spacer() do swift
        main_layout.addLayout(control_buttons_layout)

        # ### MUDANÇA FUNCIONAL: Remove 'self' para corrigir o aviso QLayout
        resize_row = QHBoxLayout()
        resize_row.addStretch(1)
        resize_button = QPushButton("Resize")
        resize_button.clicked.connect(self.resize_matrix)
        self.resize_input = QLineEdit(self)
        self.resize_input.setPlaceholderText("Número de variáveis")
        resize_row.addWidget(resize_button)
        resize_row.addWidget(self.resize_input)
        resize_row.addStretch(1)

        # ### MUDANÇA FUNCIONAL: Remove 'self' para corrigir o aviso QLayout
        calculo_row = QHBoxLayout()
        calculo_row.addStretch(1)
        self.menu_opcoes = QComboBox()
        self.menu_opcoes.addItems(["Gauss","Jordan","LU","Jacobi","Gauss-Siedel"])
        calculo_botao = QPushButton("Calcular")
        calculo_botao.clicked.connect(self.calcular)
        calculo_row.addWidget(self.menu_opcoes)
        calculo_row.addWidget(calculo_botao)
        calculo_row.addStretch(1)

        main_layout.addStretch(1)
        main_layout.addLayout(resize_row)
        main_layout.addLayout(calculo_row)

        main_layout.addStretch(1)
        # Css pra mudar a aparência (QSS sendo mais específico)
        self.setStyleSheet('''
                            QPushButton{
                            font-size: 15px;
                            background-color: #5B92A8
                            }
                            QPushButton:hover{
                            background-color: #4D7C94
                            }
                            QPushButton:focus {
                            outline: none;
                            }
    
                            QPushButton#Aumentar{
                            font-size: 30px;
                            background-color: #4CAF50; /* Verde */
                            }
                            QPushButton#Aumentar:hover{
                            background-color: #429945; /* Verde mais escuro */
                            }
    
                            QPushButton#Diminuir{
                            font-size: 30px;
                            background-color: #f44336
                            }
                            QPushButton#Diminuir:hover{
                            background-color: #C23129
                            }
    
                            QComboBox {
                            border: 1px solid #555;      /* Borda cinza escura */
                            border-radius: 5px;          /* Cantos arredondados */
                            padding: 5px 10px;           /* Espaçamento interno (vertical, horizontal) */
                            background-color: #5B92A8;   /* Fundo azul */
                            color: black;                /* Texto preto */
                            font-size: 14px;
                            min-width: 95px;
                            }
                            QComboBox:focus {
                            outline: none;
                            }
    
                            MatrixApp{
                            background-color: #A6C0ED
                            }
                            QMessageBox{
                            background-color: #A6C0ED
                            }
                    ''')

    def clear_layout(self, layout):
        """Limpa todos os widgets de um layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): #Só limpla widgets a parte desse if
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout()) #Limpa recursivamente
            elif item.spacerItem():
                pass
            else:
                print("Caso inesperado")
                exit(1)

    def sync_data_from_ui(self):
        # Salva os valores da UI (QLineEdit) no modelo de dados (self.matrix_data).
        if not self.matrix_widgets:  # Se a UI ainda não foi criada
            print("Matrix_widgets nao foi criada")
            return

        # Atualiza self.matrix_data com os valores dos QLineEdit
        for row in range(len(self.matrix_widgets)):
            for col in range(len(self.matrix_widgets[row])):
                self.matrix_data[row][col] = self.matrix_widgets[row][col].text()
        print("Matrix data agora eh:")
        print(self.matrix_data)

    #Preciso atualizar isso pra aparecer X0,X1 etc no topo da matriz
    def rebuild_matrix_ui(self):
        """Limpa e reconstrói a UI da matriz com base nos dados e dimensões atuais."""

        # --- 1. Atualiza o Modelo de Dados ---
        # Cria uma nova matriz de dados (lista de listas) com as novas dimensões
        new_data = [["0"] * self.num_cols for _ in range(self.num_rows-1)]

        # ### LINHA REMOVIDA: print("\nNew data eh:")
        # ### LINHA REMOVIDA: print(new_data)
        #row_X_label = [] #Uma lista de QLabel


        # Copia os valores antigos da matriz de dados (se existirem)
        if self.matrix_data:
            # Pega o menor tamanho entre o antigo e o novo para evitar erros
            rows_to_copy = min(len(self.matrix_data), self.num_rows-1) #Retira 1 porque a 1ª é apenas para variáveis
            cols_to_copy = min(len(self.matrix_data[0]), self.num_cols) #len(self.matrix_data[0]) é o número de colunas
            # ### LINHA REMOVIDA: print(f"\nRows to copy eh {rows_to_copy}, cols to copy eh {cols_to_copy}, Matrix data antes eh:")
            # ### LINHA REMOVIDA: print(self.matrix_data)
            for row in range(rows_to_copy):
                for col in range(cols_to_copy):
                    new_data[row][col] = self.matrix_data[row][col]
        #matrix_data é uma matriz de strings
        #new_data.pop(0)
        self.matrix_data = new_data  # O modelo de dados agora está atualizado

        # ### LINHA REMOVIDA: print("\nself.matrix_data eh:")
        # ### LINHA REMOVIDA: print(self.matrix_data)
        
        # --- 2. Limpa a UI Antiga ---
        self.clear_layout(self.matrix_grid_layout)
        self.matrix_widgets = []  # Limpa a lista de referências de widgets

        # Adiciona Labels das Variáveis (X1, X2, ...)
        for i in range(self.num_cols-1): #-1 por que o termo independente não é variável
            # ### MUDANÇA FUNCIONAL: Altera X{i} para X{i+1} para começar em X1
            new_variable = QLabel(f"X{i+1}")
            new_variable.setAlignment(Qt.AlignCenter)
            #new_variable.setFixedSize(50, 30)
            self.matrix_grid_layout.addWidget(new_variable, 0, i)

        # ### MUDANÇA FUNCIONAL: Adiciona o Label do Termo Independente (B)
        label_b = QLabel("B")
        label_b.setAlignment(Qt.AlignCenter)
        self.matrix_grid_layout.addWidget(label_b, 0, self.num_cols - 1)

        # --- 3. Recria a UI com os Dados Atualizados ---
        for row in range(1,self.num_rows):
            row_widgets = []  # Lista para os widgets desta linha
            for col in range(self.num_cols):
                line_edit = QLineEdit(self)
                line_edit.setFixedSize(50, 30)
                line_edit.setAlignment(Qt.AlignCenter)

                # Preenche o QLineEdit com o valor do nosso modelo de dados
                line_edit.setText(str(self.matrix_data[row-1][col]))
                #Coloca LineEdit em sua posição na grid
                self.matrix_grid_layout.addWidget(line_edit, row, col)
                row_widgets.append(line_edit)  # Adiciona à lista da linha

            self.matrix_widgets.append(row_widgets)  # Adiciona a linha à matriz de widgets

        self.matrix_grid_layout.setAlignment(Qt.AlignCenter)
        # ### LINHA REMOVIDA: print("\nself.matrix_data no final eh:")
        # ### LINHA REMOVIDA: print(self.matrix_data)

    def increase_dimensions(self):
        """Aumenta as dimensões e reconstrói a UI preservando os dados."""
        if (self.num_rows - 1) < self.MAX_VARIABLES:
            # 1. Salva os valores atuais da UI no self.matrix_data
            self.sync_data_from_ui()

            # 2. Aumenta as dimensões
            self.num_rows += 1
            self.num_cols += 1

            # 3. Reconstrói a UI (a função agora sabe como preservar os dados)
            self.rebuild_matrix_ui()
        else:
            # ### MUDANÇA FUNCIONAL: Usando QMessageBox para erro (melhor UX no GUI)
            QMessageBox.critical(self,"Erro","Não é possível aumentar mais as dimensões da matriz.")

    def decrease_dimensions(self):
        """Diminui as dimensões e reconstrói a UI (descartando dados)."""
        if self.num_rows > 2 and self.num_cols > 1:
            self.num_rows -= 1
            self.num_cols -= 1

            # Como o usuário disse que não precisa salvar,
            # nós lemos os dados atuais, mas só usaremos
            # a parte que "cabe" na nova matriz menor.
            self.sync_data_from_ui()

            # Reconstrói a UI. A função 'rebuild_matrix_ui'
            # vai naturalmente descartar as linhas/colunas extras
            # ao copiar os dados antigos para a nova matriz menor.
            self.rebuild_matrix_ui()
        else:
            # ### MUDANÇA FUNCIONAL: Usando QMessageBox para erro (melhor UX no GUI)
            QMessageBox.critical(self,"Erro","Não é possível diminuir mais as dimensões da matriz.")

    def resize_matrix(self):
        try:
            numero_variaveis = int(self.resize_input.text())
        except ValueError:
            QMessageBox.critical(self,"Erro","Você não digitou um inteiro")
            return
        if numero_variaveis <= 0:
            QMessageBox.critical(self, "Erro", "Você digitou um número menor ou igual a 0")
        elif numero_variaveis > self.MAX_VARIABLES:
            QMessageBox.critical(self, "Erro", "Você digitou um número muito grande")
        else:
            self.num_rows = self.num_cols = numero_variaveis+1
            self.sync_data_from_ui()
            self.rebuild_matrix_ui()

    def calcular(self):
        sistema = []
        # 1. Coleta os dados da UI, convertendo para float
        for row in range(len(self.matrix_widgets)):
            linha = []
            for col in range(len(self.matrix_widgets[row])):
                try:
                    text_value = self.matrix_widgets[row][col].text().replace(',', '.')
                    linha.append(float(text_value))
                except ValueError:
                    QMessageBox.critical(self, "Erro", f"Valor inválido na matriz na posição [{row+1},{col+1}].")
                    return
            sistema.append(linha)

        print(f"\nVocê selecionou o método {self.menu_opcoes.currentText()}, e o sistema ficou:")
        print(sistema)

        metodo_selecionado = self.menu_opcoes.currentText()
        resultado = None

        if metodo_selecionado == "Gauss": 
            if self.num_rows - 1 != self.num_cols - 1:
                QMessageBox.critical(self, "Erro", "Eliminação de Gauss requer um sistema quadrado (N equações e N variáveis).")
                return
            resultado = eliminacao_gauss(sistema) 
            
        elif metodo_selecionado == "Jordan":
            QMessageBox.information(self, "Aviso", "Método de Jordan ainda não implementado.")
        
        elif metodo_selecionado == "LU":
            QMessageBox.information(self, "Aviso", "Método de LU ainda não implementado.")

        elif metodo_selecionado == "Jacobi":
            QMessageBox.information(self, "Aviso", "Método de Jacobi ainda não implementado.")

        elif metodo_selecionado == "Gauss-Siedel":
            try:
                from metodos import gauss_seidel
                resultado = gauss_seidel(sistema)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao executar Gauss-Seidel: {e}")
                return

        # 3. Exibição do Resultado
        if resultado is not None:
            if isinstance(resultado, str):
                QMessageBox.critical(self, "Erro de Cálculo", resultado)
            else:
                mensagem_solucao = f"Solução encontrada pelo método {metodo_selecionado}:\n"
                if len(resultado) == 3:
                    variaveis = [f"X{i+1} (Mina {i+1})" for i in range(len(resultado))]
                else:
                    variaveis = [f"X{i+1}" for i in range(len(resultado))]

                for i, valor in enumerate(resultado):
                    nome = variaveis[i]
                    mensagem_solucao += f"{nome}: {valor:.4f} m³\n" 
                    
                QMessageBox.information(self, f"Resultado - {metodo_selecionado}", mensagem_solucao)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixApp()
    window.show()
    sys.exit(app.exec())