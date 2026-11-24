# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

from ui.screens.home import TelaInicial
from ui.screens.cadastro import TelaCadastro
from ui.screens.quiz import TelaQuiz
from ui.screens.ranking import TelaRanking
from core.ranking import salvar_pontuacao

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuizMaster - Desafio do Conhecimento")
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)
        self.setWindowOpacity(0.0)

        self.pilha = QStackedWidget()
        self.setCentralWidget(self.pilha)

        # Instanciando todas as telas
        self.tela_inicial = TelaInicial()
        self.tela_cadastro = TelaCadastro()
        self.tela_quiz = TelaQuiz()
        self.tela_ranking = TelaRanking()

        # Adicionando à pilha
        self.pilha.addWidget(self.tela_inicial)
        self.pilha.addWidget(self.tela_cadastro)
        self.pilha.addWidget(self.tela_quiz)
        self.pilha.addWidget(self.tela_ranking)

        # Conectando os sinais (eventos)
        self.tela_inicial.jogar_clicado.connect(self.ir_para_cadastro)
        self.tela_inicial.ranking_clicado.connect(self.ir_para_ranking)

        self.tela_cadastro.voltar_clicado.connect(self.ir_para_inicio)
        self.tela_cadastro.comecar_clicado.connect(self.ao_comecar_jogo)

        self.tela_quiz.finalizar_clicado.connect(self.ao_finalizar_quiz)
        
        self.tela_ranking.voltar_clicado.connect(self.ir_para_inicio)

    def animar_entrada(self):
        self.anim_entrada = QPropertyAnimation(self, b"windowOpacity", self)
        self.anim_entrada.setDuration(800)
        self.anim_entrada.setStartValue(0.0)
        self.anim_entrada.setEndValue(1.0)
        self.anim_entrada.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim_entrada.start()

    def ir_para_cadastro(self):
        self.pilha.setCurrentWidget(self.tela_cadastro)

    def ir_para_inicio(self):
        self.pilha.setCurrentWidget(self.tela_inicial)
        self.tela_cadastro.campo_nome.clear()

    def ir_para_ranking(self):
        self.tela_ranking.atualizar_lista() # Atualiza a lista antes de mostrar
        self.pilha.setCurrentWidget(self.tela_ranking)

    def ao_comecar_jogo(self, nome, avatar):
        self.tela_quiz.iniciar_jogo(nome, avatar)
        self.pilha.setCurrentWidget(self.tela_quiz)

    def ao_finalizar_quiz(self, acertos, total, nome, avatar):
        if acertos != -1:
            # Salva a pontuação no arquivo JSON
            salvar_pontuacao(nome, avatar, acertos, total)
            
            QMessageBox.information(
                self, "Fim de Jogo", 
                f"Muito bem, {nome} {avatar}!\nVocê acertou {acertos} de {total} perguntas.\nSua pontuação foi salva!"
            )
        else:
            QMessageBox.information(self, "QuizMaster", "Você encerrou o quiz. Voltando ao início.")
            
        self.pilha.setCurrentWidget(self.tela_inicial)