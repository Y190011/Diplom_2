from methods.order_methods import OrderMethods
from methods.customer_methods import CustomerMethods
import pytest
import helper
import allure
from config import customer_email, customer_password, customer_name, incorrect_ingredient, YOU_SHOULD_BE_AUTHORIZED, \
                   INGREDIENT_MUST_BE_PROVIDED


@allure.title("Тестирование работы с заказами")
class TestOrders:

    @allure.step("Тест - получение списка ингредиентов")
    def test_get_ingredients(self, order_methods):
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        assert len(bun_list) > 1 and len(sauce_list) > 3 and len(main_list) > 7,  \
             f"bun {len(bun_list)}, sauce {len(sauce_list)}, fillings {len(main_list)}"

    @allure.step("Тест - создание заказа с авторизацией с пустым списком ингредиентов")
    def test_create_order_with_authorization_without_ingredients(self, customer, order_methods):
        authorization_token = customer[0]
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        params = {}
        status_code, json_reply = order_methods.create_order(authorization_token, params)
        assert status_code == 400 and json_reply['success'] == False and   \
               json_reply['message'] == INGREDIENT_MUST_BE_PROVIDED, \
             f"Status_code {status_code}, success {json_reply['success']}, message '{json_reply['message']}'"


    @allure.step("Тест - создание заказа с авторизацией с правильными ингредиентами")
    def test_create_order_with_authorization_with_ingredients(self, customer, order_methods):
        authorization_token = customer[0]
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        params = {"ingredients": [bun_list[0][0], sauce_list[0][0], main_list[0][0]]}
        status_code, json_reply = order_methods.create_order(authorization_token, params)
        assert status_code == 200 and json_reply['success'] == True and json_reply['order']['number'] is not None and \
               len(json_reply['order']['ingredients']) == 3, \
             f"status_code {status_code}, success {json_reply['success']}, number {json_reply['order']['number']}, \
               order_ingredients {len(json_reply['order']['ingredients'])}"

    @allure.step("Тест - создание заказа с авторизацией с некорректной булкой")
    def test_create_order_with_authorization_with_incorrect_bun(self, customer, order_methods):
        authorization_token = customer[0]
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        params = {"ingredients": [incorrect_ingredient, sauce_list[0][0], main_list[0][0]]}
        status_code, json_reply = order_methods.create_order(authorization_token, params)
        assert status_code == 200 and len(json_reply['order']['ingredients']) == 2, \
             f"status_code {status_code}, order_ingredients {len(json_reply['order']['ingredients'])}"

    @allure.step("Тест - создание заказа с авторизацией с некорректным соусом")
    def test_create_order_with_authorization_with_incorrect_sauce(self, customer, order_methods):
        authorization_token = customer[0]
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        params = {"ingredients": [bun_list[0][0],incorrect_ingredient, main_list[0][0]]}
        status_code, json_reply = order_methods.create_order(authorization_token, params)
        assert status_code == 200 and len(json_reply['order']['ingredients']) == 2, \
             f"status_code {status_code}, order_ingredients {len(json_reply['order']['ingredients'])}"

    @allure.step("Тест - создание заказа с авторизацией с некорректным соусом")
    def test_create_order_with_authorization_with_incorrect_main(self, customer, order_methods):
        authorization_token = customer[0]
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        params = {"ingredients": [bun_list[0][0], sauce_list[0][0], incorrect_ingredient]}
        status_code, json_reply = order_methods.create_order(authorization_token, params)
        assert status_code == 200 and len(json_reply['order']['ingredients']) == 2, \
             f"status_code {status_code}, order_ingredients {len(json_reply['order']['ingredients'])}"

    @allure.step("Тест - создание заказа без авторизации")
    def test_create_order_without_authorization(self, order_methods):
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        params = {"ingredients": [bun_list[0][0], sauce_list[0][0], main_list[0][0]]}
        status_code, json_reply = order_methods.create_order_without_authorization(params)
        assert status_code == 200 and json_reply['order']['number'] is not None, \
             f"status_code {status_code}, number {json_reply['order']['number']}"

    @allure.step("Тест - создание заказов для авторизованного пользователя и получение их списка")
    def test_get_aunhorized_customer_order_list(self, customer, order_methods):
        authorization_token = customer[0]
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()

        params = {"ingredients": [bun_list[0][0], sauce_list[0][0], main_list[0][0]]}
        status_code, json_reply = order_methods.create_order(authorization_token, params)
        params = {"ingredients": [bun_list[1][0], sauce_list[1][0], main_list[1][0]]}
        status_code, json_reply = order_methods.create_order(authorization_token, params)
        params = {"ingredients": [bun_list[1][0], sauce_list[2][0], main_list[2][0]]}
        status_code, json_reply = order_methods.create_order(authorization_token, params)

        status_code, json_reply = order_methods.get_authorized_customer_order_list(authorization_token)
        assert status_code == 200 and len(json_reply['orders']) == 3, \
             f"status_code {status_code}, order_numbers {len(json_reply['orders'])}"

    @allure.step("Тест - создание заказов для неавторизованного пользователя и получение их списка")
    def test_get_unathorized_customer_order_list(self, order_methods):
        bun_list, sauce_list, main_list = order_methods.get_ingredients_list()
        params = {"ingredients": [bun_list[0][0], sauce_list[0][0], main_list[0][0]]}
        status_code, json_reply = order_methods.create_order_without_authorization(params)
        status_code, json_reply = order_methods.get_unathorized_customer_order_list()
        assert status_code == 401 and json_reply['success'] == False and \
               json_reply['message'] == YOU_SHOULD_BE_AUTHORIZED, \
             f"status_code {status_code}, order_numbers {len(json_reply['orders'])}"



