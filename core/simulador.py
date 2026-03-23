from core.calculos import calcular_juros_compostos_com_aportes
from core.impostos import calcular_ir_renda_fixa, obter_aliquota_ir
from core.inflacao import ajustar_por_inflacao
from core.models import ResultadoSimulacao
import numpy as np

def simular_investimento_completo(valor_inicial, aporte_mensal, taxa_anual, meses, inflacao_anual, 
                                 considerar_imposto=True, crescimento_aporte_anual=0.0, 
                                 mes_choque=None, intensidade_choque=0.0):
    
    # 1. Preparação
    taxa_mensal = (1 + taxa_anual) ** (1/12) - 1
    evolucao = []
    v_temp = valor_inicial
    aporte_atual = aporte_mensal
    total_investido = valor_inicial
    
    # 2. Motor de Simulação Mês a Mês (Agora é o Coração do Cálculo)
    for t in range(meses + 1):
        # A. Aplica Choque Temporal (Crise) se o mês coincidir
        if mes_choque is not None and t == mes_choque:
            v_temp = v_temp * (1 - intensidade_choque)
            
        evolucao.append(round(v_temp, 2))
        
        # B. Incrementa o aporte a cada 12 meses (Aniversário do investimento)
        if t > 0 and t % 12 == 0:
            aporte_atual *= (1 + crescimento_aporte_anual)
            
        # C. Rentabiliza o saldo e soma o aporte do mês
        if t < meses: # No último mês apenas registramos o valor final
            v_temp = v_temp * (1 + taxa_mensal) + aporte_atual
            total_investido += aporte_atual

    valor_bruto = evolucao[-1]

    # 3. Lógica de Imposto (Usando as suas funções core)
    if considerar_imposto:
        # Passamos o 'total_investido' real, que agora pode ser maior por causa dos aumentos
        valor_imposto, valor_liquido = calcular_ir_renda_fixa(valor_bruto, valor_inicial, aporte_mensal, meses) 
        aliquota = obter_aliquota_ir(meses)
    else:
        valor_imposto = 0.0
        valor_liquido = valor_bruto
        aliquota = 0.0

    # 4. Ajuste de Inflação (Sua função core)
    valor_real = ajustar_por_inflacao(valor_liquido, inflacao_anual, meses)

    # 5. Retorno (Seu Dataclass)
    return ResultadoSimulacao(
        valor_bruto=round(valor_bruto, 2),
        valor_total_investido=round(total_investido, 2),
        lucro_bruto=round(valor_bruto - total_investido, 2),
        valor_imposto=round(valor_imposto, 2),
        valor_liquido=round(valor_liquido, 2),
        valor_real_inflacao=round(valor_real, 2),
        aliquota_aplicada=aliquota,
        evolucao=evolucao
    )


def simular_monte_carlo(v_ini, v_aporte, taxa_anual, tempo_meses, volatilidade_anual=0.03, n_simulacoes=1000):
    """
    Versão Profissional: Usa retornos logarítmicos e vetorização NumPy.
    """
    # Converter taxa e vol anual para mensal (logarítmica)
    mu_mensal = np.log(1 + taxa_anual) / 12
        # De:
    # sigma_mensal = volatilidade_anual / np.sqrt(12)
    # Para (Nível Profissional):
    sigma_mensal = np.sqrt(np.log(1 + volatilidade_anual**2)) / np.sqrt(12)


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

def calcular_max_drawdown(matriz_simulacoes):
    """Calcula a maior queda (do pico ao vale) registrada nas simulações."""
    # Calcula o pico acumulado para cada simulação
    picos = np.maximum.accumulate(matriz_simulacoes, axis=1)
    # Calcula a queda em relação ao pico
    quedas = (matriz_simulacoes - picos) / picos
    # Retorna a média das maiores quedas de cada universo
    return np.mean(np.min(quedas, axis=1))

def calcular_probabilidade_perda(valores_finais_liquidos, total_investido):
    """Calcula a % de simulações que terminaram abaixo do valor investido."""
    perdas = np.sum(valores_finais_liquidos < total_investido)
    return (perdas / len(valores_finais_liquidos)) * 100

def calcular_sharpe_ratio(matriz_simulacoes, taxa_livre_risco_anual=0.1075):
    """
    Calcula o Índice Sharpe: (Retorno Médio - Taxa Livre de Risco) / Volatilidade.
    Usa a Selic atual como Taxa Livre de Risco padrão.
    """
    # 1. Calcula os retornos finais de cada simulação
    valores_finais = matriz_simulacoes[:, -1]
    valor_inicial = matriz_simulacoes[0, 0]
    
    # 2. Transforma em retorno percentual total
    retornos_percentuais = (valores_finais / valor_inicial) - 1
    
    retorno_medio = np.mean(retornos_percentuais)
    volatilidade_retornos = np.std(retornos_percentuais)
    
    # Evita divisão por zero se a volatilidade for nula (investimento fixo)
    if volatilidade_retornos == 0:
        return 0.0
        
    # 3. Ajusta a taxa livre de risco para o período (simplificado)
    sharpe = (retorno_medio - (taxa_livre_risco_anual * 0.85)) / volatilidade_retornos
    return round(sharpe, 2)

