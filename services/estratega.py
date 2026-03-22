# services/estratega.py
from core.planejador import calcular_renda_passiva

def analisar_liberdade_financeira(valor_atual, gasto_mensal, taxa_anual_real):
    """
    Diagnóstico: O quanto o usuário está perto de não precisar mais trabalhar.
    """
    renda_estimada = calcular_renda_passiva(valor_atual, taxa_anual_real)
    
    # Proteção contra divisão por zero (Dica 4 do Review)
    if gasto_mensal <= 0:
        percentual_cobertura = 100.0
    else:
        percentual_cobertura = (renda_estimada / gasto_mensal) * 100

    # Cálculo de Patrimônio Necessário (Regra dos 4% adaptada à taxa real)
    taxa_mensal_real = (1 + taxa_anual_real) ** (1/12) - 1
    patrimonio_alvo = gasto_mensal / taxa_mensal_real if taxa_mensal_real > 0 else 0
    
    falta_patrimonio = max(0, patrimonio_alvo - valor_atual)

    return {
        "renda_mensal": round(renda_estimada, 2),
        "percentual_cobertura": round(min(percentual_cobertura, 100.0), 1),
        "esta_livre": percentual_cobertura >= 100,
        "patrimonio_alvo": round(patrimonio_alvo, 2),
        "falta_para_meta": round(falta_patrimonio, 2)
    }
