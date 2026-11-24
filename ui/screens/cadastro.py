# ui/screens/cadastro.py
# Tela de cadastro simplificada: apenas o nome do jogador.

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles import ROXO

class TelaCadastro(QWidget):
    comecar_clicado = pyqtSignal(str, str)
    voltar_clicado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._montar_interface()

    def _montar_interface(self):
        centro = Qt.AlignmentFlag.AlignCenter
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(centro)

        # Título
        titulo = QLabel("Quem está jogando?")
        titulo.setStyleSheet(f"font-size: 36px; font-weight: bold; color: {ROXO};")
        titulo.setAlignment(centro)

        # Campo de Nome
        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Digite seu nome aqui...")
        self.campo_nome.setMaxLength(15)
        self.campo_nome.setAlignment(centro)
        self.campo_nome.setFixedWidth(350)
        self.campo_nome.setStyleSheet("""
            QLineEdit {
                background-color: #15152b;
                border: 2px solid #3b82f6;
                border-radius: 10px;
                padding: 12px;
                font-size: 18px;
                color: white;
            }
        """)

        # Botões de Ação
        botao_comecar = QPushButton("▶   COMEÇAR")
        botao_comecar.setObjectName("botaoPrimario")
        botao_comecar.setMinimumSize(300, 55)
        botao_comecar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_comecar.clicked.connect(self._ao_comecar)

        botao_voltar = QPushButton("Voltar")
        botao_voltar.setObjectName("botaoSecundario")
        botao_voltar.setMinimumSize(300, 45)
        botao_voltar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_voltar.clicked.connect(self.voltar_clicado)

        # Montagem na tela (tudo centralizado)
        layout.addStretch(1)
        layout.addWidget(titulo)
        layout.addSpacing(20)
        layout.addWidget(self.campo_nome, alignment=centro)
        layout.addSpacing(40)
        layout.addWidget(botao_comecar, alignment=centro)
        layout.addWidget(botao_voltar, alignment=centro)
        layout.addStretch(1)

    def _ao_comecar(self):
        nome = self.campo_nome.text().strip()
        if not nome:
            self.campo_nome.setPlaceholderText("Por favor, digite seu nome!")
            self.campo_nome.setStyleSheet("""
                QLineEdit {
                    background-color: #15152b;
                    border: 2px solid #ef4444; 
                    border-radius: 10px; 
                    padding: 12px; 
                    font-size: 18px;
                    color: white;
                }
            """)
            return
            
        # Como removemos os avatares, enviamos uma string vazia no lugar
        self.comecar_clicado.emit(nome, "")