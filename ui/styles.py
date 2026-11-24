# ui/styles.py
# Paleta de cores e estilo (QSS) de todo o QuizMaster.

# ---------- PALETA DE CORES ----------
FUNDO = "#0b0b16"          # fundo principal (quase preto)
FUNDO_CARTAO = "#15152b"   # fundo dos cartões
AZUL = "#3b82f6"
AZUL_CLARO = "#60a5fa"
ROXO = "#7c3aed"
ROXO_CLARO = "#a78bfa"
TEXTO = "#e8e8ff"
TEXTO_SUAVE = "#9a9ac0"
ACERTO = "#22c55e"         # verde (vamos usar nas respostas certas)
ERRO = "#ef4444"           # vermelho (vamos usar nas respostas erradas)

# ---------- ESTILO GERAL (QSS) ----------
# Como é um f-string, as chaves do CSS precisam ser duplicadas: {{ }}
ESTILO = f"""
QWidget {{
    background-color: {FUNDO};
    color: {TEXTO};
    font-family: 'Segoe UI';
    font-size: 16px;
}}

QLabel {{
    background: transparent;
}}

QLabel#icone {{
    font-size: 80px;
}}

QLabel#titulo {{
    font-size: 68px;
    font-weight: bold;
    color: {ROXO_CLARO};
}}

QLabel#subtitulo {{
    font-size: 22px;
    color: {AZUL_CLARO};
    letter-spacing: 4px;
}}

QLabel#categorias {{
    font-size: 40px;
}}

QLabel#rodape {{
    font-size: 13px;
    color: {TEXTO_SUAVE};
}}

QPushButton {{
    background-color: {ROXO};
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 32px;
    font-size: 18px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {ROXO_CLARO};
}}

QPushButton#botaoPrimario {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 {AZUL}, stop:1 {ROXO});
}}

QPushButton#botaoPrimario:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 {AZUL_CLARO}, stop:1 {ROXO_CLARO});
}}

QPushButton#botaoSecundario {{
    background-color: transparent;
    border: 2px solid {ROXO};
    color: {ROXO_CLARO};
}}

QPushButton#botaoSecundario:hover {{
    background-color: {FUNDO_CARTAO};
    border: 2px solid {ROXO_CLARO};
}}
"""