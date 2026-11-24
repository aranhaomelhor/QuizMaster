# ui/screens/quiz.py
# Tela onde o quiz acontece: mostra perguntas, opções e placar.

import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles import ROXO, AZUL, ACERTO, ERRO

from data.questions.banco import PERGUNTAS

class TelaQuiz(QWidget):
    # Sinais: avisam a janela principal quando o jogo termina
    finalizar_clicado = pyqtSignal(int, int, str, str) # acertos, total, nome, avatar

    def __init__(self):
        super().__init__()
        self.nome_jogador = ""
        self.avatar_jogador = ""
        self.acertos = 0
        self.indice_atual = 0
        self.perguntas_do_jogo = []
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Topo: Placar e Categoria
        topo = QHBoxLayout()
        self.label_categoria = QLabel("Categoria")
        self.label_categoria.setStyleSheet(f"color: {AZUL}; font-size: 18px; font-weight: bold;")
        
        self.label_placar = QLabel("Acertos: 0")
        self.label_placar.setStyleSheet("color: #9a9ac0; font-size: 18px; font-weight: bold;")
        self.label_placar.setAlignment(Qt.AlignmentFlag.AlignRight)

        topo.addWidget(self.label_categoria)
        topo.addStretch()
        topo.addWidget(self.label_placar)
        layout.addLayout(topo)

        # Pergunta
        self.label_pergunta = QLabel("Pergunta aqui...")
        self.label_pergunta.setWordWrap(True) # Permite quebrar linha
        self.label_pergunta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pergunta.setStyleSheet("font-size: 28px; font-weight: bold; margin: 30px 0px;")
        layout.addWidget(self.label_pergunta)

        # Botões de Opção
        self.botoes = []
        for i in range(4):
            btn = QPushButton(f"Opção {i+1}")
            btn.setMinimumHeight(60)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #15152b;
                    border: 2px solid #333;
                    border-radius: 10px;
                    font-size: 20px;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    border: 2px solid #7c3aed;
                    background-color: #1a1a35;
                }
            """)
            btn.clicked.connect(lambda checked, index=i: self._responder(index))
            self.botoes.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # Botão de Sair (por segurança)
        btn_sair = QPushButton("Encerrar Quiz")
        btn_sair.setStyleSheet("color: #ef4444; background: transparent; border: none; font-size: 14px;")
        btn_sair.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sair.clicked.connect(self._confirmar_saida)
        layout.addWidget(btn_sair, alignment=Qt.AlignmentFlag.AlignCenter)

    def iniciar_jogo(self, nome, avatar):
        self.nome_jogador = nome
        self.avatar_jogador = avatar
        self.acertos = 0
        self.indice_atual = 0
        
        # Embaralha as perguntas e pega as 5 primeiras
        self.perguntas_do_jogo = random.sample(PERGUNTAS, 5)
        
        self._carregar_pergunta()

    def _carregar_pergunta(self):
        if self.indice_atual >= len(self.perguntas_do_jogo):
            self._finalizar_jogo()
            return

        pergunta_atual = self.perguntas_do_jogo[self.indice_atual]
        
        # Atualiza o topo
        self.label_categoria.setText(pergunta_atual["categoria"])
        self.label_placar.setText(f"Acertos: {self.acertos}  |  Pergunta: {self.indice_atual + 1}/{len(self.perguntas_do_jogo)}")
        
        # Atualiza a pergunta
        self.label_pergunta.setText(pergunta_atual["pergunta"])

        # Atualiza os botões e reseta as cores
        for i, opcao in enumerate(pergunta_atual["opcoes"]):
            btn = self.botoes[i]
            btn.setText(f"  {chr(65+i)})  {opcao}") # Coloca A), B), C), D)
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #15152b;
                    border: 2px solid #333;
                    border-radius: 10px;
                    font-size: 20px;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    border: 2px solid #7c3aed;
                    background-color: #1a1a35;
                }
            """)

    def _responder(self, index_clicado):
        pergunta_atual = self.perguntas_do_jogo[self.indice_atual]
        correta = pergunta_atual["correta"]

        # Desabilita todos os botões para não clicar duas vezes
        for btn in self.botoes:
            btn.setEnabled(False)

        # Pinta de verde ou vermelho
        for i, btn in enumerate(self.botoes):
            if i == correta:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(34, 197, 94, 0.2);
                        border: 2px solid #22c55e;
                        border-radius: 10px;
                        font-size: 20px;
                        text-align: left;
                        padding-left: 20px;
                        color: #22c55e;
                    }
                """)
            elif i == index_clicado:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(239, 68, 68, 0.2);
                        border: 2px solid #ef4444;
                        border-radius: 10px;
                        font-size: 20px;
                        text-align: left;
                        padding-left: 20px;
                        color: #ef4444;
                    }
                """)

        if index_clicado == correta:
            self.acertos += 1
            self.label_placar.setText(f"Acertos: {self.acertos}  |  Pergunta: {self.indice_atual + 1}/{len(self.perguntas_do_jogo)}")

        # Espera 1 segundo e vai para a próxima
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1200, self._proxima_pergunta)

    def _proxima_pergunta(self):
        self.indice_atual += 1
        self._carregar_pergunta()

    def _finalizar_jogo(self):
        self.finalizar_clicado.emit(self.acertos, len(self.perguntas_do_jogo), self.nome_jogador, self.avatar_jogador)

    def _confirmar_saida(self):
        resposta = QMessageBox.question(
            self, "Sair", "Tem certeza que deseja encerrar o quiz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            self.finalizar_clicado.emit(-1, -1, self.nome_jogador, self.avatar_jogador)