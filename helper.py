import random

def gen_random_number():
    i = random.randint(100000, 999999)
    s = f'{i:06}'
    return s

def gen_random_email():
    return "yname_yfam_15_" + gen_random_number() + "@ya.ru"

def gen_random_name():
    return "yname_yfam_" + gen_random_number()

def gen_random_password():
    return "password" + gen_random_number()

def create_random_customer_data():
    return gen_random_name(), gen_random_password(), gen_random_email()