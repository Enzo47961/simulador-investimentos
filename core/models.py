from dataclasses import dataclass

@dataclass(frozen=True)
class ResultadoSimulacao:
    valor_bruto: float
    valor_total_investido: float
    lucro_bruto: float
    valor_imposto: float
    valor_liquido: float
    valor_real_inflacao: float
    aliquota_aplicada: float
    evolucao: list 