from core.calculos import calcular_juros_compostos_com_aportes
from core.impostos import calcular_ir_renda_fixa, obter_aliquota_ir
from core.inflacao import ajustar_por_inflacao
from core.models import ResultadoSimulacao
import numpy as np

def simular_investimento_completo(valor_inicial, aporte_mensal, taxa_anual, meses, inflacao_anual, considerar_imposto=True):
    # 1. Calcula o Bruto
    valor_bruto = calcular_juros_compostos_com_aportes(valor_inicial, aporte_mensal, taxa_anual, meses)
    
    # 2. Lógica Inteligente de Imposto
    if considerar_imposto:
        valor_imposto, valor_liquido = calcular_ir_renda_fixa(valor_bruto, valor_inicial, aporte_mensal, meses)
        aliquota = obter_aliquota_ir(meses)
    else:
        valor_imposto = 0.0
        valor_liquido = valor_bruto
        aliquota = 0.0

    # 3. Calcula o Real sobre o Líquido CORRETO
    valor_real = ajustar_por_inflacao(valor_liquido, inflacao_anual, meses)

    # --- NOVO: GERAÇÃO DA EVOLUÇÃO PARA O GRÁFICO ---
    evolucao = []
    v_temp = valor_inicial
    taxa_mensal = (1 + taxa_anual) ** (1/12) - 1
    for _ in range(meses + 1):
        evolucao.append(round(v_temp, 2))
        v_temp = v_temp * (1 + taxa_mensal) + aporte_mensal

    # 4. Retorna o Dataclass (Contrato)
    return ResultadoSimulacao(
        valor_bruto=round(valor_bruto, 2),
        valor_total_investido=round(valor_inicial + (aporte_mensal * meses), 2),
        lucro_bruto=round(valor_bruto - (valor_inicial + (aporte_mensal * meses)), 2),
        valor_imposto=round(valor_imposto, 2),
        valor_liquido=round(valor_liquido, 2),
        valor_real_inflacao=round(valor_real, 2),
        aliquota_aplicada=aliquota,
        evolucao=evolucao # <--- ADICIONADO AQUI
    )

def simular_monte_carlo(v_ini, v_aporte, taxa_anual, tempo_meses, volatilidade_anual=0.03, n_simulacoes=1000):
    """
    Versão Profissional: Usa retornos logarítmicos e vetorização NumPy.
    """
    # Converter taxa e vol anual para mensal (logarítmica)
    mu_mensal = np.log(1 + taxa_anual) / 12
    sigma_mensal = volatilidade_anual / np.sqrt(12)

    # Gera todos os sorteios de uma vez (Matriz: n_simulacoes x tempo_meses)
    retornos = np.random.normal(mu_mensal, sigma_mensal, (n_simulacoes, tempo_meses))
    
    # Matriz para armazenar a evolução
    caminhos = np.zeros((n_simulacoes, tempo_meses + 1))
    caminhos[:, 0] = v_ini

    # Simulando mês a mês (necessário por causa do aporte fixo)
    for t in range(1, tempo_meses + 1):
        # Valor anterior corrigido pelo retorno sorteado + aporte
        caminhos[:, t] = caminhos[:, t-1] * np.exp(retornos[:, t-1]) + v_aporte
    
    return caminhos

def extrair_cenarios_monte_carlo(matriz_simulacoes, v_ini, v_aporte, meses, inflacao_anual):
    """
    Extrai percentis aplicando IR e Inflação de 2026.
    """
    valores_finais_brutos = matriz_simulacoes[:, -1]
    
    def limpar_valor(valor_bruto):
        # Reutiliza sua lógica core para garantir precisão
        _, v_liquido = calcular_ir_renda_fixa(valor_bruto, v_ini, v_aporte, meses)
        return ajustar_por_inflacao(v_liquido, inflacao_anual, meses)

    # Aplicando a limpeza em cada percentil sorteado
    return {
        "pessimista": limpar_valor(np.percentile(valores_finais_brutos, 10)),
        "provavel": limpar_valor(np.percentile(valores_finais_brutos, 50)),
        "otimista": limpar_valor(np.percentile(valores_finais_brutos, 90))
    }
