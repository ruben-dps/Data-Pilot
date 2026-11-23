from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARQUIVO_ENTRADA = DATA_DIR / "sales.csv"
ARQUIVO_SAIDA = DATA_DIR / "sales_limpo.csv"

def carregar_dados(caminho=ARQUIVO_ENTRADA):
    """Lê o CSV original e valida as colunas esperadas."""
    df = pd.read_csv(caminho, sep=None, engine="python")
    colunas_obrigatorias = {
        "pedido_id", "data", "produto", "categoria", "cliente_id",
        "cidade", "canal", "quantidade", "preco_unitario", "status"
    }
    faltantes = colunas_obrigatorias - set(df.columns)
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(sorted(faltantes))}")
    return df

def limpar_dados(df):
    """Padroniza campos, remove duplicidades e cria a coluna de receita."""
    dados = df.copy()
    dados.columns = dados.columns.str.strip().str.lower()
    dados["data"] = pd.to_datetime(dados["data"], errors="coerce")
    dados["status"] = dados["status"].astype("string").str.strip().str.lower()
    dados["categoria"] = dados["categoria"].astype("string").str.strip()
    dados["cidade"] = dados["cidade"].astype("string").str.strip()
    dados["canal"] = dados["canal"].astype("string").str.strip()
    dados["quantidade"] = pd.to_numeric(dados["quantidade"], errors="coerce")
    dados["preco_unitario"] = pd.to_numeric(dados["preco_unitario"], errors="coerce")

    dados = dados.dropna(subset=[
        "pedido_id", "data", "produto", "categoria", "cliente_id",
        "quantidade", "preco_unitario", "status"
    ])
    dados = dados.drop_duplicates()
    dados = dados.drop_duplicates(subset=["pedido_id"], keep="first")
    dados = dados[dados["quantidade"] > 0]
    dados = dados[dados["preco_unitario"] >= 0]
    dados["receita"] = (dados["quantidade"] * dados["preco_unitario"]).round(2)
    dados = dados.sort_values(["data", "pedido_id"]).reset_index(drop=True)
    return dados

def salvar_dados(dados, caminho=ARQUIVO_SAIDA):
    """Salva com ponto e vírgula e vírgula decimal, conforme o desafio."""
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    dados.to_csv(caminho, sep=";", decimal=",", index=False, date_format="%Y-%m-%d")
    return caminho

def preparar_base():
    original = carregar_dados()
    limpo = limpar_dados(original)
    salvar_dados(limpo)
    return limpo

if __name__ == "__main__":
    resultado = preparar_base()
    print(f"Arquivo tratado: {ARQUIVO_SAIDA}")
    print(f"Registros originais: {len(carregar_dados())}")
    print(f"Registros após limpeza: {len(resultado)}")
    print(f"Colunas finais: {', '.join(resultado.columns)}")
