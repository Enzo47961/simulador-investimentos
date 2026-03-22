from data.taxas import obter_taxa

def obter_investimentos():
    cdi = obter_taxa("CDI")
    selic = obter_taxa("SELIC")

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
        }
    ]

INVESTIMENTOS_MERCADO = obter_investimentos()