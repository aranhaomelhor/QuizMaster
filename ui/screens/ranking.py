# ui/screens/ranking.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles import ROXO, AZUL, TEXTO_SUAVE
from core.ranking import carregar_ranking, limpar_ranking

class TelaRanking(QWidget):
    voltar_clicado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._montar_interface()

    def _montar_interface(self):
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(40, 30, 40, 30)
        self.layout_principal.setSpacing(20)

        # Título
        titulo = QLabel("🏆  Melhores Jogadores")
        titulo.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {ROXO};")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_principal.addWidget(titulo)

        # Área de rolagem
        self.area_rolagem = QScrollArea()
        self.area_rolagem.setWidgetResizable(True)
        self.area_rolagem.setStyleSheet("background: transparent; border: none;")
        
        self.widget_lista = QWidget()
        self.layout_lista = QVBoxLayout(self.widget_lista)
        self.layout_lista.setSpacing(10)
        self.layout_lista.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.area_rolagem.setWidget(self.widget_lista)
        
        self.layout_principal.addWidget(self.area_rolagem)

        # --- BOTÕES DO RODAPÉ ---
        from PyQt6.QtWidgets import QHBoxLayout
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(20)
        
        # Botão Voltar
        botao_voltar = QPushButton("Voltar ao Menu")
        botao_voltar.setObjectName("botaoSecundario")
        botao_voltar.setMinimumSize(200, 45)
        botao_voltar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_voltar.clicked.connect(self.voltar_clicado)

        # Botão Zerar Ranking (estilo de perigo, discreto)
        botao_zerar = QPushButton("🗑️  Zerar Ranking")
        botao_zerar.setMinimumSize(200, 45)
        botao_zerar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_zerar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ef4444;
                border: 2px solid #ef4444;
                border-radius: 14px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(239, 68, 68, 0.2);
            }
        """)
        botao_zerar.clicked.connect(self._confirmar_zerar)

        layout_botoes.addWidget(botao_zerar)
        layout_botoes.addWidget(botao_voltar)
        
        self.layout_principal.addLayout(layout_botoes)

    def atualizar_lista(self):
        # Limpa a lista antiga
        for i in reversed(range(self.layout_lista.count())): 
            widget = self.layout_lista.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        ranking = carregar_ranking()

        if not ranking:
            label_vazio = QLabel("Ninguém jogou ainda. Seja o primeiro!")
            label_vazio.setStyleSheet(f"font-size: 18px; color: {TEXTO_SUAVE};")
            label_vazio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout_lista.addWidget(label_vazio)
            return

        for posicao, jogador in enumerate(ranking, start=1):
            if posicao == 1: cor_pos = "gold"
            elif posicao == 2: cor_pos = "silver"
            elif posicao == 3: cor_pos = "#cd7f32"
            else: cor_pos = TEXTO_SUAVE

            # Como tiramos os avatares, deixamos apenas o nome e os acertos
            linha = QLabel(
                f"{posicao}º   {jogador['nome']}   "
                f"—   {jogador['acertos']}/{jogador['total']} acertos"
            )
            linha.setStyleSheet(f"""
                font-size: 18px; 
                color: {cor_pos}; 
                background-color: #15152b;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            """)
            self.layout_lista.addWidget(linha)

    def _confirmar_zerar(self):
        """Pergunta se o usuário tem certeza antes de apagar os dados."""
        resposta = QMessageBox.question(
            self, "Zerar Ranking", 
            "Tem certeza que deseja apagar TODAS as pontuações?\nEssa ação não pode ser desfeita.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            limpar_ranking()
            self.atualizar_lista() # Atualiza a tela na hora para mostrar que esvaziou
            QMessageBox.information(self, "Ranking", "O ranking foi zerado com sucesso! 🗑️")