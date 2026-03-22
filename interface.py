import streamlit as st
import pandas as pd
from core.simulador import simular_investimento_completo
from services.comparador import comparar_bancos
from services.recomendador import recomendar_investimentos
from core.planejador import calcular_tempo_ate_meta
from services.estratega import analisar_liberdade_financeira
from core.planejador import calcular_tempo_ate_meta, calcular_aporte_necessario
from core.simulador import simular_investimento_completo, simular_monte_carlo, extrair_cenarios_monte_carlo
import numpy as np
from core.impostos import calcular_ir_renda_fixa
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="InvestSmart - Consultor", layout="wide")

st.title("📊 InvestSmart: Seu Consultor de Investimentos")

# No interface.py, logo após o st.title(...)
from data.taxas import TAXAS_MERCADO

# Cria uma linha com as taxas oficiais buscadas na API
st.write("### 🌐 Indicadores do Mercado (Tempo Real)")
col_a, col_b, col_c = st.columns(3)
col_a.metric("SELIC (via API)", f"{TAXAS_MERCADO['SELIC']*100:.2f}%")
col_b.metric("CDI (via API)", f"{TAXAS_MERCADO['CDI']*100:.2f}%")
col_c.metric("IPCA 12m (via API)", f"{TAXAS_MERCADO['IPCA_ESTIMADO']*100:.2f}%")
st.markdown("---")


# --- SIDEBAR (Entradas de Dados) ---
st.sidebar.header("📥 Seus Dados")
v_ini = st.sidebar.number_input("Valor Inicial (R$)", min_value=0.0, value=10000.0, step=1000.0)
v_aporte = st.sidebar.number_input("Aporte Mensal (R$)", min_value=0.0, value=500.0, step=100.0)
tempo = st.sidebar.slider("Tempo (Meses)", 1, 360, 12)
inflacao = st.sidebar.slider("Inflação Anual (%)", 0.0, 20.0, 4.5) / 100

# --- TABS (Abas do Sistema) ---
tab1, tab2, tab3 = st.tabs(["💰 Simulador Manual", "🏆 Ranking de Bancos", "🎯 Planejador"])

with tab1:
    st.subheader("Simulação Personalizada")
    taxa_manual = st.number_input("Taxa Anual Esperada (%)", value=12.0) / 100
    
    if st.button("Calcular Simulação"):
        res = simular_investimento_completo(v_ini, v_aporte, taxa_manual, tempo, inflacao)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Valor Líquido", f"R$ {res.valor_liquido:,.2f}")
        col2.metric("Imposto Pago", f"R$ {res.valor_imposto:,.2f}")
        col3.metric("Poder de Compra Real", f"R$ {res.valor_real_inflacao:,.2f}")

        # --- NOVO: GRÁFICO DE EVOLUÇÃO ---
        st.markdown("---")
        st.subheader("📈 Evolução do Patrimônio no Tempo")
        df_evolucao = pd.DataFrame(res.evolucao, columns=["Patrimônio (R$)"])
        st.line_chart(df_evolucao)

# --- Adicione na Sidebar ou logo acima do botão na Tab 1 ---
volatilidade = st.sidebar.slider("Nível de Risco/Volatilidade (%)", 1.0, 20.0, 3.0, help="Quanto maior, mais as linhas se afastam.") / 100

if st.button("🚀 Simular Cenários Probabilísticos"):
    with st.spinner("Simulando 1.000 universos possíveis..."):
        matriz = simular_monte_carlo(v_ini, v_aporte, taxa_manual, tempo, volatilidade)
        cenarios = extrair_cenarios_monte_carlo(matriz, v_ini, v_aporte, tempo, inflacao)
        
        st.subheader("📊 Análise de Risco (Modelo Lognormal)")
        
        # Métricas com explicação
        c1, c2, c3 = st.columns(3)
        c1.metric("Cenário Ruim (10%)", f"R$ {cenarios['pessimista']:,.2f}", help="Existe 90% de chance de você ganhar MAIS que isso.")
        c2.metric("Cenário Provável", f"R$ {cenarios['provavel']:,.2f}", help="A mediana das simulações.")
        c3.metric("Cenário Ótimo (10%)", f"R$ {cenarios['otimista']:,.2f}", help="Cenário de mercado muito favorável.")
        
        # Gráfico Melhorado
        df_plot = pd.DataFrame({
            "Pessimista": np.percentile(matriz, 10, axis=0),
            "Médio": np.percentile(matriz, 50, axis=0),
            "Otimista": np.percentile(matriz, 90, axis=0)
        })
        
        st.line_chart(df_plot)
        st.caption("O gráfico mostra o valor bruto. As métricas acima já descontam IR e Inflação.")


        st.markdown("---")
        st.subheader("🍕 Composição do Patrimônio (Cenário Provável)")

        # 1. Pegamos o valor BRUTO mediano (sem nenhum desconto ainda)
        v_bruto_provavel = np.percentile(matriz[:, -1], 50)

        # 2. Calculamos o IR e o Líquido exatos para esse valor
        total_investido = v_ini + (v_aporte * tempo)
        v_imposto, v_liquido_nominal = calcular_ir_renda_fixa(v_bruto_provavel, v_ini, v_aporte, tempo)
        lucro_liquido = v_liquido_nominal - total_investido

        # 3. Criamos os dados com as 3 fatias
        df_pizza = pd.DataFrame({
            "Categoria": ["Capital Investido", "Lucro Líquido", "Imposto de Renda (IR)"],
            "Valores": [total_investido, max(0, lucro_liquido), v_imposto]
        })

        # 4. Gráfico com 3 cores (Azul, Verde e Vermelho/Laranja para o imposto)
        fig = px.pie(df_pizza, values='Valores', names='Categoria', 
                    color_discrete_sequence=['#29b5e8', '#1af2aa', '#ff4b4b'],
                    hole=0.4)

        st.plotly_chart(fig)




with tab2:
    st.subheader("Onde seu dinheiro rende mais?")
    
    col_p, col_z = st.columns(2)
    perfil = col_p.selectbox("Qual seu perfil?", ["conservador", "arrojado"])
    prazo = col_z.selectbox("Qual seu prazo?", ["curto", "longo"])
    
    if st.button("Gerar Ranking Inteligente"):
        # 1. Busca os dados
        lista_bruta = comparar_bancos(v_ini, v_aporte, tempo, inflacao)
        ranking = recomendar_investimentos({"perfil": perfil, "prazo": prazo}, lista_bruta)
        
        # 2. Cria uma tabela para o Streamlit mostrar
        dados_tabela = []
        for r in ranking:
            dados_tabela.append({
                "Score": r['score'],
                "Banco": r['banco'],
                "Produto": r['produto'],
                "Líquido (R$)": r['resultado'].valor_liquido,
                "Justificativa": " | ".join(r['justificativa'])
            })
        
        df = pd.DataFrame(dados_tabela)
        st.table(df) # Mostra a tabela organizada

        # 3. Gráfico Comparativo
        st.bar_chart(df.set_index("Banco")["Líquido (R$)"])

with tab3:
    st.subheader("🎯 Planejamento de Metas e Liberdade")
    
    # --- PARTE NOVA: ESCOLHA DO MODO ---
    modo_plan = st.radio(
        "O que você deseja calcular?",
        ["Tempo para atingir uma Meta", "Quanto preciso poupar por mês"],
        horizontal=True
    )

    col_m1, col_m2 = st.columns(2)
    
    if modo_plan == "Tempo para atingir uma Meta":
        # Aqui entra a sua ideia de Meta de Lucro vs Total
        tipo_m = col_m1.selectbox("Tipo de Meta", ["Valor Total", "Lucro Acumulado"])
        meta_v = col_m2.number_input("Valor da Meta (R$)", value=100000.0, step=10000.0)
        t_real = st.slider("Taxa Real Esperada (% a.a.)", 1.0, 15.0, 5.0, key="taxa_tempo") / 100

        
        if st.button("🎯 Calcular Tempo"):
            m_interna = "lucro" if tipo_m == "Lucro Acumulado" else "total"
            # Usando o seu v_ini e v_aporte da sidebar
            res_tempo = calcular_tempo_ate_meta(v_ini, v_aporte, t_real, meta_v, m_interna)
            
            if res_tempo and res_tempo[0] != -1:
                meses_t = res_tempo[0]
                st.success(f"⏱️ Você atingirá sua meta em **{meses_t // 12} anos e {meses_t % 12} meses**.")
                st.info(f"💰 Patrimônio final estimado: R$ {res_tempo[1]:,.2f}")
            else:
                st.error("❌ Meta inalcançável com esses aportes.")

    else: # Modo: Quanto preciso poupar
        meta_v = col_m1.number_input("Valor Final Desejado (R$)", value=500000.0)
        meses_p = col_m2.number_input("Prazo em Meses", value=120, step=12)
        t_real = st.slider("Taxa Real Esperada (% a.a.)", 1.0, 15.0, 5.0, key="taxa_aporte") / 100
        
        if st.button("💸 Calcular Aporte Necessário"):
            precisa = calcular_aporte_necessario(v_ini, meta_v, t_real, meses_p)
            if precisa <= 0:
                st.balloons()
                st.success("✅ Você já atingirá essa meta apenas com seu capital inicial!")
            else:
                st.warning(f"💸 Você precisará investir **R$ {precisa:,.2f}** todos os meses.")

    # --- PARTE QUE VOCÊ JÁ TINHA (DIAGNÓSTICO) ---
    st.markdown("---")
    st.subheader("🏦 Diagnóstico de Independência Financeira")
    gasto_m = st.number_input("Seu Gasto Mensal Alvo (R$)", value=3000.0, step=500.0)
    
    # Faz a análise usando a taxa real escolhida no slider (ou 5% fixo como base)
    analise = analisar_liberdade_financeira(v_ini, gasto_m, 0.05)
    
    st.write(f"Sua renda passiva hoje cobriria **{analise['percentual_cobertura']}%** do seu gasto alvo.")
    st.progress(analise['percentual_cobertura'] / 100)
    
    if analise['esta_livre']:
        st.balloons()
        st.write("🎉 **Parabéns! Seu patrimônio já sustenta seu padrão de vida!**")
    else:
        st.write(f"Ainda faltam **R$ {analise['falta_para_meta']:,.2f}** para atingir o patrimônio necessário para essa renda.")

