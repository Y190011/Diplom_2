import json
import helper
from config import BASE_URL, INGREDIENTS_URL, ORDERS_URL
import requests

class OrderMethods:
    @staticmethod
    def get_ingredients_list():
        response = requests.get(f'{BASE_URL}{INGREDIENTS_URL}')
        assert response.status_code == 200 and response.json()['success'] == True
        ingredient_list = response.json()['data']
        bun_list      = []
        sauce_list    = []
        main_list     = []
        for ingredient in ingredient_list:
            ingredient_characteristic = ingredient['_id'],ingredient['type'], ingredient['name']
            if ingredient['type'] == 'bun':
                bun_list.append(ingredient_characteristic)
            elif ingredient['type'] == 'sauce':
                sauce_list.append(ingredient_characteristic)
            elif ingredient['type'] == 'main':
                main_list.append(ingredient_characteristic)
        return bun_list, sauce_list, main_list


    def create_order(self, authorization_token, params):
        headers = {'Authorization': authorization_token}
        response = requests.post(f'{BASE_URL}{ORDERS_URL}', headers=headers, data = params)
        return response.status_code, response.json()

    def create_order_without_authorization(self, params):
        response = requests.post(f'{BASE_URL}{ORDERS_URL}', data = params)
        return response.status_code, response.json()

    def get_authorized_customer_order_list(self, authorization_token):
        headers = {'Authorization': authorization_token}
        response = requests.get(f'{BASE_URL}{ORDERS_URL}',headers = headers)
        return response.status_code, response.json()

    def get_unathorized_customer_order_list(self):
        response = requests.get(f'{BASE_URL}{ORDERS_URL}')
        return response.status_code, response.json()