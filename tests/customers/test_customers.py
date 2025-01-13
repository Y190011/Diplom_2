from methods.customer_methods import CustomerMethods
import pytest
import helper
import allure
from config import customer_email, customer_password, customer_name, empty_token, empty_value, \
                   EMAIL_PASSWORD_NAME_REQUIRED, USER_ALREADY_EXIST, EMAIL_OR_PASSWORD_INCORRECT, \
                   non_exist_email, non_exist_password, non_exist_name


@allure.title("Тестирование работы с пользователями")
class TestCustomers:

    @allure.step("Тест - создание пользователя и повторное создание пользователя, который уже существует")
    def test_create_customer_and_again(self, customer, customer_methods):
        (authorization_token, created_customer_name, created_customer_password, created_customer_email,
                              refresh_token) = customer
        status_code, json_reply = customer_methods.create_new_customer(
                {"email": created_customer_email,"password": created_customer_password,"name": created_customer_name})
        assert status_code == 403 and json_reply['success'] == False and \
               json_reply['message'] == USER_ALREADY_EXIST, \
             f"Status_code {status_code}, success {json_reply['success']}, message '{json_reply['message']}'"

    @pytest.mark.parametrize('email, password, name, field_name', [
        [empty_value, non_exist_password, non_exist_name, 'email'],
        [non_exist_email, empty_value, non_exist_name, 'password'],
        [non_exist_email, non_exist_password, empty_value, 'name']
    ])
    @allure.step("Тест - создание пользователя с пустым значением обязательного поля '{field_name}'")
    def test_create_customer_with_empty_field(self, customer_methods, email, password, name, field_name):
        status_code, json_reply = customer_methods.create_new_customer(
            {"email": email, "password": password, "name": name})
        assert (status_code == 403 and json_reply['success'] == False
                and json_reply['message'] == EMAIL_PASSWORD_NAME_REQUIRED ), \
             f"Status_code {status_code}, success {json_reply['success']}, message '{json_reply['message']}'"


    @pytest.mark.parametrize('email, password, field_name', [
                             [non_exist_email, customer_password,  'email'],
                             [customer_email,  non_exist_password, 'password'],
                             ])
    @allure.step("Тест - авторизация для существующего пользователя с некорректным значением поля {field_name}")
    def test_login_existing_customer_with_incorrect_data(self, customer_methods, email, password, field_name):
        status_code, json_reply = customer_methods.login_existing_customer(
            {"email": email, "password": password})
        assert status_code == 401 and json_reply['success'] == False and \
               json_reply['message'] == EMAIL_OR_PASSWORD_INCORRECT, \
             f"Status_code {status_code}, success {json_reply['success']}, message '{json_reply['message']}'"

    @allure.step("Тест - авторизация для существующего пользователя с корректными логином и паролем")
    def test_login_existing_customer_with_correct_login_data(self, customer_methods):
        status_code, json_reply = customer_methods.login_existing_customer(
            {"email": customer_email,"password": customer_password,"name": customer_name})
        assert status_code == 200 and json_reply['success'] == True, \
             f"Status_code {status_code}, success {json_reply['success']}"

    @allure.step("Тест - получение данных авторизованного пользователя")
    def test_get_customer_data_with_authorization(self, customer, customer_methods):
        authorization_token, name, password, email, refresh_token = customer
        status_code, json_reply = customer_methods.get_customer_data(authorization_token)
        assert status_code == 200 and json_reply['success'] == True and json_reply['user']['email'] == email and \
               json_reply['user']['name'] == name, \
             f"Status_code {status_code}, success {json_reply['success']}, email '{json_reply['user']['email']}, \
               name {json_reply['user']['name']}"

    @allure.step("Тест - изменение данных авторизованного пользователя")
    def test_change_customer_data_with_authorization(self, customer, customer_methods):
        authorization_token  = customer[0]
        new_name, new_password, new_email = helper.create_random_customer_data()
        parameters = {"email": new_email, "password": new_password, "name": new_name}
        status_code, json_reply = customer_methods.set_customer_data(authorization_token, parameters)
        assert status_code == 200 and json_reply['success'] == True, \
             f"Status_code {status_code}, success {json_reply['success']}"
        status_code, json_reply = customer_methods.get_customer_data(authorization_token)
        assert status_code == 200 and json_reply['success'] == True and json_reply['user']['email'] == new_email and \
               json_reply['user']['name'] == new_name, \
             f"Status_code {status_code}, success {json_reply['success']}, email {json_reply['user']['email']} \
              name {json_reply['user']['name']}"
        status_code, json_reply = customer_methods.login_existing_customer(parameters)
        assert status_code == 200 and json_reply['success'] == True, \
             f"Status_code {status_code}, success {json_reply['success']}"

    @allure.step("Тест - изменение данных неавторизованного пользователя ")
    def test_change_customer_data_without_authorization(self, customer_methods):
        new_name, new_password, new_email = helper.create_random_customer_data()
        parameters = {"email": new_email, "password": new_password, "name": new_name}
        status_code, json_reply = customer_methods.set_customer_data(empty_token, parameters)
        assert status_code == 401 and json_reply['success'] == False, \
             f"Status_code {status_code}, success {json_reply['success']}"