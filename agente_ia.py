import json
import os
from datetime import date
from openai import OpenAI
from metricas import obter_base, filtrar_periodo, calcular_metricas, receita_mensal, top_cidades, receita_media_por_cliente

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_indicadores",
            "description": "Calcula os indicadores gerais ou de uma categoria no período informado. Use para perguntas sobre receita, pedidos, ticket médio, clientes e cancelamentos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data_inicio": {"type": "string", "description": "Data inicial no formato AAAA-MM-DD. Opcional."},
                    "data_fim": {"type": "string", "description": "Data final no formato AAAA-MM-DD. Opcional."},
                    "categoria": {"type": "string", "description": "Categoria exata ou Todas. Opcional."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_receita_mensal",
            "description": "Retorna a receita de pedidos concluídos agrupada por mês.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_top_cidades",
            "description": "Retorna as cinco cidades com maior receita de pedidos concluídos.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_receita_media_cliente",
            "description": "Calcula a receita média por cliente único considerando pedidos concluídos.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

def executar_ferramenta(nome, argumentos):
    df = obter_base()
    if nome == "consultar_indicadores":
        filtrado = filtrar_periodo(
            df,
            argumentos.get("data_inicio"),
            argumentos.get("data_fim"),
            argumentos.get("categoria")
        )
        return calcular_metricas(filtrado)
    if nome == "consultar_receita_mensal":
        return receita_mensal(df).to_dict(orient="records")
    if nome == "consultar_top_cidades":
        return top_cidades(df).to_dict(orient="records")
    if nome == "consultar_receita_media_cliente":
        return {"receita_media_por_cliente": receita_media_por_cliente(df)}
    return {"erro": f"Ferramenta não reconhecida: {nome}"}

def responder(pergunta, historico=None):
    chave = os.getenv("OPENROUTER_API_KEY")
    if not chave:
        raise RuntimeError("Configure OPENROUTER_API_KEY no arquivo .env.")
    cliente = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=chave,
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Data Pilot - Dashboard de Vendas"
        }
    )
    modelo = os.getenv("OPENROUTER_MODEL", "openrouter/free")
    mensagens = [{
        "role": "system",
        "content": (
            "Você é o assistente do Data Pilot, um painel de análise de vendas. "
            "Responda em português, de forma clara e objetiva. "
            "Use as ferramentas para obter números; nunca invente métricas nem faça cálculos "
            "de cabeça. Python é responsável pelos cálculos e você apenas interpreta e explica "
            "os resultados. Informe quando os dados não forem suficientes."
        )
    }]
    if historico:
        mensagens.extend(historico[-8:])
    mensagens.append({"role": "user", "content": pergunta})

    for _ in range(5):
        resposta = cliente.chat.completions.create(
            model=modelo,
            messages=mensagens,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )
        mensagem = resposta.choices[0].message
        if not mensagem.tool_calls:
            return mensagem.content or "Não consegui formular uma resposta."
        mensagens.append(mensagem.model_dump(exclude_none=True))
        for chamada in mensagem.tool_calls:
            nome = chamada.function.name
            try:
                argumentos = json.loads(chamada.function.arguments or "{}")
                resultado = executar_ferramenta(nome, argumentos)
            except Exception as erro:
                resultado = {"erro": str(erro)}
            mensagens.append({
                "role": "tool",
                "tool_call_id": chamada.id,
                "content": json.dumps(resultado, ensure_ascii=False, default=str)
            })
    return "A consulta exigiu muitas etapas. Tente reformular a pergunta."
