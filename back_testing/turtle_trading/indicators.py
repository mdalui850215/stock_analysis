import pandas as pd
import numpy as np

class IndicatorManager:
    """Calculates indicators for the Turtle Trading System: ATR and N-Day Channels."""

    def calculate_atr(self, df, period=20):
        """
        Calculates the Average True Range (ATR) using Wilder's Smoothing.
        Manual implementation to avoid talib binary incompatibility.
        """
        data = df.copy()
        
        # Get column names (handles both Open/Close and open/close)
        high_col = 'High' if 'High' in data.columns else 'high'
        low_col = 'Low' if 'Low' in data.columns else 'low'
        close_col = 'Close' if 'Close' in data.columns else 'close'

        # Compute True Range (TR)
        prev_close = data[close_col].shift(1)
        tr1 = data[high_col] - data[low_col]
        tr2 = abs(data[high_col] - prev_close)
        tr3 = abs(data[low_col] - prev_close)
        
        data['TR'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate ATR using Wilder's Smoothing (alpha = 1/period)
        data['ATR'] = data['TR'].ewm(alpha=1/period, min_periods=period, adjust=False).mean()
        
        # Lag the ATR by 1 to avoid look-ahead bias as in procedural code
        data['ATR'] = data['ATR'].shift(1)
        
        return data

    def calculate_channels(self, df, ndays_high=20, ndays_low=20):
        """Calculates rolling N-Day high and low channels (lagged by 1)."""
        data = df.copy()
        
        high_col = 'High' if 'High' in data.columns else 'high'
        low_col = 'Low' if 'Low' in data.columns else 'low'
        
        data['ndays_high'] = data[high_col].rolling(ndays_high).max().shift(1)
        data['ndays_low'] = data[low_col].rolling(ndays_low).min().shift(1)
        
        return data
