# core/planejador.py

def calcular_tempo_ate_meta(valor_inicial, aporte_mensal, taxa_anual, meta, tipo_meta="total"):
    """
    Calcula meses necessários para atingir um valor total ou um lucro específico.
    """
    if taxa_anual <= 0 and aporte_mensal <= 0:
        return None # Meta impossível sem rendimento ou aporte

    taxa_mensal = (1 + taxa_anual) ** (1/12) - 1
    valor_atual = valor_inicial
    meses = 0

    # Define a condição de parada dinamicamente (Lucro vs Total)
    if tipo_meta == "lucro":
        def meta_atingida(v): return (v - valor_inicial) >= meta
    else:
        def meta_atingida(v): return v >= meta

    while not meta_atingida(valor_atual):
        valor_atual = valor_atual * (1 + taxa_mensal) + aporte_mensal
        meses += 1
        
        if meses > 1200: # Trava de segurança (100 anos)
            return -1 

    return meses, valor_atual

def calcular_renda_passiva(valor_patrimonio, taxa_anual_real):
    """Calcula retirada mensal sustentável baseada na taxa real (acima da inflação)."""
    taxa_mensal_real = (1 + taxa_anual_real) ** (1/12) - 1
    return valor_patrimonio * taxa_mensal_real

# core/planejador.py (Adicione ao final)

def calcular_aporte_necessario(valor_inicial, meta_valor_final, taxa_anual, meses):
    """
    Calcula quanto o usuário precisa investir mensalmente para atingir uma meta em X meses.
    """
    if meses <= 0:
        return 0.0
    
    taxa_mensal = (1 + taxa_anual) ** (1/12) - 1
    
    # Se não houver taxa, é apenas a divisão simples da diferença
    if taxa_mensal <= 0:
        return max(0, (meta_valor_final - valor_inicial) / meses)
    
    # Cálculo do valor futuro do capital inicial
    valor_futuro_inicial = valor_inicial * (1 + taxa_mensal) ** meses
    
    # Quanto falta para a meta após os juros do capital inicial
    valor_restante = meta_valor_final - valor_futuro_inicial
    
    if valor_restante <= 0:
        return 0.0 # Meta já atingida só com o inicial
        
    # Fórmula da anuidade (PMT) para o aporte mensal
    aporte = valor_restante / (((1 + taxa_mensal) ** meses - 1) / taxa_mensal)
    
    return round(aporte, 2)

