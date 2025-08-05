import pandas as pd
import numpy as np
 
def generate_mock_data():
    np.random.seed(42)
 
    data = {
        "week": pd.date_range(start="2023-01-01", periods=20, freq="W"),
        "total_users": np.random.randint(5000, 6000, 20),
        "reg_to_open_cvr": np.random.uniform(40, 55, 20),
        "verification_cvr": np.random.uniform(50, 60, 20),
        "open_to_txn_cvr": np.random.uniform(8, 14, 20),
        "first_deposit_cvr": np.random.uniform(60, 70, 20),
        "total_txns": np.random.randint(200, 300, 20),
        "median_time_open": np.random.normal(340, 20, 20),
        "fast_reg_5m": np.random.uniform(20, 30, 20),
        "fast_reg_10m": np.random.uniform(50, 60, 20),
    }
    return pd.DataFrame(data)