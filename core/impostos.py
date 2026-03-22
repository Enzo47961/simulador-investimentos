def obter_aliquota_ir(meses):
    """
    Retorna a alíquota do IR de Renda Fixa com base no prazo em meses.
    """
    if meses <= 6:
        return 0.225
    elif meses <= 12:
        return 0.20
    elif meses <= 24:
        return 0.175
    else:
        return 0.15


def calcular_ir_renda_fixa(valor_final, valor_inicial, aporte_mensal, meses):
    """
    Calcula o Imposto de Renda sobre o lucro.

    Retorna:
    (valor_imposto, valor_liquido)
    """

    if meses < 0:
        raise ValueError("Meses não pode ser negativo")

    if valor_inicial < 0 or aporte_mensal < 0:
        raise ValueError("Valores não podem ser negativos")

    if valor_final < 0:
        raise ValueError("Valor final não pode ser negativo")

    total_investido = valor_inicial + (aporte_mensal * meses)
    lucro_bruto = valor_final - total_investido

    # Imposto só incide se houver lucro
    if lucro_bruto <= 0:
        return 0.0, valor_final

    aliquota = obter_aliquota_ir(meses)
    valor_imposto = lucro_bruto * aliquota
    valor_liquido = valor_final - valor_imposto

    return valor_imposto, valor_liquido