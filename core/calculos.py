def converter_taxa_anual_para_mensal(taxa_anual):
    """Converte uma taxa anual (ex: 0.12) para mensal usando juros compostos."""
    return (1 + taxa_anual) ** (1/12) - 1


def calcular_juros_compostos_com_aportes(valor_inicial, aporte_mensal, taxa_anual, meses):
    """
    Calcula o montante bruto final com aportes mensais.
    Fórmula: M = P(1+i)^n + A * (((1+i)^n - 1) / i)
    """

    if meses < 0:
        raise ValueError("Meses não pode ser negativo")

    if taxa_anual < -1:
        raise ValueError("Taxa anual inválida")

    taxa_mensal = converter_taxa_anual_para_mensal(taxa_anual)

    # Parte 1: Juros sobre o valor inicial
    montante_inicial = valor_inicial * (1 + taxa_mensal) ** meses

    # Parte 2: Juros sobre os aportes mensais
    if taxa_mensal != 0:
        montante_aportes = aporte_mensal * (((1 + taxa_mensal) ** meses - 1) / taxa_mensal)
    else:
        montante_aportes = aporte_mensal * meses

    return montante_inicial + montante_aportes