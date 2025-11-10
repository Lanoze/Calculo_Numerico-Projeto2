from PySide6.QtWidgets import QApplication,QDialog, QVBoxLayout,QLabel, QPushButton
from matplotlib.figure import Figure

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import sys

class ResultadoIntegral(QDialog):
    def __init__(self,titulo: str,parent,resultado: float,x_pontos: list[float],y_pontos: list[float]):
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
        ax.fill_between(x_pontos, y_pontos, color='blue', alpha=0.6, label='Área sob a curva')
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)
        self.resultado = QLabel(f"A integral resultou em {resultado:.5f}")
        self.resultado.setStyleSheet("font-size: 10pt;")
        button_row = QVBoxLayout()
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    x_pontos = [1.0,1.4,1.8,2.2,2.6,3.0,3.4,3.8,4.2,4.6,5.0]
    y_pontos = [0.0, 0.3365, 0.5878, 0.7885, 0.9555, 1.0986, 1.2238, 1.3350, 1.4351, 1.5261, 1.6094]
    window = ResultadoIntegral("Resultado da Integral",None,1.5,x_pontos,y_pontos)
    window.show()
    sys.exit(app.exec())