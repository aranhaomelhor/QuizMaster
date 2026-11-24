# ui/screens/home.py
# Tela inicial do QuizMaster: título, ícones das categorias e botões.

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation
from PyQt6.QtGui import QColor

from ui.styles import ROXO_CLARO, AZUL


class TelaInicial(QWidget):
    # Sinais: "avisos" que a tela envia quando algo acontece.
    # Quem decide o que fazer com o aviso é a janela principal.
    jogar_clicado = pyqtSignal()
    ranking_clicado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._montar_interface()
        self._iniciar_animacao_brilho()

    def _montar_interface(self):
        centro = Qt.AlignmentFlag.AlignCenter

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 30)
        layout.setSpacing(0)

        # --- Textos ---
        icone = QLabel("🧠")
        icone.setObjectName("icone")

        titulo = QLabel("QuizMaster")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("DESAFIO DO CONHECIMENTO")
        subtitulo.setObjectName("subtitulo")

        categorias = QLabel("🔬   📜   🌍   ➗")
        categorias.setObjectName("categorias")

        rodape = QLabel("Projeto escolar  •  Feito com Python e PyQt6")
        rodape.setObjectName("rodape")

        # --- Botões ---
        botao_jogar = QPushButton("▶   JOGAR")
        botao_jogar.setObjectName("botaoPrimario")
        botao_jogar.setMinimumSize(300, 58)
        botao_jogar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_jogar.clicked.connect(self.jogar_clicado)

        botao_ranking = QPushButton("🏆   RANKING")
        botao_ranking.setObjectName("botaoSecundario")
        botao_ranking.setMinimumSize(300, 58)
        botao_ranking.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_ranking.clicked.connect(self.ranking_clicado)

        # --- Efeitos de brilho (neon) ---
        self.brilho_titulo = self._aplicar_brilho(titulo, ROXO_CLARO, 30)
        self._aplicar_brilho(botao_jogar, AZUL, 35)

        # --- Montagem na tela (de cima para baixo) ---
        layout.addStretch(2)
        layout.addWidget(icone, alignment=centro)
        layout.addSpacing(10)
        layout.addWidget(titulo, alignment=centro)
        layout.addWidget(subtitulo, alignment=centro)
        layout.addSpacing(30)
        layout.addWidget(categorias, alignment=centro)
        layout.addSpacing(45)
        layout.addWidget(botao_jogar, alignment=centro)
        layout.addSpacing(18)
        layout.addWidget(botao_ranking, alignment=centro)
        layout.addStretch(3)
        layout.addWidget(rodape, alignment=centro)

    def _aplicar_brilho(self, widget, cor, raio):
        """Coloca uma sombra colorida e sem deslocamento, que parece um brilho."""
        efeito = QGraphicsDropShadowEffect(self)
        efeito.setOffset(0, 0)
        efeito.setBlurRadius(raio)
        efeito.setColor(QColor(cor))
        widget.setGraphicsEffect(efeito)
        return efeito

    def _iniciar_animacao_brilho(self):
        """Faz o brilho do título aumentar e diminuir, em loop infinito."""
        self.anim_brilho = QPropertyAnimation(self.brilho_titulo, b"blurRadius", self)
        self.anim_brilho.setDuration(2500)
        self.anim_brilho.setKeyValueAt(0.0, 15)   # começa fraco
        self.anim_brilho.setKeyValueAt(0.5, 55)   # no meio fica forte
        self.anim_brilho.setKeyValueAt(1.0, 15)   # volta a ficar fraco
        self.anim_brilho.setLoopCount(-1)         # -1 = repete para sempre
        self.anim_brilho.start()