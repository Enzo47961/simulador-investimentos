📊 InvestSmart: Consultor e Planejador Financeiro
InvestSmart é um ecossistema de simulação e estratégia de investimentos desenvolvido em Python. Diferente de calculadoras comuns, o sistema utiliza uma Scoring Engine (mecanismo de pontuação) para recomendar ativos baseados no perfil de risco, liquidez e rentabilidade real do usuário.
------------------------------

🌐 Link do Site
https://simulador-investimentos-ferraraa.streamlit.app/

🚀 Funcionalidades Principais1. 🧠 Motor Matemático (Core)

* Juros Compostos: Cálculos precisos com aportes mensais recorrentes.
* Tributação Automática: Aplicação da tabela regressiva de IR (Renda Fixa) brasileira.
* Ajuste de Inflação: Cálculo de Poder de Compra Real usando desconto financeiro.

2. 🏆 Ranking Inteligente (Services)

* Comparador de Ativos: Analisa simultaneamente CDBs, LCIs, LCAs e Tesouro Direto.
* Scoring Engine: Algoritmo que atribui notas aos investimentos com base em:
* Rentabilidade Líquida Normalizada.
   * Compatibilidade com Perfil (Conservador vs. Arrojado).
   * Necessidade de Liquidez (Curto vs. Longo Prazo).
   * Vantagens Fiscais (Isenção de IR).

3. 🎯 Planejador Estratégico

* Tempo até a Meta: Cálculo de meses necessários para atingir Patrimônio Total ou Lucro Acumulado.
* Aporte Necessário: Define quanto o usuário precisa poupar para atingir um objetivo em tempo determinado.
* Diagnóstico de Liberdade: Barra de progresso em tempo real indicando quanto da despesa mensal é coberta pela renda passiva.

------------------------------
🛠️ Tecnologias Utilizadas

* Python 3.13+: Linguagem base.
* Streamlit: Interface web e dashboards interativos.
* Pandas: Manipulação de dados e tabelas.
* Dataclasses: Contratos de dados imutáveis para garantir integridade financeira.

------------------------------
📂 Estrutura do Projeto

projeto-investimentos/
├── app/                  # Futura integração de backend
├── core/                 # 🔥 Núcleo matemático e fórmulas puras
│   ├── calculos.py       # Juros e montantes
│   ├── impostos.py       # Regras da Receita Federal
│   ├── inflacao.py       # Desconto de poder de compra
│   ├── planejador.py     # Lógica de metas e tempo
│   └── models.py         # Contrato de dados (Dataclasses)
├── services/             # 🧠 Inteligência de Negócio
│   ├── comparador.py     # Orquestração de múltiplos bancos
│   ├── recomendador.py   # Scoring engine e lógica de perfil
│   └── estratega.py      # Diagnóstico de liberdade financeira
├── data/                 # Camada de Dados
│   ├── ativos.py         # Catálogo de produtos financeiros
│   └── taxas.py          # Central de taxas (Selic, CDI, IPCA)
├── interface.py          # Dashboard Web em Streamlit
└── main.py               # Ponto de entrada via Terminal

------------------------------
🚦 Como Rodar o Projeto

   1. Instale as dependências:
   
   pip install streamlit pandas
   
   2. Execute a interface web:
   
   streamlit run interface.py
   
   3. (Opcional) Execute via terminal:
   
   python main.py
