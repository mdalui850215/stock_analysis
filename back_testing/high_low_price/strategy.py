import pandas as pd
import numpy as np

class HighLowStrategy:
    """Strategy: Long on 20-day high breakout, exit on 20-day low breach."""

    def generate_signals(self, df):
        """
        Generates buy and sell signals based on channel breakouts.
        data: DataFrame containing 'ndays_high', 'ndays_low' and price data.
        """
        data = df.copy()
        
        # Column mapping
        close_col = 'Close' if 'Close' in data.columns else 'close'
        
        # Initializing columns
        data['signal'] = 0.0
        data['trade_price'] = 0.0
        data['trade_ret'] = 0.0
        
        n = len(data)

        # Iterative logic to match procedural code exactly
        for i in range(1, n):
            prev_signal = data['signal'].iloc[i-1]
            curr_close = data[close_col].iloc[i]
            n_high = data['ndays_high'].iloc[i]
            n_low = data['ndays_low'].iloc[i]

            # Check if we have no position
            if prev_signal == 0:
                if curr_close > n_high:
                    data.iloc[i, data.columns.get_loc('signal')] = 1.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = n_high
                else:
                    data.iloc[i, data.columns.get_loc('trade_price')] = curr_close
            
            # Check if we have a long position
            elif prev_signal == 1:
                if curr_close < n_low:
                    data.iloc[i, data.columns.get_loc('signal')] = 0.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = n_low
                    # Trade return computed only on the day of exit
                    data.iloc[i, data.columns.get_loc('trade_ret')] = (data.iloc[i]['trade_price'] / data.iloc[i-1]['trade_price']) - 1
                else:
                    data.iloc[i, data.columns.get_loc('signal')] = 1.0
                    data.iloc[i, data.columns.get_loc('trade_price')] = data.iloc[i-1]['trade_price']

        return data
