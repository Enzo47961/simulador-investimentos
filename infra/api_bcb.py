# infra/api_bcb.py
import requests

def _buscar_serie(codigo):
    """
    Função interna genérica para buscar séries do Banco Central (SGS).
    Retorna o valor mais recente em formato decimal (ex: 0.1075).
    """
    try:
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"

        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()

        dados = resposta.json()

        if not dados:
            raise ValueError("API retornou lista vazia")

        valor_str = dados[0]['valor']  # agora é o primeiro (e único)
        valor = float(valor_str.replace(",", "."))

        return valor / 100

    except Exception as e:
        print(f"[ERRO API BCB] Código {codigo}: {e}")
        return None


def buscar_selic_atual():
    valor = _buscar_serie(432)
    return valor if valor is not None else 0.1075


def buscar_cdi_atual():
    valor_diario = _buscar_serie(4389)
    if valor_diario is not None:
        # Converte taxa diária para anualizada: (1 + i)^252 - 1
        taxa_anual = (1 + valor_diario)**252 - 1
        return taxa_anual
    return 0.1065 # Backup

def buscar_ipca_atual():
    """
    Busca o IPCA acumulado dos últimos 12 meses (SGS 13522).
    É o valor ideal para o cálculo de 'Poder de Compra'.
    """
    valor = _buscar_serie(13522)
    # Em março de 2026, a projeção do Focus gira em torno de 4.1%
    return valor if valor is not None else 0.041 
