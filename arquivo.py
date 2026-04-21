import json
import os

CAMINHO_JSON = os.path.join(os.path.dirname(__file__), "dados", "estoque.json")


def _garantir_diretorio():
    """Garante que o diretório 'dados/' existe."""
    os.makedirs(os.path.dirname(CAMINHO_JSON), exist_ok=True)


def carregar_dados() -> dict:
    """
    Carrega os dados do arquivo JSON.
    Retorna um dicionário com as chaves 'estoque' e 'historico'.
    """
    _garantir_diretorio()
    if not os.path.exists(CAMINHO_JSON):
        return {"estoque": {}, "historico": []}

    try:
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("[AVISO] Arquivo de dados corrompido. Iniciando do zero.")
        return {"estoque": {}, "historico": []}


def salvar_dados(dados: dict) -> bool:
    """Salva o dicionário de dados no arquivo JSON."""
    _garantir_diretorio()
    try:
        with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return True
    except IOError as e:
        print(f"[ERRO] Não foi possível salvar os dados: {e}")
        return False


def exportar_relatorio_txt(conteudo: str, caminho: str) -> bool:
    """Exporta um relatório em formato .txt no caminho especificado."""
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return True
    except IOError as e:
        print(f"[ERRO] Não foi possível exportar o relatório: {e}")
        return False
