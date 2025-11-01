import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout
)
from PySide6.QtCore import Qt


class MatrixApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Matriz")
        self.setGeometry(100, 100, 400, 300)

        self.num_rows = 2 #O número de linhas é igual ao de colunas porque tem os labels (Variáveis)
        self.num_cols = 2 #Geralmente num_cols seria igual a num_linhas+1

        # 1. Nosso modelo de dados para armazenar os valores (começa vazio)
        self.matrix_data = []
        # Manter uma referência aos widgets para fácil acesso
        self.matrix_widgets = []

        self.setup_ui()
        # Cria a matriz inicial (agora preenche self.matrix_data com "0")
        self.rebuild_matrix_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self) #Empilha verticalmente os elementos

        label_matrix_a = QLabel("Matriz A:")
        label_matrix_a.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_matrix_a)

        self.matrix_grid_layout = QGridLayout()
        self.matrix_container = QWidget()
        self.matrix_container.setLayout(self.matrix_grid_layout) #setLayout geralmente é usado pra janela principal

        main_layout.addWidget(self.matrix_container,stretch=1) #stretch=1 deixa a matriz mais distante do label

        control_buttons_layout = QHBoxLayout() #Os botões aparecem horizontalmente
        control_buttons_layout.addStretch(1) #Adiciona inicialmente um espaço antes, e depois um no final

        btn_add = QPushButton("+")
        btn_add.setFixedSize(40, 40)
        btn_add.clicked.connect(self.increase_dimensions)
        control_buttons_layout.addWidget(btn_add)

        btn_subtract = QPushButton("-")
        btn_subtract.setFixedSize(40, 40)
        btn_subtract.clicked.connect(self.decrease_dimensions)
        control_buttons_layout.addWidget(btn_subtract)

        control_buttons_layout.addStretch(1) #Ajuda a centralizar os botões, é parecido com um spacer() do swift
        main_layout.addLayout(control_buttons_layout)

        main_layout.addStretch(1)

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
            return

        # Atualiza self.matrix_data com os valores dos QLineEdit
        for row in range(len(self.matrix_widgets)):
            for col in range(len(self.matrix_widgets[row])):
                self.matrix_data[row+1][col] = self.matrix_widgets[row][col].text()
        print("Matrix data agora eh:")
        print(self.matrix_data)

    #Preciso atualizar isso pra aparecer X0,X1 etc no topo da matriz
    def rebuild_matrix_ui(self):
        """Limpa e reconstrói a UI da matriz com base nos dados e dimensões atuais."""

        # --- 1. Atualiza o Modelo de Dados ---
        # Cria uma nova matriz de dados (lista de listas) com as novas dimensões
        new_data = [["0"] * self.num_cols for _ in range(self.num_rows)]

        #print("\nNew data eh:")
        #print(new_data)
        #row_X_label = [] #Uma lista de QLabel


        # Copia os valores antigos da matriz de dados (se existirem)
        if self.matrix_data:
            # Pega o menor tamanho entre o antigo e o novo para evitar erros
            rows_to_copy = min(len(self.matrix_data), self.num_rows)
            cols_to_copy = min(len(self.matrix_data[0]), self.num_cols) #len(self.matrix_data[0]) é o número de colunas

            for row in range(rows_to_copy):
                for col in range(cols_to_copy):
                    new_data[row][col] = self.matrix_data[row][col]
        #matrix_data é uma matriz de strings
        self.matrix_data = new_data  # O modelo de dados agora está atualizado

        print("\nNew data eh:")
        print(new_data)
        # --- 2. Limpa a UI Antiga ---
        self.clear_layout(self.matrix_grid_layout)
        self.matrix_widgets = []  # Limpa a lista de referências de widgets

        for i in range(self.num_cols-1): #-1 por que o termo independente não é variável
            new_variable = QLabel(f"X{i}")
            new_variable.setAlignment(Qt.AlignCenter)
            #new_variable.setFixedSize(50, 30)
            self.matrix_grid_layout.addWidget(new_variable, 0, i)

        # --- 3. Recria a UI com os Dados Atualizados ---
        for row in range(1,self.num_rows):
            row_widgets = []  # Lista para os widgets desta linha
            for col in range(self.num_cols):
                line_edit = QLineEdit(self)
                line_edit.setFixedSize(50, 30)
                line_edit.setAlignment(Qt.AlignCenter)

                # Preenche o QLineEdit com o valor do nosso modelo de dados
                line_edit.setText(str(self.matrix_data[row][col]))
                #Coloca LineEdit em sua posição na grid
                self.matrix_grid_layout.addWidget(line_edit, row, col)
                row_widgets.append(line_edit)  # Adiciona à lista da linha

            self.matrix_widgets.append(row_widgets)  # Adiciona a linha à matriz de widgets

        self.matrix_grid_layout.setAlignment(Qt.AlignCenter)

    def increase_dimensions(self):
        """Aumenta as dimensões e reconstrói a UI preservando os dados."""
        # 1. Salva os valores atuais da UI no self.matrix_data
        self.sync_data_from_ui()

        # 2. Aumenta as dimensões
        self.num_rows += 1
        self.num_cols += 1

        # 3. Reconstrói a UI (a função agora sabe como preservar os dados)
        self.rebuild_matrix_ui()

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
            print("Não é possível diminuir mais as dimensões da matriz.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixApp()
    window.show()
    sys.exit(app.exec())