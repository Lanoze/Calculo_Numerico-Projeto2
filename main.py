# main.py
#from logging import exception
from auxiliares import formatar_expression,avaliar_expressao
from metodos import eliminacao_gauss 
# --- NOVAS IMPORTAÇÕES NECESSÁRIAS ---
from metodos import*
# --------------------------------------
from MyWidgets import ResultadoIntegral,DynamicStackedWidget

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout,QMessageBox,QComboBox, QStackedWidget, QGroupBox, QFormLayout,
    QCheckBox
)
from PySide6.QtCore import Qt,QTimer


class MatrixApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de métodos Numéricos")

        # ### MUDANÇA FUNCIONAL: Inicializa como 3x3 + 1 para labels/coluna B
        self.num_rows = 3 #O número de linhas é igual ao de colunas porque tem os labels (Variáveis)
        self.num_cols = 3 #Geralmente num_cols seria igual a num_linhas+1
        self.MAX_VARIABLES = 10 #O número máximo de colunas é esse número + 1 (é uma constante)

        # 1. Nosso modelo de dados para armazenar os valores (começa vazio), não armazena as variáveis
        self.matrix_data = []
        # Manter uma referência aos widgets para fácil acesso
        self.matrix_widgets = []

        #self.setup_ui()
        self.main_layout = QVBoxLayout(self)  # Empilha verticalmente os elementos
        # self.main_layout.addStretch(1)
        self.label_titulo = QLabel("Solucionador de sistema linear")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label_titulo)

        # --- NOVO: QStackedWidget para alternar a interface de entrada ---
        self.stacked_input_widget = DynamicStackedWidget()
        #self.stacked_input_widget.setSizePolicy(self.stacked_input_widget.sizePolicy().Maximum)
        #Colocar stretch no stacked_widget não funcionou
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
        control_buttons_layout = QHBoxLayout()  # Os botões aparecem horizontalmente
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

        control_buttons_layout.addStretch(1)  # Ajuda a centralizar os botões
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
        self.metodo_iterativo_widget = QWidget()
        metodo_iterativoLayout = QFormLayout(self.metodo_iterativo_widget)
        self.tolLabel = QLabel("Tolerância:")
        self.tolInput = QLineEdit()
        self.tolInput.setPlaceholderText("1e-6")
        metodo_iterativoLayout.addRow(self.tolLabel,self.tolInput)
        self.listLabel = QLabel("Valores iniciais:")
        self.listInput = QLineEdit()
        self.listInput.setPlaceholderText("[0...0]")
        metodo_iterativoLayout.addRow(self.listLabel, self.listInput)
        self.iterLabel = QLabel("Máximo de iterações")
        self.iterInput = QLineEdit()
        self.iterInput.setPlaceholderText("100")
        metodo_iterativoLayout.addRow(self.iterLabel,self.iterInput)
        self.metodo_iterativo_widget.setVisible(False)
        matrix_page_layout.addWidget(self.metodo_iterativo_widget,stretch=1)

        # matrix_page_layout.addStretch(1)
        self.stacked_input_widget.addWidget(self.matrix_page)  # Adiciona a primeira página

        # =================================================================
        # 2. Página de Entrada de Interpolação (Listas X, Y)
        # =================================================================
        self.interpolation_page = QWidget()
        interp_page_layout = QVBoxLayout(self.interpolation_page)

        self.interpolation_group = QGroupBox("Dados para Interpolação (X, Y)")
        interp_layout = QFormLayout(self.interpolation_group)

        self.x_data_input = QLineEdit()
        self.x_data_input.setPlaceholderText("Ex: 3.0, 3.6, 7")
        self.xLabel = QLabel("Pontos X (separados por vírgula):")
        interp_layout.addRow(self.xLabel, self.x_data_input)

        self.y_data_input = QLineEdit()
        self.y_data_input.setPlaceholderText("Ex: 1.0, 7.5, 16.0")
        self.yLabel = QLabel("Pontos Y (separados por vírgula):")
        interp_layout.addRow(self.yLabel, self.y_data_input)

        self.x_interpolar_input = QLineEdit()
        self.x_interpolar_input.setPlaceholderText("Ex: 3.0")
        # CORRECAO---------------------------------------------------------
        self.label_x_interpolar = QLabel("Valor de x para interpolar:")
        interp_layout.addRow(self.label_x_interpolar, self.x_interpolar_input)

        interp_page_layout.addWidget(self.interpolation_group)
        self.CBUsarFuncao = QCheckBox("Usar função")
        self.CBUsarFuncao.toggled.connect(self.check_toggle)
        interp_page_layout.addWidget(self.CBUsarFuncao)
        interp_page_layout.addStretch(1)
        self.stacked_input_widget.addWidget(self.interpolation_page)  # Adiciona a segunda página
        # =================================================================

        # Linha de Cálculo
        calculo_row = QHBoxLayout()
        calculo_row.addStretch(1)
        self.menu_opcoes = QComboBox()

        # Opcoes de metodos #
        self.menu_opcoes.addItems([
            "Gauss", "Jordan", "LU", "Jacobi","Gauss-Seidel",
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

        # Css para mudar a aparência (QSS sendo mais específico)
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
                                    
                                    QCheckBox {
                                        spacing: 10px; /* Espaço entre o interruptor e o texto */
                                    }
                            
                                    /* O 'trilho' por onde o botão desliza */
                                    QCheckBox::indicator {
                                        width: 40px;
                                        height: 20px;
                                        background-color: #AAAAAA; /* Cor do trilho (desligado) */
                                        border: 1px solid #777;
                                        border-radius: 10px; /* Deixa o trilho arredondado */
                                    }
                            
                                    /* O círculo deslizante (handle) */
                                    QCheckBox::indicator::handle {
                                        background-color: white;
                                        border-radius: 5px; /* Deixa o círculo... circular */
                                        width: 16px;
                                        height: 16px;
                                        margin: 2px; /* Pequena margem interna */
                                    }
                            
                                    /* --- ESTADO LIGADO --- */
                                    
                                    /* O trilho quando está LIGADO (checked) */
                                    QCheckBox::indicator:checked {
                                        background-color: #131352; /* Cor verde (ligado) */
                                        border: 1px solid #3E8E41;
                                    }
                            
                                    /* O círculo deslizante quando está LIGADO */
                                    QCheckBox::indicator:checked::handle {
                                        /* Move o círculo para a direita */
                                        margin-left: 22px; 
                                    }

                                    MatrixApp{
                                    background-color: #A6C0ED
                                    }
                                    QMessageBox{
                                    background-color: #A6C0ED
                                    }
                                ''')

        # Cria a matriz inicial (agora preenche self.matrix_data com "0")
        self.rebuild_matrix_ui()

        # --- NOVO: Conecta a mudança de metodo para alternar a entrada de dados ---
        self.menu_opcoes.currentTextChanged.connect(self.toggle_input_area)
        self.move(100, 100)

    # ---------- ALTERAÇÃO ----------
    def toggle_input_area(self, text):
        """Alterna entre a interface da Matriz e a interface de Interpolação ou Integração."""

        # --- Interpolação (mantém sua lógica atual) ---
        if text in ["Lagrange", "Newton"]:
            self.label_titulo.setText("Interpolação")
            #self.CBUsarFuncao.setVisible(False)
            self.stacked_input_widget.setCurrentWidget(self.interpolation_page)
            self.xLabel.setText("Pontos X (separados por vírgula):")
            self.interpolation_group.setTitle("Dados para Interpolação (X, Y)")
            # Mantém placeholders originais para interpolação
            # self.x_data_input.setPlaceholderText("Ex: 1.0, 2.5, 4.0")
            # self.y_data_input.setPlaceholderText("Ex: 1.0, 7.5, 16.0")
            self.x_interpolar_input.show()  # mostrar novamente se estava oculto
            self.label_x_interpolar.show()

        # --- Integração Numérica (nova parte corrigida) ---
        elif text in ["Trapézio", "Simpson"]:
            self.label_titulo.setText("Integração Numérica")
            self.interpolation_group.setTitle("Dados para Integração (X, Y)")
            #self.CBUsarFuncao.setVisible(True)
            self.stacked_input_widget.setCurrentWidget(self.interpolation_page)

            # Ajusta textos
            self.xLabel.setText("Limites e número de pontos: ")
            # self.x_data_input.setPlaceholderText("Ex: 1.0, 2.5, 4.0")
            # self.y_data_input.setPlaceholderText("Ex: 1.0, 7.5, 16.0")
            self.x_interpolar_input.hide()# não precisa de x para interpolar aqui
            self.label_x_interpolar.hide()

        # --- Sistemas Lineares (mantém sua lógica original) ---
        else:
            self.label_titulo.setText("Solucionador de sistema linear")
            self.stacked_input_widget.setCurrentWidget(self.matrix_page)
            if text in ("Jacobi","Gauss-Seidel"):
                self.metodo_iterativo_widget.setVisible(True)
            else:
                self.metodo_iterativo_widget.setVisible(False)
        if not self.isMaximized():
            print("Changing")
            QTimer.singleShot(0,self.adjustSize)
        #self.stacked_input_widget.adjustSize()

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

        for i in range(self.num_cols-1):
            new_variable = QLabel(f"X{i+1}")
            new_variable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.matrix_grid_layout.addWidget(new_variable, 0, i)

        label_b = QLabel("B")
        label_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.matrix_grid_layout.addWidget(label_b, 0, self.num_cols - 1)

        for row in range(1,self.num_rows):
            row_widgets = []
            for col in range(self.num_cols):
                line_edit = QLineEdit(self)
                line_edit.setFixedSize(50, 30)
                line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                line_edit.setText(self.matrix_data[row-1][col])
                self.matrix_grid_layout.addWidget(line_edit, row, col)
                row_widgets.append(line_edit)
            self.matrix_widgets.append(row_widgets)

        self.matrix_grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if not self.isMaximized():
            QTimer.singleShot(0,self.adjustSize) #Pequeno atraso para conseguir ajustar para o tamanho correto

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

    def check_toggle(self,checked):
        if checked:
            self.yLabel.setText("Função:")
            self.y_data_input.setPlaceholderText("Ex: e^x")
            print("Caixinha ativada!")
        else:
            self.yLabel.setText("Pontos Y (separados por vírgula):")
            self.y_data_input.setPlaceholderText("Ex: 1.0, 7.5, 16.0")
            print("Caixinha desativada!")

    def processar_dados_interpolacao(self):
        try:
            x = [float(v.replace(',', '.')) for v in self.x_data_input.text().split(',')]
            if self.CBUsarFuncao.isChecked():
                funcao = formatar_expression(self.y_data_input.text())
                y = [avaliar_expressao(funcao,p) for p in x]
            else:
                y = [float(v.replace(',', '.')) for v in self.y_data_input.text().split(',')]
            x_interpolar = float(self.x_interpolar_input.text().replace(',', '.'))
            if len(x) != len(y):
                QMessageBox.critical(self,"Erro","X e Y devem ter o mesmo tamanho.")
                return None,None,None
            return x,y,x_interpolar
        except Exception as e:
            QMessageBox.critical(self,"Erro",f"Dados inválidos, erro: {e}")
            return None,None,None

    def calcular(self):
        metodo_selecionado = self.menu_opcoes.currentText()
        resultado = None
        if metodo_selecionado in ("Jacobi","LU"):
            resultado = "Método ainda não implementado"
        if metodo_selecionado in ["Gauss", "Gauss-Seidel", "Jordan", "LU", "Jacobi"]:
            sistema = []
            for row in range(len(self.matrix_widgets)):
                linha = []
                for col in range(len(self.matrix_widgets[row])):
                    try:
                        linha.append(float(self.matrix_widgets[row][col].text().replace(',', '.')))
                    except ValueError:
                        QMessageBox.critical(self,"Erro","Valor inválido na matriz.")
                        return
                sistema.append(linha)

            try:
                if metodo_selecionado == "Gauss":
                    resultado = eliminacao_gauss(sistema)
                elif metodo_selecionado == "Gauss-Seidel":
                    tol = self.tolInput.text()
                    if tol: #Se não for string vazia
                        tol = float(tol)
                    else:
                        tol = 1e-6
                    max_iter = self.iterInput.text()
                    if max_iter:
                        max_iter = int(self.iterInput.text())
                    else:
                        max_iter = 100
                    valores_iniciais = self.listInput.text()
                    if valores_iniciais:
                        valores_iniciais = [float(x) for x in self.listInput.text().split(',')]
                        if len(valores_iniciais) == self.num_rows - 1:
                            resultado = gauss_seidel(sistema,max_iter=max_iter,tol=tol,valores_iniciais=valores_iniciais)
                        else:
                            resultado = "Você não colocou o número correto de valores iniciais."
                    else:
                        valores_iniciais = []
                        resultado = gauss_seidel(sistema, max_iter=max_iter, tol=tol, valores_iniciais=valores_iniciais)
                elif metodo_selecionado == "Jordan":
                    resultado = eliminacao_jordan(sistema)
            except Exception as e:
                mensagem = f"Erro: {e}"
                # --- INÍCIO DA CORREÇÃO ---

                # PRIMEIRO, CHECAR SE O RESULTADO É UMA STRING (QUE SÓ PODE SER ERRO)
            if isinstance(resultado, str):
                mensagem = resultado # A própria string já é a mensagem de erro

                # SE FOR UMA LISTA (O QUE ESPERAMOS), AÍ SIM FORMATAMOS
            elif isinstance(resultado, list):
                try:
                        # Tenta formatar, agora com segurança
                    mensagem = "\n".join(f"X{i+1}: {float(v):.5g}" for i,v in enumerate(resultado))
                except ValueError:
                        # Se falhar aqui, a lista tinha lixo dentro
                    mensagem = f"Erro: A função retornou valores não-numéricos na lista: {resultado}"

            #     # Caso a função retorne algo que não é lista nem string
            # else:
            #     mensagem = f"Resultado em formato inesperado: {str(resultado)}"

                # Exibe o que quer que tenha acontecido
            QMessageBox.information(self,f"Resultado - {metodo_selecionado}",mensagem)
                # --- FIM DA CORREÇÃO ---

        elif metodo_selecionado in ["Lagrange","Newton"]:
            x,y,x_interp = self.processar_dados_interpolacao()
            if x is None: return
            resultado = interpolacao_lagrange(x,y,x_interp) if metodo_selecionado=="Lagrange" else interpolacao_newton(x,y,x_interp)
            QMessageBox.information(self,f"Resultado - {metodo_selecionado}",f"P({x_interp}) ≈ {resultado:.6f}")
            return

        elif metodo_selecionado in ["Trapézio","Simpson"]:
            x_dados = self.x_data_input.text().split(',')
            if len(x_dados) != 3:
                QMessageBox.critical(self,"Erro","Você precisa digitar exatamente 3 números")
                return
            try:
                x_dados[0] = float(x_dados[0])
                x_dados[1] = float(x_dados[1])
                x_dados[2] = int(x_dados[2])
            except ValueError:
                QMessageBox.critical(self,"Erro","Tipo de dado inválido")
                return
            lim_inferior,lim_superior,numero_pontos = x_dados
            if numero_pontos < 2:
                QMessageBox.critical(self,"Erro","Você precisa de pelo menos 2 pontos")
                return
            elif numero_pontos > 1000:
                QMessageBox.critical(self, "Erro", "Você colocou um número muito grande de pontos (> 1000)")
                return
            if metodo_selecionado == "Simpson" and numero_pontos%2 == 0:
                QMessageBox.critical(self, "Erro", "O método de 1/3 de Simpson requer um número ímpar de pontos")
                return
            y_pontos = []
            x_pontos = []
            h = (lim_superior - lim_inferior) / (numero_pontos - 1)
            ponto_atual = lim_inferior

            #Se os pontos vão ser calculados por uma função
            if self.CBUsarFuncao.isChecked():
                try:
                    funcao = formatar_expression(self.y_data_input.text())
                    #Estamos considerando o espaçamento entre os pontos constante
                    for i in range(numero_pontos):
                        x_pontos.append(ponto_atual)
                        y_pontos.append(avaliar_expressao(funcao,ponto_atual))
                        # Fiz dessa forma mais complexa para evitar erro de arredondamento, melhor que ficar somando h
                        ponto_atual = lim_inferior + (i+1)*h
                except Exception as e:
                    #print("Erro fatal")
                    QMessageBox.critical(self,"Erro",f"Ocorreu algum erro: {e}")
                    return
            #O usuário já digitou os pontos de y
            else:
                y_pontos = self.y_data_input.text().split(',')
                if len(y_pontos) != numero_pontos:
                    QMessageBox.critical(self,"Erro","O número de pontos X e Y devem ser iguais")
                    return
                try:
                    for i in range(numero_pontos):
                        x_pontos.append(ponto_atual)
                        y_pontos[i] = float(y_pontos[i])
                        ponto_atual = lim_inferior + (i+1)*h
                except Exception as e:
                    QMessageBox.critical(self,"Erro",f"Ocorreu algum erro: {e}")
            print(f"X = {x_pontos}")
            print(f"Y = {y_pontos}")
            # Necessário a cópia pois os metodos removem o ponto inicial e final de Y_pontos
            if metodo_selecionado == "Trapézio":
                resultado = integracao_trapezio(y_pontos.copy(),h)
            else:
                resultado = integracao_simpson(y_pontos.copy(),h)
            ResultadoIntegral("Resultado da Integral",self, resultado,x_pontos,y_pontos).exec()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixApp()
    window.show()
    sys.exit(app.exec())
