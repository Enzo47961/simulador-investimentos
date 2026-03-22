from infra.api_bcb import buscar_selic_atual, buscar_cdi_atual , buscar_ipca_atual

TAXAS_MERCADO = {
    "SELIC": 0.1075,
    "CDI": 0.1065,
    "IPCA_ESTIMADO": 0.041
}

def atualizar_taxas():
    """Atualiza as taxas com dados reais da API."""
    selic = buscar_selic_atual()
    cdi = buscar_cdi_atual()
    ipca = buscar_ipca_atual()

    if selic:
        TAXAS_MERCADO["SELIC"] = selic
    if cdi:
        TAXAS_MERCADO["CDI"] = cdi
    if ipca:
        TAXAS_MERCADO["IPCA_ESTIMADO"] = ipca

def obter_taxa(chave):
    return TAXAS_MERCADO.get(chave, 0.0)