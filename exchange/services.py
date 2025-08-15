# exchange/services.py
import requests

def get_currency_rates():
    """
    Busca taxas de câmbio de uma API.
    Por enquanto, retorna dados de exemplo para não bloquear o desenvolvimento.
    """
    try:
        # No futuro, podemos usar uma API real como a AwesomeAPI
        # response = requests.get('https://economia.awesomeapi.com.br/json/all/USD-BRL,EUR-BRL,GBP-BRL')
        # data = response.json()
        # Lógica para formatar os dados viria aqui
        pass # Ignora a chamada real por enquanto
    except requests.RequestException as e:
        # Se a API falhar, retorna os dados de exemplo
        print(f"API de câmbio indisponível: {e}. Usando dados de exemplo.")
        
    # Retorna uma lista com dados de exemplo (mock)
    return [
        {'code': 'USD', 'name': 'Dólar Americano', 'bid': '5.15'},
        {'code': 'EUR', 'name': 'Euro', 'bid': '5.60'},
        {'code': 'GBP', 'name': 'Libra Esterlina', 'bid': '6.25'},
    ]