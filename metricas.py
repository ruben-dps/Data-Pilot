from pathlib import Path
import pandas as pd
from limpeza import ARQUIVO_SAIDA, preparar_base

def obter_base(caminho=ARQUIVO_SAIDA):
    caminho = Path(caminho)
    if not caminho.exists():
        preparar_base()
    df = pd.read_csv(caminho, sep=";", decimal=",", parse_dates=["data"])
    df["status"] = df["status"].astype(str).str.strip().str.lower()
    return df

def filtrar_periodo(df, data_inicio=None, data_fim=None, categoria=None):
    resultado = df.copy()
    if data_inicio:
        resultado = resultado[resultado["data"] >= pd.to_datetime(data_inicio)]
    if data_fim:
        resultado = resultado[resultado["data"] <= pd.to_datetime(data_fim)]
    if categoria and categoria != "Todas":
        resultado = resultado[resultado["categoria"] == categoria]
    return resultado

def calcular_metricas(df):
    total = len(df)
    concluidos = df[df["status"] == "concluido"]
    cancelados = df[df["status"] == "cancelado"]
    receita = float(concluidos["receita"].sum())
    pedidos = int(concluidos["pedido_id"].nunique())
    clientes = int(concluidos["cliente_id"].nunique())
    return {
        "receita_total": round(receita, 2),
        "pedidos_concluidos": pedidos,
        "ticket_medio": round(receita / pedidos, 2) if pedidos else 0.0,
        "clientes_unicos": clientes,
        "taxa_cancelamento": round((len(cancelados) / total) * 100, 2) if total else 0.0,
        "pedidos_cancelados": int(cancelados["pedido_id"].nunique()),
        "total_registros": int(total),
    }

def receita_mensal(df):
    concluidos = df[df["status"] == "concluido"].copy()
    if concluidos.empty:
        return pd.DataFrame(columns=["mes", "receita"])
    concluidos["mes"] = concluidos["data"].dt.to_period("M").astype(str)
    return concluidos.groupby("mes", as_index=False)["receita"].sum().sort_values("mes")

def top_cidades(df, limite=5):
    concluidos = df[df["status"] == "concluido"]
    return (concluidos.groupby("cidade", as_index=False)["receita"]
            .sum().sort_values("receita", ascending=False).head(limite))

def receita_media_por_cliente(df):
    concluidos = df[df["status"] == "concluido"]
    clientes = concluidos["cliente_id"].nunique()
    return round(float(concluidos["receita"].sum()) / clientes, 2) if clientes else 0.0
