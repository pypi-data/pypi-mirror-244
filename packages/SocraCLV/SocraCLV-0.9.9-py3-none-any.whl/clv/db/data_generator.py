from faker import Faker
import pandas as pd
import random
import logging
from ..logger import CustomFormatter
import os

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

fake = Faker()

# Data Models

## Dim_Customer
def generate_dim_customer(customer_id):
    day1 = fake.date_time_this_decade()
    day2 = fake.date_time_this_decade()
    return {
        "customer_id": customer_id,
        "age": random.randint(18, 80),
        "gender": fake.random_element(elements=("Male", "Female")),
        "first_transaction_date": day2 if day1 > day2 else day1,
        "last_transaction_date": day1 if day1 > day2 else day2,
        "survival_time": abs(int(random.random() * (day1 - day2).days)),
        "event_observed": random.random() > 0.4
    }

## Dim_Payment_Method
def generate_dim_payment_method(payment_method_id):
    return {
        "payment_method_id": payment_method_id,
        "payment_method_name": fake.random_element(elements=("Credit Card", "Debit Card", "Paypal", "Bank Transfer", "Cash"))
    }

## Fact_Transacation
def generate_fact_transaction(transaction_id, customer_id, payment_method_id):
    transaction_date = fake.date_time_this_decade()
    amount = round(random.uniform(10.0, 500.0), 2)

    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "payment_method_id": payment_method_id,
        "transaction_date": transaction_date,
        "amount": amount
    }