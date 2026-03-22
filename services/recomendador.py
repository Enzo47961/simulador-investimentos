# services/recomendador.py

def recomendar_investimentos(perfil_usuario, lista_comparada):
    """
    Scoring Engine Normalizada: Equilibra Rentabilidade % com Perfil.
    Escala de Pesos: Tudo oscila entre -15 e +15 para manter o equilíbrio.
    """
    recomendados = []
    
    for item in lista_comparada:
        # Criamos uma cópia para não sujar os dados originais (Boa prática!)
        novo_item = item.copy()
        res = novo_item['resultado']
        score = 0.0
        justificativa = []

        # --- 1. PERFORMANCE FINANCEIRA (Normalizada em %) ---
        # Regra: Rentabilidade líquida de 10% no período = 10 pontos
        rentabilidade_periodo = (res.valor_liquido / res.valor_total_investido - 1) * 100
        score += rentabilidade_periodo
        justificativa.append(f"Rentabilidade Líquida: +{rentabilidade_periodo:.1f} pts")

        # --- 2. PERFIL DE RISCO (Balanceado: max +10) ---
        if perfil_usuario['perfil'] == "conservador":
            if novo_item['risco'] in ["minimo", "baixo"]:
                score += 10
                justificativa.append("Segurança para seu perfil (+10)")
        else: # Arrojado
            if novo_item['risco'] == "medio":
                score += 7
                justificativa.append("Apetite a risco (+7)")
            if novo_item['tipo'] == "pre":
                score += 5
                justificativa.append("Taxa Fixa Atrativa (+5)")


        # --- 3. PRAZO E LIQUIDEZ (Ajuste de Pesos) ---
        if perfil_usuario['prazo'] == "curto":
            if novo_item['liquidez'] == "alta": 
                score += 8  # Antes era 12, agora 8 (mais equilibrado)
                justificativa.append("Liquidez Imediata (+8)")
            elif novo_item['liquidez'] == "media":
                score += 3  # Adicionado para o Inter não ficar no zero
                justificativa.append("Liquidez Razoável (+3)")
            elif novo_item['liquidez'] == "baixa":
                score -= 15 # Penalidade firme, mas proporcional
                justificativa.append("AVISO: Baixa Liquidez (-15)")

        # --- 4. EFICIÊNCIA FISCAL ---
        if novo_item['isento']:
            score += 5
            justificativa.append("Vantagem Isenção (+5)")

        novo_item['score'] = round(score, 1)
        novo_item['justificativa'] = justificativa
        recomendados.append(novo_item)

    # Ordena pelo Score Final (Equilíbrio entre Bolso e Perfil)
    return sorted(recomendados, key=lambda x: x['score'], reverse=True)
