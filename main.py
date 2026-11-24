# main.py
# Ponto de entrada do QuizMaster: cria a aplicação e abre a janela.

import sys
from PyQt6.QtWidgets import QApplication

from ui.styles import ESTILO
from ui.main_window import JanelaPrincipal


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(ESTILO)   # aplica o tema escuro a TODAS as telas

    janela = JanelaPrincipal()
    janela.show()
    janela.animar_entrada()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()