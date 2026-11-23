🚀 Data Pilot

Plataforma inteligente de análise exploratória, limpeza de dados e geração automática de insights com Inteligência Artificial.

O Data Pilot é uma solução modular desenvolvida para automatizar o ciclo de vida inicial de dados comerciais (Sales Data). O sistema integra pipelines de higienização de dados, cálculo de indicadores-chave de desempenho (KPIs) e um agente de Inteligência Artificial capaz de interpretar métricas e responder perguntas de negócio em linguagem natural por meio de uma interface interativa.

📋 Índice

Arquitetura e Funcionalidades

Estrutura do Projeto

Pré-requisitos

Instalação e Configuração

Como Executar

Testes Automatizados

Boas Práticas e Segurança

✨ Arquitetura e Funcionalidades

O projeto foi estruturado sob o princípio de separação de responsabilidades (Separation of Concerns), dividindo-se em quatro camadas principais:

Higienização e Tratamento de Dados (limpeza.py)

Ingestão de dados brutos (data/sales.csv).

Padronização de colunas, tratamento de valores ausentes, remoção de duplicatas e tipagem correta de variáveis.

Exportação da base tratada e pronta para consumo analítico (data/sales_limpo.csv).

Motor de Métricas e KPIs (metricas.py)

Consolidação de indicadores financeiros e operacionais (receita total, ticket médio, volume de vendas, desempenho por categoria/região, entre outros).

Fornecimento de agregações estruturadas tanto para visualização quanto para o contexto do agente de IA.

Agente Analítico de IA (agente_ia.py)

Integração com modelos de linguagem (LLMs) para análise contextualizada dos dados.

Tradução de perguntas de negócio em diagnósticos claros, identificando tendências, anomalias e oportunidades.

Interface Interativa (app.py)

Aplicação web centralizada que conecta o pipeline de dados, os painéis de métricas e o chat analítico com o agente de IA em uma experiência fluida para o usuário final.

📂 Estrutura do Projeto

data-pilot/
├── data/
│   ├── sales.csv            # Base de dados bruta (entrada)
│   └── sales_limpo.csv      # Base de dados higienizada (saída)
├── tests/
│   └── test_projeto.py      # Suíte de testes automatizados
├── .env.example             # Modelo de variáveis de ambiente
├── .gitignore               # Regras de arquivos ignorados pelo Git
├── agente_ia.py             # Lógica do agente inteligente e prompts
├── app.py                   # Ponto de entrada da interface da aplicação
├── limpeza.py               # Pipeline de ETL e tratamento de dados
├── metricas.py              # Regras de negócio e cálculo de indicadores
└── requirements.txt         # Dependências do projeto


🔧 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em seu ambiente:

Python 3.10 ou superior

pip (gerenciador de pacotes Python)

Chave de API válida do provedor de LLM configurado no projeto

⚙️ Instalação e Configuração

Clone o repositório e acesse o diretório do projeto:

git clone <url-do-repositorio>
cd data-pilot


Crie e ative um ambiente virtual (recomendado):

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate


Instale as dependências:

pip install -r requirements.txt


Configure as variáveis de ambiente:
Copie o arquivo de exemplo e preencha com suas credenciais:

cp .env.example .env


Edite o arquivo .env e insira sua chave de API e demais parâmetros necessários.

▶️ Como Executar

Execute o pipeline de limpeza de dados (caso precise reprocessar a base bruta):

python limpeza.py


Inicie a aplicação principal:

streamlit run app.py


(Caso utilize outro framework web em app.py, execute python app.py.)

🧪 Testes Automatizados

O projeto conta com testes unitários e de integração localizados em tests/test_projeto.py para garantir a confiabilidade do tratamento de dados e do cálculo de métricas.

Para executar a suíte de testes:

pytest


🔒 Boas Práticas e Segurança

Credenciais: Nunca versione o arquivo .env com chaves reais. Utilize sempre o .env.example como referência de estrutura.

Imutabilidade dos Dados Brutos: O arquivo data/sales.csv é mantido intacto; todas as transformações são persistidas em data/sales_limpo.csv.
