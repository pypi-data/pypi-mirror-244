from .Data_Processing import MM, p

class CLV():
    def __init__(self, t, customer_id):
        """
        Initialize the CLV calculator with the specified time 't' and customer ID.

        Parameters:
        -----------
        t : int
            Time for which CLV is calculated.
        customer_id : int
            Identifier for the customer, for which the CLV is calculated.
        """
        self.t = t
        self.customer_id = customer_id

    def calculate_clv(self):
        """
        Calculate the Customer Lifetime Value (CLV) based on survival probabilities.

        Returns:
        --------
        float:
            The calculated Customer Lifetime Value (CLV) rounded to three decimal places.
        """
        # Define the discount rate
        discount_rate = 0.1025  # 10.25% as a decimal

        # Get the monthly margins and probabilities for the customer
        monthly_margin = MM()
        customer_probabilities = p()

        # Extract relevant probabilities based on t and customer_id
        probabilities_list = customer_probabilities.loc[1:self.t, self.customer_id].values.tolist()

        # Calculate the CLV using the formula
        clv = 0
        for i in range(len(probabilities_list)):
            clv += (probabilities_list[i] / ((1 + discount_rate / 12) ** i))

        clv *= monthly_margin
        clv = round(clv, 3)

        return clv
