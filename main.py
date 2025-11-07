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
        #CORRECAO---------------------------------------------------------
        self.label_x_interpolar = QLabel("Valor de x para interpolar:")
        interp_layout.addRow(self.label_x_interpolar, self.x_interpolar_input)
        
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

    # ---------- ALTERAÇÃO ----------
    def toggle_input_area(self, text):
        """Alterna entre a interface da Matriz e a interface de Interpolação ou Integração."""

        # --- Interpolação (mantém sua lógica atual) ---
        if text in ["Lagrange", "Newton"]:
            self.label_titulo.setText("Interpolação")
            self.stacked_input_widget.setCurrentWidget(self.interpolation_page)

            # Mantém placeholders originais para interpolação
            self.x_data_input.setPlaceholderText("Ex: 1.0, 2.5, 4.0")
            self.y_data_input.setPlaceholderText("Ex: 1.0, 7.5, 16.0")
            self.x_interpolar_input.show()  # mostrar novamente se estava oculto
            self.label_x_interpolar.show()
            return

        # --- Integração Numérica (nova parte corrigida) ---
        elif text in ["Trapézio", "Simpson"]:
            self.label_titulo.setText("Integração Numérica")
            self.stacked_input_widget.setCurrentWidget(self.interpolation_page)

            # Ajusta textos
            self.x_data_input.setPlaceholderText("Ex: 3.00, 2.92, 2.75, 2.52, 2.30, 1.84, 0.92, 0.40")
            self.y_data_input.setPlaceholderText("Ex: 0.40 (distância entre pontos)")
            self.x_interpolar_input.hide()# não precisa de x para interpolar aqui
            self.label_x_interpolar.hide()
            return

        # --- Sistemas Lineares (mantém sua lógica original) ---
        else:
            self.label_titulo.setText("Solucionador de sistema linear")
            self.stacked_input_widget.setCurrentWidget(self.matrix_page)
            return

        # --------------------------------------

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def sync_data_from_ui(self):
        if not self.matrix_widgets: 
            return
        for row in range(len(self.matrix_widgets)):
            for col in range(len(self.matrix_widgets[row])):
                self.matrix_data[row][col] = self.matrix_widgets[row][col].text()

    def rebuild_matrix_ui(self):
        new_data = [["0"] * self.num_cols for _ in range(self.num_rows-1)]
        if self.matrix_data:
            rows_to_copy = min(len(self.matrix_data), self.num_rows-1)
            cols_to_copy = min(len(self.matrix_data[0]), self.num_cols)
            for row in range(rows_to_copy):
                for col in range(cols_to_copy):
                    new_data[row][col] = self.matrix_data[row][col]
        self.matrix_data = new_data 
        self.clear_layout(self.matrix_grid_layout)
        self.matrix_widgets = []

        if not self.isMaximized():
            self.adjustSize()

        for i in range(self.num_cols-1):
            new_variable = QLabel(f"X{i+1}")
            new_variable.setAlignment(Qt.AlignCenter)
            self.matrix_grid_layout.addWidget(new_variable, 0, i)

        label_b = QLabel("B")
        label_b.setAlignment(Qt.AlignCenter)
        self.matrix_grid_layout.addWidget(label_b, 0, self.num_cols - 1)

        for row in range(1,self.num_rows):
            row_widgets = [] 
            for col in range(self.num_cols):
                line_edit = QLineEdit(self)
                line_edit.setFixedSize(50, 30)
                line_edit.setAlignment(Qt.AlignCenter)
                line_edit.setText(self.matrix_data[row-1][col])
                self.matrix_grid_layout.addWidget(line_edit, row, col)
                row_widgets.append(line_edit)
            self.matrix_widgets.append(row_widgets) 

        self.matrix_grid_layout.setAlignment(Qt.AlignCenter)

    def increase_dimensions(self):
        if (self.num_rows - 1) < self.MAX_VARIABLES:
            self.sync_data_from_ui()
            self.num_rows += 1
            self.num_cols += 1
            self.rebuild_matrix_ui()

    def decrease_dimensions(self):
        if self.num_rows > 2 and self.num_cols > 1:
            self.num_rows -= 1
            self.num_cols -= 1
            self.sync_data_from_ui()
            self.rebuild_matrix_ui()

    def resize_matrix(self):
        try:
            numero_variaveis = int(self.resize_input.text())
        except ValueError:
            QMessageBox.critical(self,"Erro","Você não digitou um inteiro")
            return
        if numero_variaveis <= 0:
            QMessageBox.critical(self, "Erro", "Número inválido")
        elif numero_variaveis > self.MAX_VARIABLES:
            QMessageBox.critical(self, "Erro", "Número muito grande")
        else:
            self.num_rows = self.num_cols = numero_variaveis+1
            self.sync_data_from_ui()
            self.rebuild_matrix_ui()

    def processar_dados_interpolacao(self):
        try:
            X = [float(v.replace(',', '.')) for v in self.x_data_input.text().split(',')]
            Y = [float(v.replace(',', '.')) for v in self.y_data_input.text().split(',')]
            x_interpolar = float(self.x_interpolar_input.text().replace(',', '.'))
            if len(X) != len(Y):
                QMessageBox.critical(self,"Erro","X e Y devem ter o mesmo tamanho.")
                return None,None,None
            return X,Y,x_interpolar
        except:
            QMessageBox.critical(self,"Erro","Dados inválidos.")
            return None,None,None

    def calcular(self):
        metodo_selecionado = self.menu_opcoes.currentText()
        resultado = None

        if metodo_selecionado in ["Gauss", "Gauss-Seidel", "Jordan", "LU", "Jacobi"]:
            sistema = []
            for row in range(len(self.matrix_widgets)):
                linha = []
                for col in range(len(self.matrix_widgets[row])):
                    try:
                        linha.append(float(self.matrix_widgets[row][col].text().replace(',', '.')))
                    except:
                        QMessageBox.critical(self,"Erro","Valor inválido na matriz.")
                        return
                sistema.append(linha)

            if metodo_selecionado == "Gauss":
                resultado = eliminacao_gauss(sistema)

            elif metodo_selecionado == "Gauss-Seidel":
                resultado = gauss_seidel(sistema)

            if resultado is not None:
                    # --- INÍCIO DA CORREÇÃO ---

                    # PRIMEIRO, CHECAR SE O RESULTADO É UMA STRING (QUE SÓ PODE SER ERRO)
                if isinstance(resultado, str):
                    mensagem = resultado # A própria string já é a mensagem de erro
                    
                    # SE FOR UMA LISTA (O QUE ESPERAMOS), AÍ SIM FORMATAMOS
                elif isinstance(resultado, list):
                    try:
                            # Tenta formatar, agora com segurança
                        mensagem = "\n".join(f"X{i+1}: {float(v):.4f}" for i,v in enumerate(resultado))
                    except ValueError:
                            # Se falhar aqui, a lista tinha lixo dentro
                        mensagem = f"Erro: A função retornou valores não-numéricos na lista: {resultado}"
                    
                    # Caso a função retorne algo que não é lista nem string
                else:
                    mensagem = f"Resultado em formato inesperado: {str(resultado)}"

                    # Exibe o que quer que tenha acontecido
                QMessageBox.information(self,f"Resultado - {metodo_selecionado}",mensagem)
                    # --- FIM DA CORREÇÃO ---
                return

        elif metodo_selecionado in ["Lagrange","Newton"]:
            X,Y,x_interp = self.processar_dados_interpolacao()
            if X is None: return
            resultado = interpolacao_lagrange(X,Y,x_interp) if metodo_selecionado=="Lagrange" else interpolacao_newton(X,Y,x_interp)
            QMessageBox.information(self,f"Resultado - {metodo_selecionado}",f"P({x_interp}) ≈ {resultado:.6f}")
            return

        elif metodo_selecionado in ["Trapézio","Simpson"]:
            try:
                valores = [float(v.replace(",", ".")) for v in self.x_data_input.text().split(",")]
                h = float(self.y_data_input.text().replace(",", ".")) if self.y_data_input.text() else 0.40

                if metodo_selecionado == "Trapézio":
                    soma = valores[0] + valores[-1] + 2 * sum(valores[1:-1])
                    resultado = (h / 2) * soma
                else:
                    y = valores
                    A13 = (h/3)*(y[0] + y[4] + 4*(y[1]+y[3]) + 2*y[2])
                    A38 = (3*h/8)*(y[4] + 3*(y[5]+y[6]) + y[7])
                    resultado = A13 + A38

                QMessageBox.information(self,f"Resultado - {metodo_selecionado}",f"Área ≈ {resultado:.6f} m²")
                return

            except:
                pass

            func_text = self.x_data_input.text().strip()
            a = float(self.y_data_input.text().replace(",", "."))
            b = float(self.x_interpolar_input.text().replace(",", "."))
            n = int(self.resize_input.text())
            f = eval("lambda x: " + func_text)
            resultado = integracao_trapezio_repetida(f,a,b,n) if metodo_selecionado=="Trapézio" else integracao_simpson_repetida(f,a,b,n)
            QMessageBox.information(self,f"Resultado - {metodo_selecionado}",f"Integral ≈ {resultado:.6f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixApp()
    window.show()
    sys.exit(app.exec())
