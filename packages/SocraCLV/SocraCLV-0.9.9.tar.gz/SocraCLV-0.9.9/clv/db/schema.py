import logging
import os

from ..logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


from sqlalchemy import create_engine,Column,Integer,String,Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



engine = create_engine('sqlite:///internet_service_provider.db')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Dim_Payment_Method(Base):
    """
    Dimension table for storing different payment methods.
    
    Attributes:
    - payment_method_id: Unique identifier for the payment method (Primary Key).
    - payment_method_name: Descriptive name of the payment method.
    """
    __tablename__ = "dim_payment_method"

    payment_method_id = Column(Integer, primary_key=True)
    payment_method_name = Column(String(255))


class Dim_Customer(Base):
    """
    Dimension table for storing customer details.
    
    Attributes:
    - customer_id: Unique identifier for the customer (Primary Key).
    - age: Age of the customer.
    - gender: Gender of the customer.
    - first_transaction_date: Date of the first transaction made by the customer.
    - last_transaction_date: Date of the last transaction made by the customer.
    - survival_time: The duration (in days) between the first and last transaction.
    - event_observed: A Boolean flag indicating whether an event of interest (e.g., churn) has been observed.
    """
    __tablename__ = "dim_customer"

    customer_id = Column(Integer, primary_key=True)
    age = Column(Integer)
    gender = Column(String(100))
    first_transaction_date = Column(DateTime)
    last_transaction_date = Column(DateTime)
    survival_time = Column(Integer)
    event_observed = Column(Boolean)


class Fact_Transacation(Base):
    """
    Fact table for storing transactions.
    
    Attributes:
    - transaction_id: Unique identifier for the transaction (Primary Key).
    - customer_id: Identifier for the customer. Foreign key to dim_customer table.
    - payment_method_id: Identifier for the payment method. Foreign key to dim_payment_method table.
    - transaction_date: Date and time when the transaction occurred.
    - amount: The monetary value of the transaction.
    
    Relationships:
    - customer: Establishes a relationship with the Dim_Customer table, with a back-reference named 'transaction'.
    - payment_method: Establishes a relationship with the Dim_Payment_Method table, with a back-reference named 'transaction'.
    """
    __tablename__ = "fact_transaction"

    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('dim_customer.customer_id'))
    payment_method_id = Column(Integer, ForeignKey('dim_payment_method.payment_method_id'))
    transaction_date = Column(DateTime)
    amount = Column(Float)

    customer = relationship("Dim_Customer", backref="transaction")
    payment_method = relationship("Dim_Payment_Method", backref="transaction")


class CLV_Prediction(Base):
    """
    Table for storing customer lifetime value predictions.
    
    Attributes:
    - prediction_id: Unique identifier for each prediction (Primary Key, auto-incremented).
    - customer_id: Identifier for the customer, linked to the dim_customer table.
    - clv: Predicted Customer Lifetime Value.
    - customer_type: Type of customer (e.g., new, returning, loyal).
    - is_campaign1_success: Boolean flag indicating the success of the first campaign for the customer.
    - is_campaign2_success: Boolean flag indicating the success of the second campaign for the customer.
    
    Relationships:
    - customer: Establishes a relationship with the Dim_Customer table, indicating which customer this prediction is for.
    """
    __tablename__ = "clv_prediction"

    prediction_id = Column(Integer, autoincrement=True, primary_key=True)
    customer_id = Column(Integer, ForeignKey('dim_customer.customer_id'))
    clv = Column(Float)
    predicted_customer_type = Column(String)
    is_campaign1_success = Column(Boolean)
    is_campaign2_success = Column(Boolean)


Base.metadata.create_all(engine)


