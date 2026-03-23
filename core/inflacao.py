def converter_inflacao_anual_para_mensal(inflacao_anual):
    """
    Converte a inflação anual (ex: 0.06) para mensal.
    """
    if inflacao_anual < -1:
        raise ValueError("Inflação anual não pode ser menor que -100%")

    return (1 + inflacao_anual) ** (1/12) - 1


def ajustar_por_inflacao(valor_nominal, inflacao_anual, meses):
    """
    Calcula o valor real (poder de compra) de um valor futuro.
    """

    if meses < 0:
        raise ValueError("Meses não pode ser negativo")

    if valor_nominal < 0:
        raise ValueError("Valor nominal não pode ser negativo")

    inflacao_mensal = converter_inflacao_anual_para_mensal(inflacao_anual)

    # Evita problemas com ponto flutuante
    if abs(inflacao_mensal) < 1e-9:
        return valor_nominal

    # Fator acumulado de inflação
    fator_inflacao = (1 + inflacao_mensal) ** meses

    valor_real = valor_nominal / fator_inflacao

    return valor_real

# ... (suas funções anteriores: converter_inflacao_anual_para_mensal e ajustar_por_inflacao)

def calcular_taxa_real_fisher(taxa_nominal, inflacao_anual):
    """
    Calcula a rentabilidade real líquida (acima da inflação) usando a fórmula de Fisher.
    Esta é a fórmula padrão usada por economistas e bancos centrais.
    """
    # Evita divisão por zero caso a inflação fosse -100% (improvável mas seguro)
    if inflacao_anual <= -1:
        return taxa_nominal 
        
    return ((1 + taxa_nominal) / (1 + inflacao_anual)) - 1
