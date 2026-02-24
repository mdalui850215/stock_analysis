import pandas as pd

class IndicatorManager:
    """Calculates indicators for the High/Low Price strategy: N-Day High and Low."""

    def calculate_channels(self, df, ndays_high=20, ndays_low=20):
        """
        Calculates the moving highest high and lowest low.
        Supports both 'High/Low' and 'high/low' column names.
        Values are shifted by 1 to avoid look-ahead bias.
        """
        data = df.copy()
        
        # Mapping column names (supporting lowercase)
        high_col = 'High' if 'High' in data.columns else 'high'
        low_col = 'Low' if 'Low' in data.columns else 'low'
        
        if high_col not in data.columns or low_col not in data.columns:
            raise KeyError(f"Required High/Low columns not found. Available: {list(data.columns)}")

        data['ndays_high'] = data[high_col].rolling(ndays_high).max().shift(1)
        data['ndays_low'] = data[low_col].rolling(ndays_low).min().shift(1)
        
        return data
