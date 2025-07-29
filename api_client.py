import requests
import json

def get_currency_quotes(currency_list):
    """
    Busca as cotações atuais para uma lista de moedas em relação ao Real.
    Ex: currency_list=['USD', 'EUR', 'CAD']
    Retorna um dicionário com os dados ou None em caso de erro.
    """
    if not currency_list:
        return {} # Retorna vazio se a lista estiver vazia

    # Converte ['USD', 'EUR'] para 'USD-BRL,EUR-BRL'
    pairs = [f"{code}-BRL" for code in currency_list]
    url_suffix = ",".join(pairs)
    url = f"https://economia.awesomeapi.com.br/last/{url_suffix}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar cotações da API: {e}")
        return None
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON da API.")
        return None

# --- NOVA FUNÇÃO ---
def get_historical_data(currency_code, days=30):
    """
    Busca os dados históricos de uma moeda nos últimos N dias.
    Ex: currency_code='USD', days=30
    """
    url = f"https://economia.awesomeapi.com.br/json/daily/{currency_code}-BRL/{days}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        # A API retorna erro 404 em texto puro se a moeda não for encontrada
        if isinstance(data, list):
            return data
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados históricos para {currency_code}: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON histórico para {currency_code}.")
        return None


if __name__ == '__main__':
    quotes = get_currency_quotes()
    if quotes:
        print("Cotações recebidas com sucesso:")
        print(json.dumps(quotes, indent=2))
    
    # Teste da nova função
    historical = get_historical_data("USD", 7)
    if historical:
        print("\nHistórico dos últimos 7 dias para o Dólar:")
        print(json.dumps(historical, indent=2))