# services/comparador.py
from core.simulador import simular_investimento_completo
from data.ativos import INVESTIMENTOS_MERCADO

def comparar_bancos(v_ini, aporte, meses, inflacao):
    ranking = []
    for ativo in INVESTIMENTOS_MERCADO:
        res = simular_investimento_completo(
            v_ini, aporte, ativo['taxa_anual'], meses, inflacao, 
            considerar_imposto=not ativo['isento']
        )
        
        # Criamos uma cópia do ativo e adicionamos o resultado da simulação
        # Isso garante que risco, liquidez e tipo "viajem" junto com o resultado
        item = ativo.copy()
        item['resultado'] = res
        ranking.append(item)
    
    return sorted(ranking, key=lambda x: x['resultado'].valor_liquido, reverse=True)

