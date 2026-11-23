import os
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from limpeza import preparar_base, ARQUIVO_SAIDA
from metricas import obter_base, filtrar_periodo, calcular_metricas, receita_mensal, top_cidades, receita_media_por_cliente
from agente_ia import responder

load_dotenv()
st.set_page_config(page_title="Data Pilot | Vendas", page_icon="📊", layout="wide")

@st.cache_data
def carregar_base():
    if not Path(ARQUIVO_SAIDA).exists():
        preparar_base()
    return obter_base()

st.title("📊 Data Pilot — Análise de Vendas")
st.caption("Dashboard interativo e assistente de IA para explorar os dados de vendas.")

try:
    df = carregar_base()
except Exception as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.stop()

with st.sidebar:
    st.header("Filtros")
    categorias = ["Todas"] + sorted(df["categoria"].dropna().unique().tolist())
    categoria = st.selectbox("Categoria", categorias)
    data_min = df["data"].min().date()
    data_max = df["data"].max().date()
    periodo = st.date_input("Período", value=(data_min, data_max), min_value=data_min, max_value=data_max)
    if isinstance(periodo, tuple) and len(periodo) == 2:
        inicio, fim = periodo
    else:
        inicio, fim = data_min, data_max

dados = filtrar_periodo(df, inicio, fim, categoria)
indicadores = calcular_metricas(dados)
media_cliente = receita_media_por_cliente(dados)

st.subheader("Indicadores principais")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Receita total", f"R$ {indicadores['receita_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Pedidos concluídos", f"{indicadores['pedidos_concluidos']:,}".replace(",", "."))
c3.metric("Ticket médio", f"R$ {indicadores['ticket_medio']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c4.metric("Clientes únicos", f"{indicadores['clientes_unicos']:,}".replace(",", "."))
c5.metric("Cancelamentos", f"{indicadores['taxa_cancelamento']:.2f}%".replace(".", ","))

st.subheader("Receita ao longo dos meses")
mensal = receita_mensal(dados)
if mensal.empty:
    st.info("Não há pedidos concluídos para os filtros selecionados.")
else:
    fig = px.line(mensal, x="mes", y="receita", markers=True,
                  labels={"mes": "Mês", "receita": "Receita (R$)"},
                  title="Receita mensal — pedidos concluídos")
    fig.update_layout(xaxis_title="Mês", yaxis_title="Receita (R$)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Top 5 cidades")
    cidades = (dados[dados["status"] == "concluido"]
               .groupby("cidade", as_index=False)["receita"].sum()
               .sort_values("receita", ascending=False).head(5))
    if cidades.empty:
        st.info("Sem dados para exibir.")
    else:
        fig_cidades = px.bar(cidades, x="cidade", y="receita",
                             labels={"cidade": "Cidade", "receita": "Receita (R$)"})
        st.plotly_chart(fig_cidades, use_container_width=True)
with col_b:
    st.subheader("Receita por categoria")
    categorias_df = (dados[dados["status"] == "concluido"]
                     .groupby("categoria", as_index=False)["receita"].sum()
                     .sort_values("receita", ascending=False))
    if categorias_df.empty:
        st.info("Sem dados para exibir.")
    else:
        fig_cat = px.pie(categorias_df, names="categoria", values="receita",
                         title="Participação da receita por categoria")
        st.plotly_chart(fig_cat, use_container_width=True)

st.subheader("Indicadores complementares")
x1, x2 = st.columns(2)
x1.metric("Receita média por cliente", f"R$ {media_cliente:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
x2.metric("Pedidos cancelados", indicadores["pedidos_cancelados"])

with st.expander("Visualizar dados tratados"):
    st.dataframe(dados, use_container_width=True)
    st.download_button(
        "Baixar dados tratados (CSV)",
        data=dados.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
        file_name="sales_filtrado.csv",
        mime="text/csv"
    )

st.divider()
st.header("💬 Converse com seus dados")
st.write("Faça perguntas sobre receita, pedidos, ticket médio, cancelamentos, meses, cidades ou clientes.")

if "chat" not in st.session_state:
    st.session_state.chat = []

for item in st.session_state.chat:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

pergunta = st.chat_input("Ex.: Qual foi a receita total no período?")
if pergunta:
    st.session_state.chat.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)
    with st.chat_message("assistant"):
        with st.spinner("Consultando os dados..."):
            try:
                historico = [
                    {"role": item["role"], "content": item["content"]}
                    for item in st.session_state.chat[:-1]
                    if item["role"] in ("user", "assistant")
                ]
                resposta = responder(pergunta, historico)
            except Exception as erro:
                resposta = f"Não foi possível consultar o assistente: {erro}"
            st.markdown(resposta)
    st.session_state.chat.append({"role": "assistant", "content": resposta})
