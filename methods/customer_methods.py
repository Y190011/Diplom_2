import requests
import pytest
import json
from config import BASE_URL, USER_URL, REGISTER_URL, LOGIN_URL, USER_URL
import helper

class CustomerMethods:

    def create_new_customer(self, params):
        response = requests.post(f'{BASE_URL}{REGISTER_URL}', data=params)
        return response.status_code, response.json()

    def login_existing_customer(self, params):
        response = requests.post(f'{BASE_URL}{LOGIN_URL}', data=params)
        return response.status_code, response.json()

    def delete_customer(self, authorization_token):
        headers  = {'Authorization':authorization_token}
        response = requests.delete(f'{BASE_URL}{USER_URL}', headers=headers)
        assert response.status_code == 202 and response.json()['success'] == True, \
             f"status_code {response.status_code}, success {response.json()['success']}"
        return response.status_code, response.json()

    def get_customer_data(self, authorization_token ):
        headers  = {'Authorization':authorization_token}
        response = requests.get(f'{BASE_URL}{USER_URL}', headers=headers)
        return response.status_code, response.json()

    def set_customer_data(self, authorization_token, params):
        headers = {'Authorization': authorization_token}
        response = requests.patch(f'{BASE_URL}{USER_URL}', headers=headers, data = params)
        return response.status_code, response.json()

    def creation_customer_with_verification(self):
        customer_name, customer_password, customer_email = helper.create_random_customer_data()
        status_code, json_reply = self.create_new_customer(
            {"email": customer_email, "password": customer_password, "name": customer_name})
        assert status_code == 200 and json_reply['success'] == True, \
             f"Status_code {status_code}, success {json_reply['success']}"
        authorization_token = json_reply['accessToken']
        refresh_token       = json_reply['refreshToken']
        return authorization_token, customer_name, customer_password, customer_email, refresh_token

