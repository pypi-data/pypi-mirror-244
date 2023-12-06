from ..db import SqlHandler
from ..logger import CustomFormatter
import pandas as pd
import numpy as np
from datetime import datetime
from lifelines import LogNormalAFTFitter, LogNormalFitter


# Create an instance of SqlHandler
clv_handler = SqlHandler('internet_service_provider', 'fact_transaction')

# Get transaction table data
data = clv_handler.get_table_data()
clv_handler.close_cnxn()

connect_to_dim_customer = SqlHandler('internet_service_provider', 'dim_customer')

# Get transaction table data
dim_customer = connect_to_dim_customer.get_table_data()
connect_to_dim_customer.close_cnxn()
dim_customer['survival_time_months'] = 1 + dim_customer['survival_time'] // 30


# Convert 'transaction_date' to datetime
data['transaction_date'] = pd.to_datetime(data['transaction_date'])


def MM():
    """
    Calculate the average monthly margin based on the last year's transaction data.

    Returns:
    -------
    float:
        The calculated average monthly margin.
    """

    # Filter the data for the previous year
    prev_year = data['transaction_date'].dt.year.max()-1
    filtered_data = data[data['transaction_date'].dt.year == prev_year]

    # Calculate the average monthly margin for the previous year
    average_monthly_margin = np.sum(filtered_data['amount']) / 12

    return average_monthly_margin

def p():
    """
    Calculate the survival probabilities for customers using AFT estimator for a year.

    Returns:
    --------
    Dataframe:
        A dataframe of survival probabilities at different time points up to 12 months for each customer.
    """
    data = dim_customer.copy()
    data.drop(columns=['first_transaction_date', 'last_transaction_date'], inplace=True)
    data = pd.get_dummies(data, columns=['gender'], prefix='gender', drop_first=True)


    log_aft = LogNormalAFTFitter()
    log_aft.fit(data, duration_col="survival_time_months", event_col="event_observed")
    time_points = list(range(1, 13))
    pred = log_aft.predict_survival_function(data, times=time_points)


    return pred