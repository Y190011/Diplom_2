import pytest
from methods.customer_methods import CustomerMethods
from methods.order_methods    import OrderMethods
@pytest.fixture()
def customer():
    customer_methods = CustomerMethods()
    customer_data = customer_methods.creation_customer_with_verification()
    yield customer_data
    customer_methods.delete_customer(customer_data[0])

@pytest.fixture()
def customer_methods():
    customer_methods = CustomerMethods()
    return customer_methods

@pytest.fixture()
def order_methods():
    order_methods = OrderMethods()
    yield order_methods