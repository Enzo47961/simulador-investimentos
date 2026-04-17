📊 InvestSmart: Consultor e Planejador Financeiro
InvestSmart é um ecossistema de simulação e estratégia de investimentos desenvolvido em Python. Diferente de calculadoras comuns, o sistema utiliza uma Scoring Engine (mecanismo de pontuação) para recomendar ativos baseados no perfil de risco, liquidez e rentabilidade real do usuário.

---

🚀 Funcionalidades Principais1. 🧠 Motor Matemático (Core)

- Juros Compostos: Cálculos precisos com aportes mensais recorrentes.
- Tributação Automática: Aplicação da tabela regressiva de IR (Renda Fixa) brasileira.
- Ajuste de Inflação: Cálculo de Poder de Compra Real usando desconto financeiro.

2. 🏆 Ranking Inteligente (Services)

- Comparador de Ativos: Analisa simultaneamente CDBs, LCIs, LCAs e Tesouro Direto.
- Scoring Engine: Algoritmo que atribui notas aos investimentos com base em:
- Rentabilidade Líquida Normalizada.
  - Compatibilidade com Perfil (Conservador vs. Arrojado).
  - Necessidade de Liquidez (Curto vs. Longo Prazo).
  - Vantagens Fiscais (Isenção de IR).

3. 🎯 Planejador Estratégico

- Tempo até a Meta: Cálculo de meses necessários para atingir Patrimônio Total ou Lucro Acumulado.
- Aporte Necessário: Define quanto o usuário precisa poupar para atingir um objetivo em tempo determinado.
- Diagnóstico de Liberdade: Barra de progresso em tempo real indicando quanto da despesa mensal é coberta pela renda passiva.

---

🛠️ Tecnologias Utilizadas

- Python 3.13+: Linguagem base.
- Streamlit: Interface web e dashboards interativos.
- Pandas: Manipulação de dados e tabelas.
- Dataclasses: Contratos de dados imutáveis para garantir integridade financeira.

---

📂 Estrutura do Projeto

projeto-investimentos/
├── app/ # Futura integração de backend
├── core/ # 🔥 Núcleo matemático e fórmulas puras
│ ├── calculos.py # Juros e montantes
│ ├── impostos.py # Regras da Receita Federal
│ ├── inflacao.py # Desconto de poder de compra
│ ├── planejador.py # Lógica de metas e tempo
│ └── models.py # Contrato de dados (Dataclasses)
├── services/ # 🧠 Inteligência de Negócio
│ ├── comparador.py # Orquestração de múltiplos bancos
│ ├── recomendador.py # Scoring engine e lógica de perfil
│ └── estratega.py # Diagnóstico de liberdade financeira
├── data/ # Camada de Dados
│ ├── ativos.py # Catálogo de produtos financeiros
│ └── taxas.py # Central de taxas (Selic, CDI, IPCA)
├── interface.py # Dashboard Web em Streamlit
└── main.py # Ponto de entrada via Terminal

---

🚦 Como Rodar o Projeto

1.  Instale as dependências:

pip install streamlit pandas

2.  Execute a interface web:

streamlit run interface.py

3.  (Opcional) Execute via terminal:

python main.py

---

📈 Roadmap / Próximos Passos (2026)

- Integração com API: Conexão direta com o Banco Central (SGS) para Selic e IPCA em tempo real.
- Gráficos de Pizza: Visualização da divisão entre Capital Investido e Lucro Gerado.
- Diversificação: Algoritmo para sugerir divisão de carteira entre os ativos.

---

💡 Próximo Passo Sugerido:
Agora que sua documentação está pronta, você quer que eu te mostre o código da API gratuita para buscar a Selic automaticamente? Assim, você só precisará copiar ele quando decidir automatizar o projeto no futuro!

streamlit run interface.py

git add . (prepara todos os arquivos alterados).
git commit -m "sua mensagem aqui" (salva uma "foto" das alterações localmente).
git push (envia tudo para o site do GitHub).

Como funciona na prática (Passo a passo):
Ache o "DNA" do commit:
No terminal, digite git log --oneline. Você verá algo assim:
a1b2c3d (Commit 3 - O mais recente)
e4f5g6h (Commit 2 - O que você quer)
i7j8k9l (Commit 1)
Crie a nova linha do tempo:
Digite o comando:
git checkout -b versao-recuperada e4f5g6h
(Troque versao-recuperada pelo nome que quiser e e4f5g6h pelo código do seu commit).
