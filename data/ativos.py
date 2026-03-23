from data.taxas import obter_taxa

def obter_investimentos():
    cdi = obter_taxa("CDI")
    selic = obter_taxa("SELIC")
    ipca = obter_taxa("IPCA_ESTIMADO") 

    return [
        {
            "banco": "Nubank",
            "produto": "CDB 100% CDI",
            "taxa_anual": cdi * 1.0,
            "isento": False, "risco": "baixo", "liquidez": "alta", "tipo": "pos"
        },
        {
            "banco": "Inter",
            "produto": "LCI 90% CDI",
            "taxa_anual": cdi * 0.9,
            "isento": True, "risco": "baixo", "liquidez": "media", "tipo": "pos"
        },
        {
            "banco": "Tesouro",
            "produto": "Selic + 0.1%",
            "taxa_anual": selic + 0.001,
            "isento": False, "risco": "minimo", "liquidez": "alta", "tipo": "pos"
        },
        {
            "banco": "XP",
            "produto": "CDB Pré 14%",
            "taxa_anual": 0.14,
            "isento": False, "risco": "medio", "liquidez": "baixa", "tipo": "pre"
        },
        {
            "banco": "Tesouro",
            "produto": "IPCA + 6%",
            "taxa_anual": ipca + 0.06, # Taxa real + inflação de 2026
            "isento": False, "risco": "minimo", "liquidez": "baixa", "tipo": "pos"
        },
        {
            "banco": "Itaú",
            "produto": "LCA 88% CDI",
            "taxa_anual": cdi * 0.88,
            "isento": True, "risco": "minimo", "liquidez": "media", "tipo": "pos"
        },
    ]

INVESTIMENTOS_MERCADO = obter_investimentos()