from PySide6.QtCore import Qt,QTimer
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, \
    QSizePolicy, QGridLayout, QWidget
from matplotlib.figure import Figure

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import sys

class ResultadoIntegral(QDialog):
    def __init__(self,parent,resultado: float,x_pontos: list[float],y_pontos: list[float], x_pontos_special = [], y_pontos_special = [],result_text = '',titulo = '',area = False):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setModal(True) #Bloqueia interação com a janela principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figura)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.setMinimumWidth(300)
        #self.figura.set_visible(False)
        ax = self.figura.add_subplot(111)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title("Gráfico")
        #ax.set_ylim(bottom=0.0)

        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')

        # 3. Move os espinhos da esquerda e de baixo para a posição 0
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')

        # 4. (Opcional) Aumenta a ordem Z para que fiquem sobre os dados
        ax.spines['left'].set_zorder(10)
        ax.spines['bottom'].set_zorder(10)
        ax.grid(True)
        ax.axhline(y=0, color='black')
        ax.axvline(x=0, color='black')

        ax.plot(x_pontos,y_pontos,label="Pontos",marker='o')
        if area:
            ax.fill_between(x_pontos, y_pontos, color='blue', alpha=0.6, label='Área sob a curva')
        if x_pontos_special and y_pontos_special:
            ax.scatter(x_pontos_special,y_pontos_special, c=['red']*len(x_pontos_special)) #Sem s=100
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas,stretch=1)
        self.resultado = QLabel(f"{result_text} {resultado:.6f}")
        self.resultado.setStyleSheet("font-size: 10pt;")
        button_row = QHBoxLayout()
        #button_row.addWidget(self.)
        main_layout.addWidget(self.resultado)
        self.grafico_btn = QPushButton("Mostrar")
        self.voltar_btn = QPushButton("Voltar")
        button_row.addWidget(self.grafico_btn)
        button_row.addWidget(self.voltar_btn)

        self.grafico_btn.clicked.connect(self.controla_grafico)
        self.voltar_btn.clicked.connect(self.close)

        main_layout.addLayout(button_row)
        self.toolbar.setVisible(False)
        self.canvas.setVisible(False)

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
                                            ResultadoIntegral{
                                            background-color: #A6C0ED
                                            }
                                        ''')
    def controla_grafico(self):
        if self.grafico_btn.text() == "Mostrar":
            self.toolbar.setVisible(True)
            self.canvas.setVisible(True)
            self.grafico_btn.setText("Esconder")
        else:
            self.toolbar.setVisible(False)
            self.canvas.setVisible(False)
            self.grafico_btn.setText("Mostrar")
        self.adjustSize()


class DynamicStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def sizeHint(self):
        """Retorna o sizeHint do widget atual"""
        if self.currentWidget():
            return self.currentWidget().sizeHint()
        return super().sizeHint()

    def minimumSizeHint(self):
        """Retorna o minimumSizeHint do widget atual"""
        if self.currentWidget():
            return self.currentWidget().minimumSizeHint()
        return super().minimumSizeHint()

class ResultadoSistema(QDialog):
    def __init__(self, parent,number_variables: int,resultado, passo_a_passo = [],titulo_janela = ''):
        super().__init__(parent)
        self.setWindowTitle(titulo_janela)
        self.current_page=0
        self.paginas = passo_a_passo

        main_layout = QVBoxLayout(self)

        self.iterNumber = QLabel("Iteração 0")
        self.iterNumber.hide()

        self.central_widget = QWidget()
        self.central_widget.hide()
        central_layout = QHBoxLayout(self.central_widget)

        self.previous_btn = QPushButton('<')
        self.previous_btn.setStyleSheet("font-weight: bold;font-size: 15px;")
        self.previous_btn.setEnabled(False)
        self.next_btn = QPushButton('>')
        self.next_btn.setStyleSheet("font-weight: bold;font-size: 15px;")

        if len(self.paginas) <= 1:
            self.next_btn.hide()
            self.previous_btn.hide()

        self.alternar_btn = QPushButton("Passo-a-passo")

        self.matrix = QGridLayout()
        #main_layout.addLayout(self.matrix)
        for i in range(number_variables):
            new_variable = QLabel(f"X{i+1}")
            new_variable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            new_variable.setStyleSheet("font-size: 16px;font-weight: bold;")
            self.matrix.addWidget(new_variable, 0, i)

        label_b = QLabel("B")
        label_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_b.setStyleSheet("font-size: 16px;font-weight: bold;")
        self.matrix.addWidget(label_b, 0, number_variables)
        self.label_matrix = []
        matriz_atual = self.paginas[0] #passo_a_passo é uma lista tripla, considerando não-iterativo
        for i in range(number_variables):
            linha = []
            for j in range(number_variables+1):
                new_label = QLabel(f"{matriz_atual[i][j]:.3g}")
                new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                new_label.setStyleSheet("font-size: 16px; background-color: white; color: black;")
                linha.append(new_label)
                self.matrix.addWidget(new_label, i+1, j)
            self.label_matrix.append(linha)
        self.resultLabel = QLabel(resultado)

        central_layout.addWidget(self.previous_btn)
        central_layout.addLayout(self.matrix)
        central_layout.addWidget(self.next_btn)

        main_layout.addWidget(self.iterNumber)
        main_layout.addWidget(self.central_widget)
        main_layout.addWidget(self.resultLabel)
        main_layout.addWidget(self.alternar_btn)

        self.previous_btn.clicked.connect(self.mudar_pagina)
        self.next_btn.clicked.connect(self.mudar_pagina)
        self.alternar_btn.clicked.connect(self.alternar)


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
                                ResultadoSistema{
                                background-color: #A6C0ED
                                }
                                ''')

    def mudar_pagina(self):
        if self.sender() == self.next_btn:
            self.current_page += 1
            self.previous_btn.setEnabled(True)
        else:
            self.current_page -= 1
            self.next_btn.setEnabled(True)
        if self.current_page == 0:
            self.previous_btn.setEnabled(False)
        elif self.current_page == len(self.paginas)-1:
            self.next_btn.setEnabled(False)
        self.iterNumber.setText(f"Iteração {self.current_page}")
        for i in range(len(self.label_matrix)):
            for j in range(len(self.label_matrix[i])):
                self.label_matrix[i][j].setText(f"{self.paginas[self.current_page][i][j]:.3g}")

    def alternar(self):
        if self.alternar_btn.text() == "Passo-a-passo":
            self.resultLabel.hide()
            self.central_widget.show()
            self.iterNumber.show()
            self.alternar_btn.setText("Resultado")
        else:
            self.resultLabel.show()
            self.central_widget.hide()
            self.iterNumber.hide()
            self.alternar_btn.setText("Passo-a-passo")
        self.central_widget.updateGeometry()
        self.resultLabel.updateGeometry()
        self.iterNumber.updateGeometry()
        QTimer.singleShot(0,self.adjustSize)

class ResultadoSistemaIterativo(QDialog):
    def __init__(self,parent, number_variables: int, resultado: str,passo_a_passo=[],
                 matriz_organizada = [], diferencas_relativas=[],titulo_janela = ''):
        super().__init__(parent)
        self.setWindowTitle(titulo_janela)
        self.current_page = 0
        self.paginas = passo_a_passo
        self.differences = diferencas_relativas #Teoricamente tem um elemento a menos que páginas

        main_layout = QVBoxLayout(self)

        self.iterNumber = QLabel("Matriz reorganizada")
        self.iterNumber.hide()
        self.central_widget = QWidget()
        self.central_widget.hide()
        self.central_layout = QHBoxLayout(self.central_widget)

        self.previous_btn = QPushButton('<')
        self.previous_btn.setStyleSheet("font-weight: bold;font-size: 15px;")
        self.previous_btn.setEnabled(False)
        self.next_btn = QPushButton('>')
        self.next_btn.setStyleSheet("font-weight: bold;font-size: 15px;")

        if len(self.paginas) <= 1:
            self.next_btn.hide()
            self.previous_btn.hide()

        self.stacked_central = DynamicStackedWidget()

        self.alternar_btn = QPushButton("Passo-a-passo")

        self.widgetMatrizSistema = QWidget()
        self.layoutMatrizSistema = QGridLayout(self.widgetMatrizSistema)

        self.widgetResultado = QWidget()
        self.layoutResultado = QGridLayout(self.widgetResultado)

        #Preencher a matriz do sistema
        for i in range(number_variables):
            new_variable = QLabel(f"X{i+1}")
            new_variable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            new_variable.setStyleSheet("font-size: 16px;font-weight: bold;")
            self.layoutMatrizSistema.addWidget(new_variable, 0, i)
        label_b = QLabel("B")
        label_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_b.setStyleSheet("font-size: 16px;font-weight: bold;")
        self.layoutMatrizSistema.addWidget(label_b, 0, number_variables)
        self.label_matrix = [] #Talvez não precise disso
        for i in range(number_variables):
            linha = []
            for j in range(number_variables+1):
                new_label = QLabel(f"{matriz_organizada[i][j]:.3g}")
                new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                new_label.setStyleSheet("font-size: 16px; background-color: white; color: black;")
                linha.append(new_label)
                self.layoutMatrizSistema.addWidget(new_label, i+1, j)
            self.label_matrix.append(linha)
        self.resultLabel = QLabel(resultado)

        #Preencher a iteração 0 dos resultados
        for i in range(number_variables):
            new_variable = QLabel(f"X{i + 1}")
            new_variable.setAlignment(Qt.AlignmentFlag.AlignCenter)
            new_variable.setStyleSheet("font-size: 16px;font-weight: bold;")
            self.layoutResultado.addWidget(new_variable, 0, i)
        label_dif = QLabel("Dif")
        label_dif.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_dif.setStyleSheet("font-size: 16px;font-weight: bold;")
        self.layoutResultado.addWidget(label_dif, 0, number_variables)

        self.resultLabelList = []
        for i in range(number_variables):
            new_label = QLabel(f"{passo_a_passo[0][i]:.3g}")
            new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            new_label.setStyleSheet("font-size: 16px; background-color: white; color: black;")
            self.resultLabelList.append(new_label)
            self.layoutResultado.addWidget(new_label, 1, i)

        label_dif_valor = QLabel(f"{diferencas_relativas[0]:.3g}")
        label_dif_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_dif_valor.setStyleSheet("font-size: 16px; background-color: white; color: black;")
        self.resultLabelList.append(label_dif_valor)
        self.layoutResultado.addWidget(label_dif_valor, 1, number_variables)

        self.resultLabelPrincipal = QLabel(resultado)
        self.alternar_btn = QPushButton("Passo-a-passo")

        main_layout.addWidget(self.iterNumber)

        self.central_layout.addWidget(self.previous_btn)
        self.central_layout.addWidget(self.stacked_central)
        self.central_layout.addWidget(self.next_btn)
        main_layout.addWidget(self.central_widget)

        self.stacked_central.addWidget(self.widgetMatrizSistema)
        self.stacked_central.addWidget(self.widgetResultado)

        main_layout.addWidget(self.resultLabelPrincipal)
        main_layout.addWidget(self.alternar_btn)

        self.previous_btn.clicked.connect(self.mudar_pagina)
        self.next_btn.clicked.connect(self.mudar_pagina)
        self.alternar_btn.clicked.connect(self.alternar)

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
                                        ResultadoSistemaIterativo{
                                        background-color: #A6C0ED
                                        }
                                        ''')

    def mudar_pagina(self):
        if self.sender() == self.next_btn:
            self.current_page += 1
            self.previous_btn.setEnabled(True)
            self.stacked_central.setCurrentWidget(self.widgetResultado)
        else:
            self.current_page -= 1
            self.next_btn.setEnabled(True)

        if self.current_page == 0:
            self.stacked_central.setCurrentWidget(self.widgetMatrizSistema)
            self.previous_btn.setEnabled(False)
            self.iterNumber.setText("Matriz reorganizada")
        elif self.current_page == len(self.paginas): #Como eu acesso os índices subtraindo 1, pra acessar o último elemento eu coloco sem -1 aqui
            self.next_btn.setEnabled(False)

        if self.current_page > 0:
            self.iterNumber.setText(f"Iteração {self.current_page - 1}")

            for i in range(len(self.resultLabelList)-1):
                self.resultLabelList[i].setText(f"{self.paginas[self.current_page-1][i]:.3g}")
            if self.current_page > 1:
                self.resultLabelList[-1].setText(f"{self.differences[self.current_page-2]:.3g}")
            else:
                self.resultLabelList[-1].setText("-")

    def alternar(self):
        if self.alternar_btn.text() == "Passo-a-passo":
            self.resultLabelPrincipal.hide()
            self.central_widget.show()
            self.iterNumber.show()
            self.alternar_btn.setText("Resultado")
        else:
            self.resultLabelPrincipal.show()
            self.central_widget.hide()
            self.iterNumber.hide()
            self.alternar_btn.setText("Passo-a-passo")
        self.central_widget.updateGeometry()
        self.resultLabelPrincipal.updateGeometry()
        self.iterNumber.updateGeometry()
        QTimer.singleShot(0,self.adjustSize)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    x_pontos = [1.0,1.4,1.8,2.2,2.6,3.0,3.4,3.8,4.2,4.6,5.0]
    y_pontos = [0.0, 0.3365, 0.5878, 0.7885, 0.9555, 1.0986, 1.2238, 1.3350, 1.4351, 1.5261, 1.6094]
    window = ResultadoIntegral("Resultado da Integral",None,1.5,x_pontos,y_pontos)
    window.show()
    sys.exit(app.exec())