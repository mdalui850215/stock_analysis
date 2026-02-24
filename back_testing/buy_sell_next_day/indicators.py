import pandas as pd
import numpy as np

class IndicatorManager:
    """Calculates indicators for the Buy and Sell Next Day strategy."""
    
    def calculate_returns(self, df):
        """Calculates Open-Open, Close-Close, and Open-Close returns."""
        if df.empty:
            return df
            
        data = df.copy()
        
        # Check for column names (support both Open/Close and open/close)
        open_col = 'Open' if 'Open' in data.columns else 'open'
        close_col = 'Close' if 'Close' in data.columns else 'close'
        
        if open_col not in data.columns or close_col not in data.columns:
             raise KeyError(f"Required columns not found. Available: {list(data.columns)}")
        
        # Create log returns as per the procedural code
        data['oo_returns'] = np.log(data[open_col] / data[open_col].shift(1))
        data['cc_returns'] = np.log(data[close_col] / data[close_col].shift(1))
        data['oc_returns'] = np.log(data[close_col] / data[open_col])
        
        return data

    def calculate_down_days(self, df):
        """Identifies consecutive down days based on Close-Close returns."""
        data = df.copy()
        # Mark days with negative close-to-close returns
        data['is_down'] = np.where(data['cc_returns'] < 0, 1, 0)
        
        # Consecutive count: reset when 'is_down' is 0
        # A simple way to compute consecutive count:
        group = (data['is_down'] == 0).cumsum()
        data['consecutive_down'] = data.groupby(group)['is_down'].cumsum()
        
        return data
