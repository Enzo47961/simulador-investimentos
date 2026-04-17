# main.py
from core.simulador import simular_investimento_completo
from services.comparador import comparar_bancos
from services.recomendador import recomendar_investimentos # <-- ADICIONADO
import streamlit as st

def limpar_entrada(texto):
    if not texto: return 0.0
    limpo = texto.replace('R$', '').replace('%', '').strip()
    if '.' in limpo and ',' in limpo:
        limpo = limpo.replace('.', '').replace(',', '.')
    elif ',' in limpo:
        limpo = limpo.replace(',', '.')
    try:
        return float(limpo)
    except ValueError:
        raise ValueError(f"'{texto}' não é um número válido.")

def normalizar_taxa(valor):
    return valor / 100 if valor >= 1 else valor

def exibir_relatorio(resultado, titulo="RELATÓRIO DE INVESTIMENTO"):
    print("\n" + "="*45)
    print(f"      📊 {titulo}      ")
    print("="*45)
    print(f"💰 Total Investido:    R$ {resultado.valor_total_investido:,.2f}")
    print(f"📈 Valor Bruto:        R$ {resultado.valor_bruto:,.2f}")
    print(f"💸 Imposto de Renda:   R$ {resultado.valor_imposto:,.2f} ({resultado.aliquota_aplicada * 100:.1f}%)")
    print(f"✅ Valor Líquido:      R$ {resultado.valor_liquido:,.2f}")
    print(f"📉 Valor Real (IPCA):  R$ {resultado.valor_real_inflacao:,.2f}")
    print("-" * 45)
    rentabilidade = (resultado.valor_liquido / resultado.valor_total_investido - 1) * 100
    print(f"🚀 Rentabilidade no Período: {rentabilidade:.2f}%")
    print("="*45 + "\n")

def menu_principal():
    print("\n" + "Selectione uma opção:" )
    print("1. Simulação Manual (Digitar Taxa)")
    print("2. Recomendação por Perfil (Ranking Inteligente)") # <-- NOME AJUSTADO
    print("0. Sair")
    return input("\nOpção: ")

def main():
    print("--- Simulador de Investimentos Profissional ---")
    
    while True:
        opcao = menu_principal()
        
        if opcao == "0":
            break
            
        try:
            v_ini = limpar_entrada(input("Valor inicial (R$): "))
            v_aporte = limpar_entrada(input("Aporte mensal (R$): "))
            tempo = int(input("Tempo (meses): "))
            if tempo <= 0: raise ValueError("Tempo deve ser maior que zero.")
            inflacao = normalizar_taxa(limpar_entrada(input("Inflação anual (%): ")))

            if opcao == "1":
                taxa = normalizar_taxa(limpar_entrada(input("Taxa anual (%): ")))
                res = simular_investimento_completo(v_ini, v_aporte, taxa, tempo, inflacao)
                exibir_relatorio(res)

            elif opcao == "2":
                # --- NOVAS PERGUNTAS DE PERFIL ---
                print("\nQual seu perfil?\n1-Conservador | 2-Arrojado")
                perf = "conservador" if input("Opção: ") == "1" else "arrojado"
                print("\nQual seu prazo?\n1-Curto Prazo | 2-Longo Prazo")
                praz = "curto" if input("Opção: ") == "1" else "longo"
                
                # --- INTEGRAÇÃO COM COMPARADOR E RECOMENDADOR ---
                lista_bruta = comparar_bancos(v_ini, v_aporte, tempo, inflacao)
                ranking = recomendar_investimentos({"perfil": perf, "prazo": praz}, lista_bruta)
                
                print("\n⭐ RANKING RECOMENDADO PARA VOCÊ:")
                
                for i, item in enumerate(ranking, 1):
                    res = item['resultado'] 
                    isento_str = "[ISENTO]" if item['isento'] else ""
                    
                    # Exibe o Score e a Justificativa (Inteligência nova)
                    print(f"{i}º - {item['banco']} ({item['produto']}) - {item['score']} pts {isento_str}")
                    print(f"    💡 {', '.join(item['justificativa'])}")
                    print(f"    👉 Líquido: R$ {res.valor_liquido:,.2f} | IR: R$ {res.valor_imposto:,.2f}")
                
                # --- RELATÓRIO DETALHADO DO VENCEDOR (Mantido como você pediu) ---
                detalhe = input("\nQuer ver o relatório detalhado do 1º lugar? (s/n): ")
                if detalhe.lower() == 's':
                    vencedor = ranking[0]
                    exibir_relatorio(vencedor['resultado'], f"VENCEDOR: {vencedor['banco']}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n💥 Erro inesperado: {e}")

if __name__ == "__main__":
    main()
