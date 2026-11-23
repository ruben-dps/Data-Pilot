Data Pilot — Dashboard e Assistente de Vendas
Projeto desenvolvido para o desafio Data Pilot. A aplicação utiliza Python e pandas para preparar e calcular os indicadores de vendas, Streamlit para apresentar o dashboard, Plotly para os gráficos e um assistente de IA conectado à API do OpenRouter para interpretar perguntas sobre os dados.
Sumário
Objetivo
Dados utilizados
Funcionalidades
Tecnologias
Instalação
Configuração da IA
Como executar
Ferramentas do agente
Melhorias implementadas
Testes
Estrutura do projeto
Segurança
Objetivo
Criar um painel interativo para análise de vendas, permitindo acompanhar indicadores importantes e consultar os dados por meio de linguagem natural. A regra central do projeto é: Python calcula e a IA explica. Os valores apresentados pelo agente são obtidos pelas funções Python, evitando que o modelo invente ou estime resultados.
Dados utilizados
O arquivo `data/sales.csv` contém os registros fornecidos para o desafio, com as colunas:
`pedido\_id`, `data`, `produto`, `categoria`, `cliente\_id`, `cidade`, `canal`, `quantidade`, `preco\_unitario` e `status`.
A etapa de preparação:
Lê o CSV original.
Converte a coluna `data` para data.
Padroniza o campo `status` em letras minúsculas.
Remove registros incompletos e duplicidades.
Valida quantidade e preço unitário.
Cria a coluna `receita`, calculada por `quantidade × preco\_unitario`.
Salva `data/sales\_limpo.csv` com `;` como separador e `,` como separador decimal.
Os dados originais são preservados em `data/sales.csv`.
Funcionalidades
Receita total de pedidos concluídos.
Quantidade de pedidos concluídos.
Ticket médio.
Clientes únicos.
Taxa e quantidade de cancelamentos.
Filtro por categoria e período.
Gráfico de receita mensal.
Gráfico de receita por categoria.
Ranking das cinco cidades com maior receita.
Receita média por cliente.
Chat para perguntas sobre os indicadores.
Critérios dos indicadores: a receita, o número de pedidos, o ticket médio e os clientes únicos consideram somente pedidos com status `concluido`. A taxa de cancelamento é calculada dividindo a quantidade de registros cancelados pelo total de registros no recorte selecionado.
Tecnologias
Python
pandas
Streamlit
Plotly
OpenAI SDK
OpenRouter
Instalação
Recomendado: Python 3.10 ou superior.
No terminal, dentro da pasta do projeto:
```bash
python -m venv .venv
```
Ative o ambiente virtual no Windows:
```bash
.venv\\Scripts\\activate
```
No Linux/macOS:
```bash
source .venv/bin/activate
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
Configuração da IA
Crie uma conta em OpenRouter.
Gere uma chave de API.
Faça uma cópia do arquivo `.env.example` e renomeie a cópia para `.env`.
Abra o `.env` e informe sua chave em `OPENROUTER\_API\_KEY`.
Se necessário, altere `OPENROUTER\_MODEL` para um modelo disponível que aceite tool calling.
Exemplo:
```env
OPENROUTER\_API\_KEY=sua\_chave\_real
OPENROUTER\_MODEL=openrouter/free
```
A disponibilidade e o suporte a chamadas de ferramentas dependem do modelo selecionado e podem mudar no OpenRouter. A chave não deve ser compartilhada nem enviada ao GitHub.
Como executar
Primeiro, prepare os dados:
```bash
python limpeza.py
```
Depois, inicie o dashboard:
```bash
streamlit run app.py
```
O Streamlit exibirá no terminal o endereço local para abrir a aplicação no navegador, normalmente `http://localhost:8501`.
Ferramentas do agente
O agente recebe as perguntas e decide qual função Python utilizar. As funções disponíveis são:
Ferramenta	Finalidade
`consultar\_indicadores`	Receita, pedidos, ticket médio, clientes e cancelamentos, com filtros de data e categoria
`consultar\_receita\_mensal`	Receita de pedidos concluídos por mês
`consultar\_top\_cidades`	Cinco cidades com maior receita
`consultar\_receita\_media\_cliente`	Receita média por cliente único
O fluxo é: pergunta do usuário → modelo seleciona uma ferramenta → Python executa o cálculo → resultado retorna ao modelo → IA apresenta a explicação.
Melhorias implementadas
Além dos indicadores e gráficos principais, foram implementados:
Receita média por cliente.
Ranking das cinco cidades com maior receita.
Consulta de indicadores por intervalo de datas e categoria.
Testes automatizados para as principais regras de limpeza e cálculo.
Testes
Execute os testes na raiz do projeto:
```bash
python -m unittest discover -s tests -v
```
Os testes verificam:
Padronização dos status.
Cálculo da receita por pedido.
Remoção de pedidos duplicados.
Cálculo de receita, pedidos concluídos, clientes únicos e taxa de cancelamento.
Agrupamento mensal da receita.
Ranking de cidades.
Os testes devem ser executados no ambiente local antes da entrega. Registre no repositório o resultado efetivamente obtido ao executar o comando.
Estrutura do projeto
```text
data-pilot/
├── app.py
├── agente\_ia.py
├── limpeza.py
├── metricas.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── data/
│   ├── sales.csv
│   └── sales\_limpo.csv
└── tests/
    └── test\_projeto.py
```
Segurança
O arquivo `.env` contém a chave privada e não deve ser enviado ao GitHub.
O `.gitignore` já impede o versionamento do `.env`.
O arquivo `.env.example` contém somente um exemplo, sem chave real.
Antes de publicar, confira se nenhuma chave ou informação privada foi adicionada ao repositório.
