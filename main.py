# main.py

from metodos import eliminacao_gauss 
# --- NOVAS IMPORTAÇÕES NECESSÁRIAS ---
from metodos import gauss_seidel, interpolacao_lagrange, interpolacao_newton, integracao_trapezio_repetida, integracao_simpson_repetida 
# --------------------------------------

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout,QMessageBox,QComboBox, QStackedWidget, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt, QEvent


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
        self.setWindowTitle("Solucionador de Sistema Linear / Interpolação")
        self.setGeometry(100, 100, 400, 300)

        # ### MUDANÇA FUNCIONAL: Inicializa como 3x3 + 1 para labels/coluna B
        self.num_rows = 3 #O número de linhas é igual ao de colunas porque tem os labels (Variáveis)
        self.num_cols = 3 #Geralmente num_cols seria igual a num_linhas+1
        self.MAX_VARIABLES = 10 #O número máximo de colunas é esse número + 1 (é uma constante)

        # 1. Nosso modelo de dados para armazenar os valores (começa vazio), não armazena as variáveis
        self.matrix_data = []
        # Manter uma referência aos widgets para fácil acesso
        self.matrix_widgets = []

        self.setup_ui()
        # Cria a matriz inicial (agora preenche self.matrix_data com "0")
        self.rebuild_matrix_ui()

        # --- NOVO: Conecta a mudança de metodo para alternar a entrada de dados ---
        self.menu_opcoes.currentTextChanged.connect(self.toggle_input_area)

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self) #Empilha verticalmente os elementos
        #self.main_layout.addStretch(1)
        self.label_titulo = QLabel("Solucionador de sistema linear")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label_titulo)

        # --- NOVO: QStackedWidget para alternar a interface de entrada ---
        self.stacked_input_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_input_widget)

        # =================================================================
        # 1. Página de Entrada de Sistemas Lineares (Matriz)
        # =================================================================
        self.matrix_page = QWidget()
        matrix_page_layout = QVBoxLayout(self.matrix_page)

        # Matriz Grid Layout 
        self.matrix_grid_layout = QGridLayout()
        matrix_page_layout.addLayout(self.matrix_grid_layout)

        # Controles de Dimensão 
        control_buttons_layout = QHBoxLayout() #Os botões aparecem horizontalmente
        control_buttons_layout.addStretch(1)

        self.btn_add = QPushButton("+")
        self.btn_add.setFixedSize(40, 40)
        self.btn_add.setObjectName("Aumentar")
        self.btn_add.clicked.connect(self.increase_dimensions)
        control_buttons_layout.addWidget(self.btn_add)

        self.btn_subtract = QPushButton("-")
        self.btn_subtract.setFixedSize(40, 40)
        self.btn_subtract.setObjectName("Diminuir")
        self.btn_subtract.clicked.connect(self.decrease_dimensions)
        control_buttons_layout.addWidget(self.btn_subtract)

        control_buttons_layout.addStretch(1) #Ajuda a centralizar os botões
        matrix_page_layout.addLayout(control_buttons_layout)
        
        # Resize da Matriz 
        resize_row = QHBoxLayout()
        resize_row.addStretch(1)
        resize_button = QPushButton("Resize")
        resize_button.clicked.connect(self.resize_matrix)
        self.resize_input = QLineEdit()
        self.resize_input.setPlaceholderText("Número de variáveis")
        resize_row.addWidget(resize_button)
        resize_row.addWidget(self.resize_input)
        resize_row.addStretch(1)
        matrix_page_layout.addLayout(resize_row)
        
        #matrix_page_layout.addStretch(1)
        self.stacked_input_widget.addWidget(self.matrix_page) # Adiciona a primeira página

        # =================================================================
        # 2. Página de Entrada de Interpolação (Listas X, Y)
        # =================================================================
        self.interpolation_page = QWidget()
        interp_page_layout = QVBoxLayout(self.interpolation_page)
        
        interpolation_group = QGroupBox("Dados para Interpolação (X, Y)")
        interp_layout = QFormLayout(interpolation_group)
        
        self.x_data_input = QLineEdit()
        self.x_data_input.setPlaceholderText("Ex: 1.0, 2.5, 4.0")
        interp_layout.addRow(QLabel("Pontos X (separados por vírgula):"), self.x_data_input)
        
        self.y_data_input = QLineEdit()
        self.y_data_input.setPlaceholderText("Ex: 1.0, 7.5, 16.0")
        interp_layout.addRow(QLabel("Pontos Y (separados por vírgula):"), self.y_data_input)
        
        self.x_interpolar_input = QLineEdit()
        self.x_interpolar_input.setPlaceholderText("Ex: 3.0")
        interp_layout.addRow(QLabel("Valor de x para interpolar:"), self.x_interpolar_input)
        
        interp_page_layout.addWidget(interpolation_group)
        interp_page_layout.addStretch(1)
        self.stacked_input_widget.addWidget(self.interpolation_page) # Adiciona a segunda página
        # =================================================================

        # Linha de Cálculo 
        calculo_row = QHBoxLayout()
        calculo_row.addStretch(1)
        self.menu_opcoes = QComboBox()

        # Opcoes de metodos #
        self.menu_opcoes.addItems([
        "Gauss", "Gauss-Seidel", "Jordan", "LU", "Jacobi",
        "Lagrange", "Newton", "Trapézio", "Simpson"
        ])

        # #########################################################
        self.calculo_botao = QPushButton("Calcular")
        self.calculo_botao.clicked.connect(self.calcular)
        calculo_row.addWidget(self.menu_opcoes)
        calculo_row.addWidget(self.calculo_botao)
        calculo_row.addStretch(1)
        self.main_layout.addLayout(calculo_row)
        self.main_layout.addStretch(1)

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
                            border: 1px solid #555; 
                            border-radius: 5px; 
                            padding: 5px 10px; 
                            background-color: #5B92A8; 
                            color: black; 
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

    # --- NOVO: Função para alternar as áreas de input ---
    def toggle_input_area(self, text):
        """Alterna entre a interface da Matriz e a interface de Interpolação."""
        if text in ["Lagrange", "Newton", "Trapézio", "Simpson"]:
            self.label_titulo.setText("Interpolação")
            self.stacked_input_widget.setCurrentWidget(self.interpolation_page)
        else:
            self.label_titulo.setText("Solucionador de sistema linear")
            self.stacked_input_widget.setCurrentWidget(self.matrix_page)

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
        if not self.matrix_widgets: 
            return

        for row in range(len(self.matrix_widgets)):
            for col in range(len(self.matrix_widgets[row])):
                self.matrix_data[row][col] = self.matrix_widgets[row][col].text()

    def rebuild_matrix_ui(self):
        """Limpa e reconstrói a UI da matriz com base nos dados e dimensões atuais."""
        # --- 1. Atualiza o Modelo de Dados ---
        new_data = [["0"] * self.num_cols for _ in range(self.num_rows-1)]

        if self.matrix_data:
            rows_to_copy = min(len(self.matrix_data), self.num_rows-1)
            cols_to_copy = min(len(self.matrix_data[0]), self.num_cols)
            for row in range(rows_to_copy):
                for col in range(cols_to_copy):
                    new_data[row][col] = self.matrix_data[row][col]

        self.matrix_data = new_data 

        # --- 2. Limpa a UI Antiga --- 
        self.clear_layout(self.matrix_grid_layout)
        self.matrix_widgets = []

        if not self.isMaximized():
            self.adjustSize()

        # Adiciona Labels das Variáveis (X1, X2, ...)
        for i in range(self.num_cols-1):
            new_variable = QLabel(f"X{i+1}")
            new_variable.setAlignment(Qt.AlignCenter)
            self.matrix_grid_layout.addWidget(new_variable, 0, i)

        # ### MUDANÇA FUNCIONAL: Adiciona o Label do Termo Independente (B)
        label_b = QLabel("B")
        label_b.setAlignment(Qt.AlignCenter)
        self.matrix_grid_layout.addWidget(label_b, 0, self.num_cols - 1)

        # --- 3. Recria a UI com os Dados Atualizados 
        for row in range(1,self.num_rows):
            row_widgets = [] 
            for col in range(self.num_cols):
                line_edit = QLineEdit(self)
                line_edit.setFixedSize(50, 30)
                line_edit.setAlignment(Qt.AlignCenter)

                line_edit.setText(str(self.matrix_data[row-1][col]))
                self.matrix_grid_layout.addWidget(line_edit, row, col)
                row_widgets.append(line_edit)

            self.matrix_widgets.append(row_widgets) 

        self.matrix_grid_layout.setAlignment(Qt.AlignCenter)

    def increase_dimensions(self):
        """Aumenta as dimensões e reconstrói a UI preservando os dados."""
      
        if (self.num_rows - 1) < self.MAX_VARIABLES:
            self.sync_data_from_ui()
            self.num_rows += 1
            self.num_cols += 1
            self.rebuild_matrix_ui()
        else:
            print("Não é possível aumentar mais as dimensões da matriz.")

    def decrease_dimensions(self):
        """Diminui as dimensões e reconstrói a UI (descartando dados)."""
       
        if self.num_rows > 2 and self.num_cols > 1:
            self.num_rows -= 1
            self.num_cols -= 1
            self.sync_data_from_ui()
            self.rebuild_matrix_ui()
        else:
            print("Não é possível diminuir mais as dimensões da matriz.")

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

    # --- NOVO: Função para processar os dados de interpolação ---
    def processar_dados_interpolacao(self):
        """Lê os QLineEdits de interpolação e retorna X, Y, x_interpolar ou exibe erro."""
        try:
            # Converte a string de X em lista de floats
            X_str = self.x_data_input.text().replace(' ', '').split(',')
            X = [float(val.replace(',', '.')) for val in X_str if val]
            
            # Converte a string de Y em lista de floats
            Y_str = self.y_data_input.text().replace(' ', '').split(',')
            Y = [float(val.replace(',', '.')) for val in Y_str if val]

            # Converte o x a interpolar para float
            x_interpolar = float(self.x_interpolar_input.text().replace(',', '.'))
            
            if len(X) != len(Y) or len(X) < 2:
                QMessageBox.critical(self, "Erro de Interpolação", "As listas de X e Y devem ter o mesmo número de pontos (mínimo 2) e não podem estar vazias.")
                return None, None, None
            
            return X, Y, x_interpolar
        
        except ValueError:
            QMessageBox.critical(self, "Erro de Formato", "Certifique-se de que os valores de X, Y e x para interpolar são números válidos.")
            return None, None, None

    def calcular(self):
        metodo_selecionado = self.menu_opcoes.currentText()
        resultado = None

        # --- Lógica de Sistemas Lineares (Preservada) ---
        if metodo_selecionado in ["Gauss", "Gauss-Seidel", "Jordan", "LU", "Jacobi"]:
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

            print(f"\nVocê selecionou o método {metodo_selecionado}, e o sistema ficou:")
            print(sistema)
            
            if metodo_selecionado == "Gauss": 
                if self.num_rows - 1 != self.num_cols - 1:
                    QMessageBox.critical(self, "Erro", "Eliminação de Gauss requer um sistema quadrado (N equações e N variáveis).")
                    return
                resultado = eliminacao_gauss(sistema) 
                
            elif metodo_selecionado == "Gauss-Seidel":
                # Já importa 'gauss_seidel' no cabeçalho
                if self.num_rows - 1 != self.num_cols - 1:
                    QMessageBox.critical(self, "Erro", "Gauss-Seidel requer um sistema quadrado (N equações e N variáveis).")
                    return
                try:
                    resultado = gauss_seidel(sistema)
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Falha ao executar Gauss-Seidel: {e}")
                    return

            elif metodo_selecionado == "Jordan":
                QMessageBox.information(self, "Aviso", "Método de Jordan ainda não implementado.")
                return
            
            elif metodo_selecionado == "LU":
                QMessageBox.information(self, "Aviso", "Método de LU ainda não implementado.")
                return

            elif metodo_selecionado == "Jacobi":
                QMessageBox.information(self, "Aviso", "Método de Jacobi ainda não implementado.")
                return
                
            # 3. Exibição do Resultado para Sistemas Lineares (Preservada)
            if resultado is not None:
                if isinstance(resultado, str):
                    QMessageBox.critical(self, "Erro de Cálculo", resultado)
                else:
                    mensagem_solucao = f"Solução encontrada pelo método {metodo_selecionado}:\n"
                    variaveis = [f"X{i+1}" for i in range(len(resultado))]
                    for i, valor in enumerate(resultado):
                        nome = variaveis[i]
                        mensagem_solucao += f"{nome}: {valor:.4f}\n"
                    QMessageBox.information(self, f"Resultado - {metodo_selecionado}", mensagem_solucao)

        # --- NOVO: Lógica para os métodos de Interpolação ---
        elif metodo_selecionado in ["Lagrange", "Newton"]:
            X, Y, x_interpolar = self.processar_dados_interpolacao()
            
            if X is None:
                return # Erro já exibido por processar_dados_interpolacao

            print(f"\nVocê selecionou o método {metodo_selecionado}. X={X}, Y={Y}, x_interpolar={x_interpolar}")

            if metodo_selecionado == "Lagrange":
                resultado = interpolacao_lagrange(X, Y, x_interpolar)
                
            elif metodo_selecionado == "Newton":
                resultado = interpolacao_newton(X, Y, x_interpolar)

            # 3. Exibição do Resultado para Interpolação
            if resultado is not None:
                if isinstance(resultado, str):
                    QMessageBox.critical(self, "Erro de Cálculo", resultado)
                else:
                    mensagem_solucao = (
                        f"Resultado da Interpolação de {metodo_selecionado}:\n"
                        f"P({x_interpolar}) = {resultado:.6f}"
                    )
                    QMessageBox.information(self, f"Resultado - {metodo_selecionado}", mensagem_solucao)

        # TRECHO ALTERADO 
        elif metodo_selecionado in ["Trapézio", "Simpson"]:

            try:
                valores = [float(v.replace(",", ".")) for v in self.x_data_input.text().split(",")]
                h = float(self.y_data_input.text().replace(",", ".")) if self.y_data_input.text() else 0.40
                n = len(valores) - 1

                if metodo_selecionado == "Trapézio":
                    soma = valores[0] + valores[-1] + 2 * sum(valores[1:-1])
                    resultado = (h / 2) * soma
                else:
                    y = valores
                    A13 = (h/3)*(y[0] + y[4] + 4*(y[1]+y[3]) + 2*y[2])
                    A38 = (3*h/8)*(y[4] + 3*(y[5]+y[6]) + y[7])
                    resultado = A13 + A38

                QMessageBox.information(self, f"Resultado - {metodo_selecionado}", f"Área aproximada ≈ {resultado:.6f} m²")
                return

            except:
                pass

            func_text = self.x_data_input.text().strip()
            a_text = self.y_data_input.text().replace(",", ".")
            b_text = self.x_interpolar_input.text().replace(",", ".")
            n_text = self.resize_input.text()

            try:
                f = eval("lambda x: " + func_text)
                a = float(a_text)
                b = float(b_text)
                n = int(n_text)
            except:
                QMessageBox.critical(self, "Erro de Entrada",
                    "Para integração via função, preencha:\n\n"
                    "X: f(x)\nY: limite inferior\Valor X para interpolar: limite superior\nResize: n")
                return

            if metodo_selecionado == "Trapézio":
                resultado = integracao_trapezio_repetida(f, a, b, n)
            else:
                resultado = integracao_simpson_repetida(f, a, b, n)

            QMessageBox.information(self, f"Resultado - {metodo_selecionado}", f"Integral aproximada ≈ {resultado:.6f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixApp()
    window.show()
    sys.exit(app.exec())