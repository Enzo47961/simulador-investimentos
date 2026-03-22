from core.calculos import calcular_juros_compostos_com_aportes
from core.impostos import calcular_ir_renda_fixa, obter_aliquota_ir
from core.inflacao import ajustar_por_inflacao
from core.models import ResultadoSimulacao

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
