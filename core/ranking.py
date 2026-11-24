# core/ranking.py
import json
import os

ARQUIVO_RANKING = "data/ranking.json"

def salvar_pontuacao(nome, avatar, acertos, total):
    ranking = carregar_ranking()
    ranking.append({
        "nome": nome,
        "avatar": avatar,
        "acertos": acertos,
        "total": total
    })
    ranking.sort(key=lambda x: x["acertos"], reverse=True)
    ranking = ranking[:10]
    
    os.makedirs("data", exist_ok=True)
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=4)

def carregar_ranking():
    if not os.path.exists(ARQUIVO_RANKING):
        return []
    try:
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def limpar_ranking():
    """Apaga o arquivo de ranking do computador."""
    if os.path.exists(ARQUIVO_RANKING):
        os.remove(ARQUIVO_RANKING)