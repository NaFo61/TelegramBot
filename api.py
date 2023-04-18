from config import TOKEN_API_KEY
import requests

class Trans:
    def __init__(self, from_, to_, amount_):
        self.from_ = from_.upper()   # Из какой валюты
        self.to_ = to_.upper()  # В какую валюту
        self.amount_ = amount_.upper()  # Сколько

    def get_result(self):
        url = f"https://api.apilayer.com/exchangerates_data/convert?"  # Ссылка для API

        params = {  # Параметры по которым будем отправлять запрос
            'to': self.to_,
            'from': self.from_,
            'amount': self.amount_,
            'apikey': TOKEN_API_KEY
        }

        response = requests.request("GET", url, params=params)  # Получаем ответ

        result = response.json()  # Расшифровываем ответ

        result = result.get('result')  # Извлекаем значение по ключу result
        return result  # Возращаем ответ

class Rate:
    def get_rates(self):
        import requests

        url = f"https://api.apilayer.com/exchangerates_data/latest?"

        params_1 = {  # Параметры по которым будем отправлять запрос
            'symbols': 'RUB',
            'base': 'USD',
            'apikey': TOKEN_API_KEY
        }

        params_2 = {  # Параметры по которым будем отправлять запрос
            'symbols': 'RUB',
            'base': 'EUR',
            'apikey': TOKEN_API_KEY
        }

        response_1 = requests.request("GET", url, params=params_1)  # Получаем ответ
        result_1 = response_1.json().get('rates').get('RUB')  # Расшифровываем ответ

        response_2 = requests.request("GET", url, params=params_2)  # Получаем ответ
        result_2 = response_2.json().get('rates').get('RUB')  # Расшифровываем ответ
        return (result_1, result_2)  # Возращаем ответ
